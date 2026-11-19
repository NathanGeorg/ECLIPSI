import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.database import Base, engine, SessionLocal
from backend.models import Appointment, ProfessionalProfile, Rating, Record, User
from backend.security import hash_password
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(User).count() == 0:
    admin = User(name="Admin Sintético", email="admin@example.com", password_hash=hash_password("Demo123!"), role="admin")
    professional = User(name="Dra. Ana Sintética", email="ana.psi@example.com", password_hash=hash_password("Demo123!"), role="professional")
    patient = User(name="Paciente Sintético", email="pac1@example.com", password_hash=hash_password("Demo123!"), role="patient")
    db.add_all([admin, professional, patient])
    db.flush()
    profile = ProfessionalProfile(user_id=professional.id, registration_number="CRP-EX-001",
                                  uf="SP", specialty="Psicologia", approach="TCC",
                                  modality="Online", location="Brasil (demonstrativo)", price="150.00",
                                  description="Perfil sintético para demonstração acadêmica.")
    db.add(profile)
    db.commit()
    print("Banco criado com dados sintéticos.")
else:
    print("Banco já inicializado.")
db.close()
