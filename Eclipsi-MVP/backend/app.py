from datetime import datetime, timedelta
from decimal import Decimal
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Appointment, ProfessionalProfile, Rating, Record, User
from .security import create_token, hash_password, require_role, verify_password

app = FastAPI(title="ECLIPSI MVP API", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(pattern="^(patient|professional)$")
    registration_number: str | None = None
    uf: str | None = None
    specialty: str | None = None
    approach: str | None = None
    modality: str | None = None
    location: str | None = None
    price: Decimal | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfessionalRequest(BaseModel):
    specialty: str
    approach: str
    modality: str
    location: str | None = None
    price: Decimal = Field(gt=0)
    description: str = ""


class AppointmentRequest(BaseModel):
    professional_id: int
    starts_at: datetime
    ends_at: datetime


class RecordRequest(BaseModel):
    appointment_id: int
    content: str = Field(min_length=3)


class RatingRequest(BaseModel):
    appointment_id: int
    score: int = Field(ge=1, le=5)
    comment: str | None = None


class AdminUserUpdate(BaseModel):
    role: str | None = Field(default=None, pattern="^(patient|professional|admin)$")
    active: bool | None = None


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health():
    return {"status": "ok", "database": "sqlite", "synthetic": True}


@app.post("/api/auth/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(func.lower(User.email) == str(data.email).lower()).first():
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")
    if data.role == "professional" and not all((data.specialty, data.approach, data.modality, data.price)):
        raise HTTPException(status_code=422, detail="Profissional requer especialidade, abordagem, modalidade e preço.")
    if data.role == "professional":
        if not data.registration_number or not data.uf:
            raise HTTPException(status_code=422, detail="Profissional requer registro profissional e UF.")
        if len(data.uf) != 2 or not data.uf.isalpha():
            raise HTTPException(status_code=422, detail="UF inválida.")
    user = User(name=data.name, email=str(data.email).lower(), password_hash=hash_password(data.password), role=data.role)
    db.add(user)
    db.flush()
    if data.role == "professional":
        db.add(ProfessionalProfile(user_id=user.id, registration_number=data.registration_number,
                                   uf=data.uf.upper(), specialty=data.specialty, approach=data.approach,
                                   modality=data.modality, location=data.location, price=data.price,
                                   description="Perfil sintético criado no MVP consolidado."))
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}


@app.post("/api/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(func.lower(User.email) == str(data.email).lower(), User.active == True).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")
    return {"access_token": create_token(user.id), "token_type": "bearer", "role": user.role, "name": user.name}


@app.get("/api/professionals")
def search_professionals(name: str | None = None, specialty: str | None = None,
                        modality: str | None = None, description: str | None = None,
                        db: Session = Depends(get_db)):
    query = db.query(ProfessionalProfile, User).join(User, ProfessionalProfile.user_id == User.id).filter(User.active == True)
    if name:
        query = query.filter(func.lower(User.name).contains(name.lower()))
    if specialty:
        query = query.filter(func.lower(ProfessionalProfile.specialty).contains(specialty.lower()))
    if modality:
        query = query.filter(func.lower(ProfessionalProfile.modality).contains(modality.lower()))
    if description:
        query = query.filter(func.lower(ProfessionalProfile.description).contains(description.lower()))
    return [{"id": p.id, "name": u.name, "registration_number": p.registration_number, "uf": p.uf,
             "specialty": p.specialty, "approach": p.approach,
             "modality": p.modality, "location": p.location, "price": str(p.price), "description": p.description}
            for p, u in query.all()]


@app.post("/api/appointments", status_code=201)
def schedule(data: AppointmentRequest, user: User = Depends(require_role("patient")), db: Session = Depends(get_db)):
    if data.ends_at <= data.starts_at:
        raise HTTPException(status_code=422, detail="Horário final deve ser posterior ao inicial.")
    if data.starts_at <= datetime.utcnow():
        raise HTTPException(status_code=422, detail="O agendamento deve ser futuro.")
    professional = db.query(ProfessionalProfile).filter(ProfessionalProfile.id == data.professional_id).first()
    if not professional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado.")
    conflict = db.query(Appointment).filter(Appointment.professional_id == data.professional_id,
        Appointment.status != "cancelled", Appointment.starts_at < data.ends_at, Appointment.ends_at > data.starts_at).first()
    if conflict:
        raise HTTPException(status_code=409, detail="Horário indisponível.")
    appointment = Appointment(patient_id=user.id, professional_id=data.professional_id,
                              starts_at=data.starts_at, ends_at=data.ends_at,
                              price_at_booking=professional.price)
    db.add(appointment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Horário indisponível.")
    db.refresh(appointment)
    return {"id": appointment.id, "professional_id": appointment.professional_id, "starts_at": appointment.starts_at,
            "ends_at": appointment.ends_at, "status": appointment.status}


@app.get("/api/appointments")
def my_appointments(user: User = Depends(require_role("patient", "professional")), db: Session = Depends(get_db)):
    if user.role == "patient":
        rows = db.query(Appointment).filter(Appointment.patient_id == user.id).all()
    else:
        profile = db.query(ProfessionalProfile).filter(ProfessionalProfile.user_id == user.id).first()
        rows = db.query(Appointment).filter(Appointment.professional_id == profile.id).all() if profile else []
    return [{"id": r.id, "patient_id": r.patient_id, "professional_id": r.professional_id,
             "starts_at": r.starts_at, "ends_at": r.ends_at, "status": r.status,
             "price_at_booking": str(r.price_at_booking)} for r in rows]


@app.post("/api/records", status_code=201)
def create_record(data: RecordRequest, user: User = Depends(require_role("professional")), db: Session = Depends(get_db)):
    profile = db.query(ProfessionalProfile).filter(ProfessionalProfile.user_id == user.id).first()
    appointment = db.query(Appointment).filter(Appointment.id == data.appointment_id).first()
    if not profile or not appointment or appointment.professional_id != profile.id:
        raise HTTPException(status_code=404, detail="Consulta não pertence ao profissional.")
    record = Record(appointment_id=appointment.id, professional_id=profile.id, patient_id=appointment.patient_id, content=data.content)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, "appointment_id": record.appointment_id, "patient_id": record.patient_id,
            "created_at": record.created_at}


@app.get("/api/records")
def list_records(user: User = Depends(require_role("patient", "professional")), db: Session = Depends(get_db)):
    if user.role == "patient":
        rows = db.query(Record).filter(Record.patient_id == user.id).all()
    else:
        profile = db.query(ProfessionalProfile).filter(ProfessionalProfile.user_id == user.id).first()
        rows = db.query(Record).filter(Record.professional_id == profile.id).all() if profile else []
    return [{"id": r.id, "appointment_id": r.appointment_id, "patient_id": r.patient_id,
             "content": r.content, "created_at": r.created_at} for r in rows]


@app.post("/api/ratings", status_code=201)
def rate(data: RatingRequest, user: User = Depends(require_role("patient")), db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == data.appointment_id, Appointment.patient_id == user.id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    if appointment.status != "completed":
        raise HTTPException(status_code=409, detail="Avaliação disponível somente após consulta realizada.")
    if db.query(Rating).filter(Rating.appointment_id == appointment.id).first():
        raise HTTPException(status_code=409, detail="Consulta já avaliada.")
    rating = Rating(appointment_id=appointment.id, patient_id=user.id,
                    professional_id=appointment.professional_id, score=data.score, comment=data.comment)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return {"id": rating.id, "score": rating.score, "professional_id": rating.professional_id}


@app.get("/api/earnings")
def earnings(user: User = Depends(require_role("professional")), db: Session = Depends(get_db)):
    profile = db.query(ProfessionalProfile).filter(ProfessionalProfile.user_id == user.id).first()
    if not profile:
        return {"appointments_completed": 0, "estimated_earnings": "0.00"}
    completed = db.query(Appointment).filter(Appointment.professional_id == profile.id,
                                              Appointment.status == "completed").all()
    count = len(completed)
    total = sum((appointment.price_at_booking for appointment in completed), Decimal("0"))
    return {"appointments_completed": count, "estimated_earnings": f"{total:.2f}"}


@app.post("/api/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id: int, user: User = Depends(require_role("professional")), db: Session = Depends(get_db)):
    profile = db.query(ProfessionalProfile).filter(ProfessionalProfile.user_id == user.id).first()
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not profile or not appointment or appointment.professional_id != profile.id:
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    appointment.status = "completed"
    db.commit()
    return {"id": appointment.id, "status": appointment.status}


@app.get("/api/admin/stats")
def admin_stats(user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    return {"users": db.query(User).count(), "patients": db.query(User).filter(User.role == "patient").count(),
            "professionals": db.query(User).filter(User.role == "professional").count(),
            "appointments": db.query(Appointment).count(), "ratings": db.query(Rating).count()}


@app.get("/api/admin/users")
def admin_users(user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    return [{"id": item.id, "name": item.name, "email": item.email, "role": item.role, "active": item.active}
            for item in db.query(User).all()]


@app.patch("/api/admin/users/{user_id}")
def admin_update_user(user_id: int, data: AdminUserUpdate,
                      user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if data.role is not None:
        target.role = data.role
    if data.active is not None:
        target.active = data.active
    db.commit()
    return {"id": target.id, "name": target.name, "email": target.email, "role": target.role, "active": target.active}


@app.delete("/api/admin/users/{user_id}", status_code=204)
def admin_delete_user(user_id: int, user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if target.id == user.id:
        raise HTTPException(status_code=409, detail="Administrador não pode excluir a própria conta.")
    target.active = False
    db.commit()
    return None
