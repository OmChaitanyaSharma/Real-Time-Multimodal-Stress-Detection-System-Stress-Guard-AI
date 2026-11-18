import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    res = client.post("/api/auth/login", json={"email": "demo@stressguard.edu", "password": "Demo@123"})
    return res.json()["access_token"]

def test_multimodal_evaluation_behavioural_only():
    token = get_auth_token()
    payload = {
        "modality_mode": "behavioural_only",
        "behavioural_data": {
            "sleep_hours": 4.5,
            "screen_time_hours": 11.0,
            "work_study_hours": 10.0,
            "academic_work_pressure": 5,
            "physical_activity_mins": 0,
            "break_frequency": 1,
            "self_reported_mood": 1,
            "perceived_stress_level": 5
        },
        "notes": "Test severe workload assessment"
    }
    response = client.post(
        "/api/fusion/evaluate",
        headers={"Authorization": f"Bearer {token}"},
        json=payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["stress_category"] in ["Moderate", "High"]
    assert data["fused_stress_score"] > 0.40
    assert len(data["recommendations"]) > 0
    assert data["modality_mode"] == "behavioural_only"

def test_history_trends():
    token = get_auth_token()
    response = client.get(
        "/api/history/trends",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    trends = response.json()
    assert isinstance(trends, list)
    assert len(trends) >= 1
    assert "fused_stress_score" in trends[0]

def test_get_latest_assessment():
    token = get_auth_token()
    response = client.get(
        "/api/history/latest",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "fused_stress_score" in data
    assert "stress_category" in data
    assert "modality_mode" in data

def test_covered_frame_fallback_in_multimodal():
    """
    When multimodal mode receives an empty/blank frame where no face is detected,
    it must gracefully fall back to behavioural-only without crashing.
    """
    token = get_auth_token()
    # 1x1 black pixel base64 image
    blank_pixel_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    payload = {
        "modality_mode": "multimodal",
        "facial_data": {
            "image_base64": blank_pixel_base64
        },
        "behavioural_data": {
            "sleep_hours": 7.5,
            "screen_time_hours": 6.0,
            "work_study_hours": 6.5,
            "academic_work_pressure": 2,
            "physical_activity_mins": 45,
            "break_frequency": 4,
            "self_reported_mood": 4,
            "perceived_stress_level": 2
        }
    }
    response = client.post(
        "/api/fusion/evaluate",
        headers={"Authorization": f"Bearer {token}"},
        json=payload
    )
    assert response.status_code == 200
    data = response.json()
    # It must have fallen back to behavioural_only because the blank pixel has no face
    assert data["modality_mode"] == "behavioural_only"
    assert data["stress_category"] in ["Low", "Moderate"]

def test_security_headers_present():
    """
    Verifies that security headers (nosniff, DENY, etc.) are attached by middleware.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert "strict-origin-when-cross-origin" in response.headers.get("Referrer-Policy", "")
    assert "camera=(self)" in response.headers.get("Permissions-Policy", "")

def test_bola_cross_tenant_isolation():
    """
    Shannon BOLA / IDOR Vector:
    User B should not be able to query User A's private assessment ID.
    """
    # 1. Register a temporary user B with unique email
    user_b_email = f"attacker_{uuid.uuid4().hex[:8]}@stressguard.edu"
    client.post("/api/auth/register", json={
        "email": user_b_email,
        "full_name": "Adversary Audit",
        "password": "Password@123"
    })
    res_b = client.post("/api/auth/login", json={"email": user_b_email, "password": "Password@123"})
    token_b = res_b.json()["access_token"]

    # 2. Get User A (Demo user) assessment list
    token_a = get_auth_token()
    res_a = client.get("/api/history", headers={"Authorization": f"Bearer {token_a}"})
    demo_assessments = res_a.json()
    assert len(demo_assessments) > 0
    target_assessment_id = demo_assessments[0]["id"]

    # 3. User B attempts to access User A's assessment
    idor_attempt = client.get(
        f"/api/history/{target_assessment_id}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    # Must return 404 (or 403), never leaking User A's data
    assert idor_attempt.status_code in [404, 403]

def test_decompression_bomb_payload_mitigation():
    """
    Shannon DoS Vector:
    An oversized base64 payload (>6MB) must be neutralized cleanly without OOM crash.
    """
    token = get_auth_token()
    # 7MB oversized dummy payload
    oversized_payload = "A" * (7 * 1024 * 1024)
    res = client.post(
        "/api/facial/analyze",
        headers={"Authorization": f"Bearer {token}"},
        json={"image_base64": f"data:image/jpeg;base64,{oversized_payload}"}
    )
    assert res.status_code == 200
    data = res.json()
    # Image decoding fails safely and returns face_detected: False
    assert data["face_detected"] is False

def test_unauthenticated_request_blocked():
    """
    Shannon Auth Gate:
    Protected endpoints reject unauthenticated access with 401.
    """
    res = client.get("/api/history")
    assert res.status_code == 401
