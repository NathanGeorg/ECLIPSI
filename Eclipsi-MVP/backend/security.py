import base64
import binascii
import hashlib
import hmac
import json
import os
import time
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .database import get_db
from .models import User

SECRET = os.getenv("ECLIPSI_SECRET", "local-synthetic-development-secret")
bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return "pbkdf2_sha256$200000$" + base64.urlsafe_b64encode(salt).decode().rstrip("=") + "$" + base64.urlsafe_b64encode(digest).decode().rstrip("=")


def verify_password(password: str, encoded: str) -> bool:
    try:
        _, rounds, salt_text, digest_text = encoded.split("$")
        salt = base64.urlsafe_b64decode(salt_text + "=" * (-len(salt_text) % 4))
        expected = base64.urlsafe_b64decode(digest_text + "=" * (-len(digest_text) % 4))
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(rounds))
        return hmac.compare_digest(expected, actual)
    except (ValueError, TypeError):
        return False


def encode_segment(value: dict) -> str:
    raw = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def create_token(user_id: int) -> str:
    payload = encode_segment({"sub": str(user_id), "exp": int(time.time()) + 86400})
    signature = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).digest()
    return payload + "." + base64.urlsafe_b64encode(signature).decode().rstrip("=")


def decode_token(token: str) -> int:
    try:
        payload, signature_text = token.split(".")
        expected = hmac.new(SECRET.encode(), payload.encode(), hashlib.sha256).digest()
        actual = base64.urlsafe_b64decode(signature_text + "=" * (-len(signature_text) % 4))
        if not hmac.compare_digest(expected, actual):
            raise ValueError
        raw = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
        data = json.loads(raw)
        if data["exp"] < int(time.time()):
            raise ValueError
        return int(data["sub"])
    except (ValueError, KeyError, json.JSONDecodeError, binascii.Error):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")


def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Autenticação obrigatória.")
    user = db.query(User).filter(User.id == decode_token(credentials.credentials), User.active == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuário inválido.")
    return user


def require_role(*roles: str):
    def guard(user: User = Depends(current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Permissão insuficiente.")
        return user
    return guard
