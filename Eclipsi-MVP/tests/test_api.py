from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models import Appointment, ProfessionalProfile


def test_register_login_duplicate_and_role_guard(client):
    registered = client.post("/api/auth/register", json={
        "name": "Novo Paciente", "email": "novo@example.com", "password": "Seguro123!",
        "role": "patient"
    })
    assert registered.status_code == 201
    login = client.post("/api/auth/login", json={"email": "novo@example.com", "password": "Seguro123!"})
    assert login.status_code == 200
    duplicate = client.post("/api/auth/register", json={
        "name": "Duplicado", "email": "novo@example.com", "password": "Seguro123!",
        "role": "patient"
    })
    assert duplicate.status_code == 409
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    assert client.get("/api/admin/stats", headers=headers).status_code == 403


def test_professional_registration_and_search(client):
    response = client.post("/api/auth/register", json={
        "name": "Prof. Sintético", "email": "prof2@example.com", "password": "Seguro123!",
        "role": "professional", "specialty": "Psicologia", "approach": "Humanista",
        "modality": "Presencial", "location": "Cidade fictícia", "price": "120.00",
        "registration_number": "CRP-EX-002", "uf": "RJ"
    })
    assert response.status_code == 201
    found = client.get("/api/professionals", params={"specialty": "Psico"})
    assert found.status_code == 200
    assert any(p["name"] == "Prof. Sintético" for p in found.json())


def test_appointment_conflict(client):
    from conftest import auth
    headers = auth(client, "paciente@example.com")
    start = datetime.utcnow() + timedelta(days=2)
    end = start + timedelta(minutes=50)
    payload = {"professional_id": 1, "starts_at": start.isoformat(), "ends_at": end.isoformat()}
    first = client.post("/api/appointments", json=payload, headers=headers)
    assert first.status_code == 201
    second = client.post("/api/appointments", json={
        "professional_id": 1,
        "starts_at": (start + timedelta(minutes=10)).isoformat(),
        "ends_at": (end + timedelta(minutes=10)).isoformat()
    }, headers=headers)
    assert second.status_code == 409


def test_records_privacy(client):
    from conftest import auth
    patient_headers = auth(client, "paciente@example.com")
    professional_headers = auth(client, "ana@example.com")
    start = datetime.utcnow() + timedelta(days=3)
    end = start + timedelta(minutes=50)
    appointment = client.post("/api/appointments", json={
        "professional_id": 1, "starts_at": start.isoformat(), "ends_at": end.isoformat()
    }, headers=patient_headers)
    appointment_id = appointment.json()["id"]
    created = client.post("/api/records", json={"appointment_id": appointment_id, "content": "Nota clínica sintética"},
                          headers=professional_headers)
    assert created.status_code == 201
    assert client.get("/api/records", headers=professional_headers).status_code == 200
    assert client.get("/api/records", headers=patient_headers).status_code == 200
    assert client.post("/api/records", json={"appointment_id": appointment_id, "content": "Tentativa indevida"},
                       headers={"Authorization": patient_headers["Authorization"]}).status_code == 403


def test_rating(client):
    from conftest import auth
    patient_headers = auth(client, "paciente@example.com")
    start = datetime.utcnow() + timedelta(days=4)
    appointment = client.post("/api/appointments", json={
        "professional_id": 1, "starts_at": start.isoformat(), "ends_at": (start + timedelta(minutes=50)).isoformat()
    }, headers=patient_headers)
    appointment_id = appointment.json()["id"]
    professional_headers = auth(client, "ana@example.com")
    completed = client.post(f"/api/appointments/{appointment_id}/complete", headers=professional_headers)
    assert completed.status_code == 200
    response = client.post("/api/ratings", json={"appointment_id": appointment_id, "score": 5, "comment": "Sintético"},
                           headers=patient_headers)
    assert response.status_code == 201
    assert response.json()["score"] == 5
    assert client.post("/api/ratings", json={"appointment_id": appointment_id, "score": 4},
                       headers=patient_headers).status_code == 409


def test_earnings_and_admin_stats(client):
    from conftest import auth
    professional_headers = auth(client, "ana@example.com")
    db = SessionLocal()
    profile = db.query(ProfessionalProfile).filter(ProfessionalProfile.user_id == 2).first()
    if profile:
        db.add(Appointment(patient_id=3, professional_id=profile.id,
                           starts_at=datetime.utcnow() - timedelta(days=1),
                           ends_at=datetime.utcnow() - timedelta(days=1) + timedelta(minutes=50),
                           status="completed", price_at_booking="150.00"))
        db.commit()
    db.close()
    earnings = client.get("/api/earnings", headers=professional_headers)
    assert earnings.status_code == 200
    assert earnings.json()["appointments_completed"] == 1
    admin_headers = auth(client, "admin@example.com")
    stats = client.get("/api/admin/stats", headers=admin_headers)
    assert stats.status_code == 200
    assert stats.json()["users"] >= 3
