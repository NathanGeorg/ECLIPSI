import hashlib
from sqlalchemy.orm import Session
from app.repositories import user_repository


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(db: Session, name: str, email: str, password: str, user_type: str):
    if user_repository.get_by_email(db, email):
        raise ValueError("E-mail já cadastrado.")

    return user_repository.create(
        db, name, email, hash_password(password), user_type
    )


def authenticate_user(db: Session, email: str, password: str):
    user = user_repository.get_by_email(db, email)
    if not user or user.password_hash != hash_password(password):
        return None
    return user
