import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    res = client.post("/api/auth/login", json={"email": "demo@stressguard.edu", "password": "Demo@123"})
    return res.json()["access_token"]

def test_behavioural_analysis():
    token = get_auth_token()
    payload = {
        "sleep_hours": 7.5,
        "screen_time_hours": 6.0,
        "work_study_hours": 7.0,
        "academic_work_pressure": 2,
        "physical_activity_mins": 45,
        "break_frequency": 4,
        "self_reported_mood": 4,
        "perceived_stress_level": 2
    }
    response = client.post(
        "/api/behavioural/analyze",
        headers={"Authorization": f"Bearer {token}"},
        json=payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_category"] in ["Low", "Moderate", "High"]
    assert 0.0 <= data["stress_score"] <= 1.0
    assert len(data["shap_contributions"]) == 8
    assert "Low" in data["probabilities"]
