from sqlalchemy.orm import Session
from app.models.user import User


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create(db: Session, name: str, email: str, password_hash: str, user_type: str) -> User:
    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        user_type=user_type,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
