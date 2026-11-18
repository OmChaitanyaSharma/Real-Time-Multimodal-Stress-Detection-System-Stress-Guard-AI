import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_login_demo_user():
    response = client.post(
        "/api/auth/login",
        json={"email": "demo@stressguard.edu", "password": "Demo@123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post(
        "/api/auth/login",
        json={"email": "demo@stressguard.edu", "password": "WrongPassword"}
    )
    assert response.status_code == 401
