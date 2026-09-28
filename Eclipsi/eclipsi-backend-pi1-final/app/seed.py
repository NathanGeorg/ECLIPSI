from app.database.connection import Base, SessionLocal, engine
from app.models.professional import ProfessionalProfile
from app.models.user import User
from app.repositories.user_repository import get_by_email
from app.services.auth_service import hash_password


def seed_database():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if get_by_email(db, "joao@eclipsi.test"):
            return

        joao = User(
            name="João Banana",
            email="joao@eclipsi.test",
            password_hash=hash_password("123456"),
            user_type="PATIENT",
        )
        maria = User(
            name="Maria Demal",
            email="maria@eclipsi.test",
            password_hash=hash_password("123456"),
            user_type="PROFESSIONAL",
        )
        carlos = User(
            name="Carlos Souza",
            email="carlos@eclipsi.test",
            password_hash=hash_password("123456"),
            user_type="PROFESSIONAL",
        )

        db.add_all([joao, maria, carlos])
        db.commit()
        db.refresh(maria)
        db.refresh(carlos)

        db.add_all([
            ProfessionalProfile(
                user_id=maria.id,
                specialty="Psicóloga",
                approach="Terapia Cognitivo-Comportamental",
                description="Atendimento psicológico com foco em ansiedade, rotina e relações.",
                modality="Online",
                location="Recife",
                price=150.00,
            ),
            ProfessionalProfile(
                user_id=carlos.id,
                specialty="Psicólogo",
                approach="Psicanálise",
                description="Atendimento psicológico voltado à escuta e compreensão de questões pessoais.",
                modality="Presencial",
                location="Recife",
                price=120.00,
            ),
        ])
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
    print("Banco criado e dados fictícios inseridos.")
