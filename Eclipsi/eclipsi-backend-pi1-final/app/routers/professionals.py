from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.repositories.professional_repository import get_by_id, list_professionals
from app.schemas.professional import ProfessionalResponse

router = APIRouter(prefix="/professionals", tags=["Profissionais"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def to_response(row):
    profile, name = row
    return ProfessionalResponse(
        id=profile.id,
        user_id=profile.user_id,
        name=name,
        specialty=profile.specialty,
        approach=profile.approach,
        description=profile.description,
        modality=profile.modality,
        location=profile.location,
        price=profile.price,
    )


@router.get("", response_model=list[ProfessionalResponse])
def get_professionals(
    specialty: str | None = None,
    approach: str | None = None,
    modality: str | None = None,
    db: Session = Depends(get_db),
):
    return [to_response(row) for row in list_professionals(db, specialty, approach, modality)]


@router.get("/{professional_id}", response_model=ProfessionalResponse)
def get_professional(professional_id: int, db: Session = Depends(get_db)):
    row = get_by_id(db, professional_id)
    if not row:
        raise HTTPException(status_code=404, detail="Profissional não encontrado.")
    return to_response(row)
