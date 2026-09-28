from sqlalchemy.orm import Session
from app.models.professional import ProfessionalProfile
from app.models.user import User


def list_professionals(db: Session, specialty=None, approach=None, modality=None):
    query = (
        db.query(ProfessionalProfile, User.name)
        .join(User, User.id == ProfessionalProfile.user_id)
        .filter(User.user_type == "PROFESSIONAL")
    )

    if specialty:
        query = query.filter(ProfessionalProfile.specialty.ilike(f"%{specialty}%"))
    if approach:
        query = query.filter(ProfessionalProfile.approach.ilike(f"%{approach}%"))
    if modality:
        query = query.filter(ProfessionalProfile.modality.ilike(f"%{modality}%"))

    return query.all()


def get_by_id(db: Session, professional_id: int):
    return (
        db.query(ProfessionalProfile, User.name)
        .join(User, User.id == ProfessionalProfile.user_id)
        .filter(
            ProfessionalProfile.id == professional_id,
            User.user_type == "PROFESSIONAL",
        )
        .first()
    )
