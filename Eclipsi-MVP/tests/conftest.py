import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

TEST_DB = Path(__file__).resolve().parents[1] / "test.db"
os.environ["ECLIPSI_DATABASE_URL"] = f"sqlite:///{TEST_DB.as_posix()}"

from backend.app import app
from backend.database import Base, engine, SessionLocal
from backend.models import ProfessionalProfile, User
from backend.security import hash_password


@pytest.fixture(autouse=True)
def reset_database():
    if TEST_DB.exists():
        TEST_DB.unlink()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    admin = User(name="Admin Teste", email="admin@example.com", password_hash=hash_password("Demo123!"), role="admin")
    professional = User(name="Profissional Teste", email="ana@example.com", password_hash=hash_password("Demo123!"), role="professional")
    patient = User(name="Paciente Teste", email="paciente@example.com", password_hash=hash_password("Demo123!"), role="patient")
    db.add_all([admin, professional, patient])
    db.flush()
    db.add(ProfessionalProfile(user_id=professional.id, registration_number="CRP-EX-001", uf="SP",
                               specialty="Psicologia", approach="TCC",
                               modality="Online", location="Remoto", price="150.00",
                               description="Perfil sintético"))
    db.commit()
    db.close()
    yield
    engine.dispose()
    if TEST_DB.exists():
        TEST_DB.unlink()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def auth(client, email, password="Demo123!"):
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
