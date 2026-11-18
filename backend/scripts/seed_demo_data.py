import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.assessment import Assessment
from app.utils.security import get_password_hash

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if demo user exists
        demo_email = "demo@stressguard.edu"
        user = db.query(User).filter(User.email == demo_email).first()
        if not user:
            print("Creating demo user: demo@stressguard.edu / Demo@123")
            user = User(
                email=demo_email,
                full_name="Alex Sharma",
                hashed_password=get_password_hash("Demo@123"),
                is_active=True,
                created_at=datetime.utcnow() - timedelta(days=14)
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            print(f"Demo user already exists with ID: {user.id}")

        # Check existing assessments
        existing_count = db.query(Assessment).filter(Assessment.user_id == user.id).count()
        if existing_count >= 8:
            print(f"User already has {existing_count} assessments, skipping seeding.")
            return

        print("Seeding realistic historical assessments...")
        now = datetime.utcnow()

        # Simulated timeline: Day -14 (Low) -> Day -9 (Moderate) -> Day -5 (High, exam) -> Day -1 (Moderate/Low recovery)
        history_profiles = [
            # Day 14 ago: Low Stress
            {
                "days_ago": 14,
                "mode": "multimodal",
                "fused_score": 0.22,
                "facial_score": 0.20,
                "beh_score": 0.24,
                "category": "Low",
                "confidence": 0.91,
                "emotions": {"happy": 0.65, "neutral": 0.25, "surprise": 0.05, "sad": 0.02, "fear": 0.01, "disgust": 0.01, "anger": 0.01},
                "ear": 0.31,
                "beh": {"sleep_hours": 8.0, "screen_time_hours": 4.5, "work_study_hours": 5.0, "academic_work_pressure": 2, "physical_activity_mins": 60, "break_frequency": 4, "self_reported_mood": 4, "perceived_stress_level": 2},
                "notes": "Weekend rest period, feeling energized."
            },
            # Day 12 ago: Low Stress
            {
                "days_ago": 12,
                "mode": "multimodal",
                "fused_score": 0.28,
                "facial_score": 0.25,
                "beh_score": 0.30,
                "category": "Low",
                "confidence": 0.88,
                "emotions": {"happy": 0.50, "neutral": 0.35, "surprise": 0.08, "sad": 0.03, "fear": 0.01, "disgust": 0.01, "anger": 0.02},
                "ear": 0.29,
                "beh": {"sleep_hours": 7.5, "screen_time_hours": 5.0, "work_study_hours": 6.0, "academic_work_pressure": 2, "physical_activity_mins": 45, "break_frequency": 4, "self_reported_mood": 4, "perceived_stress_level": 2},
                "notes": "Starting project sprint."
            },
            # Day 10 ago: Moderate Stress
            {
                "days_ago": 10,
                "mode": "multimodal",
                "fused_score": 0.44,
                "facial_score": 0.40,
                "beh_score": 0.48,
                "category": "Moderate",
                "confidence": 0.86,
                "emotions": {"neutral": 0.45, "sad": 0.20, "happy": 0.15, "fear": 0.10, "anger": 0.05, "surprise": 0.03, "disgust": 0.02},
                "ear": 0.25,
                "beh": {"sleep_hours": 6.0, "screen_time_hours": 8.0, "work_study_hours": 8.5, "academic_work_pressure": 3, "physical_activity_mins": 20, "break_frequency": 2, "self_reported_mood": 3, "perceived_stress_level": 3},
                "notes": "Lab report deadlines approaching."
            },
            # Day 8 ago: Moderate Stress
            {
                "days_ago": 8,
                "mode": "behavioural_only",
                "fused_score": 0.52,
                "facial_score": None,
                "beh_score": 0.52,
                "category": "Moderate",
                "confidence": 0.85,
                "emotions": None,
                "ear": None,
                "beh": {"sleep_hours": 5.8, "screen_time_hours": 9.5, "work_study_hours": 9.0, "academic_work_pressure": 4, "physical_activity_mins": 15, "break_frequency": 2, "self_reported_mood": 2, "perceived_stress_level": 4},
                "notes": "Questionnaire assessment from library."
            },
            # Day 6 ago: High Stress
            {
                "days_ago": 6,
                "mode": "multimodal",
                "fused_score": 0.76,
                "facial_score": 0.72,
                "beh_score": 0.79,
                "category": "High",
                "confidence": 0.92,
                "emotions": {"anger": 0.35, "fear": 0.25, "sad": 0.20, "neutral": 0.12, "disgust": 0.05, "surprise": 0.02, "happy": 0.01},
                "ear": 0.19,
                "beh": {"sleep_hours": 4.2, "screen_time_hours": 12.0, "work_study_hours": 11.5, "academic_work_pressure": 5, "physical_activity_mins": 0, "break_frequency": 1, "self_reported_mood": 1, "perceived_stress_level": 5},
                "notes": "Night before mid-term presentation."
            },
            # Day 4 ago: High Stress
            {
                "days_ago": 4,
                "mode": "multimodal",
                "fused_score": 0.71,
                "facial_score": 0.68,
                "beh_score": 0.74,
                "category": "High",
                "confidence": 0.89,
                "emotions": {"fear": 0.30, "sad": 0.28, "neutral": 0.20, "anger": 0.12, "disgust": 0.06, "surprise": 0.03, "happy": 0.01},
                "ear": 0.21,
                "beh": {"sleep_hours": 5.0, "screen_time_hours": 11.0, "work_study_hours": 10.0, "academic_work_pressure": 5, "physical_activity_mins": 10, "break_frequency": 2, "self_reported_mood": 2, "perceived_stress_level": 4},
                "notes": "Submitting major project documentation."
            },
            # Day 2 ago: Moderate Stress (Recovery begins)
            {
                "days_ago": 2,
                "mode": "facial_only",
                "fused_score": 0.46,
                "facial_score": 0.46,
                "beh_score": None,
                "category": "Moderate",
                "confidence": 0.84,
                "emotions": {"neutral": 0.50, "happy": 0.22, "sad": 0.15, "surprise": 0.05, "fear": 0.04, "disgust": 0.02, "anger": 0.02},
                "ear": 0.27,
                "beh": None,
                "notes": "Quick webcam check between lectures."
            },
            # Yesterday: Low-Moderate
            {
                "days_ago": 1,
                "mode": "multimodal",
                "fused_score": 0.33,
                "facial_score": 0.30,
                "beh_score": 0.36,
                "category": "Low",
                "confidence": 0.90,
                "emotions": {"happy": 0.45, "neutral": 0.40, "surprise": 0.08, "sad": 0.04, "fear": 0.01, "disgust": 0.01, "anger": 0.01},
                "ear": 0.30,
                "beh": {"sleep_hours": 7.8, "screen_time_hours": 5.5, "work_study_hours": 6.0, "academic_work_pressure": 2, "physical_activity_mins": 40, "break_frequency": 4, "self_reported_mood": 4, "perceived_stress_level": 2},
                "notes": "Post-exam decompression."
            }
        ]

        from app.ml.recommender import generate_recommendations
        from app.ml.behavioural_model import FEATURE_DISPLAY_NAMES

        for prof in history_profiles:
            ts = now - timedelta(days=prof["days_ago"], hours=random.randint(1, 4))
            recs = generate_recommendations(
                stress_category=prof["category"],
                fused_score=prof["fused_score"],
                facial_score=prof["facial_score"],
                ear=prof["ear"],
                behavioural_features=prof["beh"]
            )

            # Build realistic SHAP contributions if behavioural features present
            shap_items = None
            if prof["beh"]:
                b = prof["beh"]
                shap_items = [
                    {"feature": "academic_work_pressure", "display_name": FEATURE_DISPLAY_NAMES["academic_work_pressure"], "value": b["academic_work_pressure"], "shap_value": round((b["academic_work_pressure"] - 2.5) * 0.14, 4)},
                    {"feature": "perceived_stress_level", "display_name": FEATURE_DISPLAY_NAMES["perceived_stress_level"], "value": b["perceived_stress_level"], "shap_value": round((b["perceived_stress_level"] - 2.5) * 0.15, 4)},
                    {"feature": "sleep_hours", "display_name": FEATURE_DISPLAY_NAMES["sleep_hours"], "value": b["sleep_hours"], "shap_value": round((7.0 - b["sleep_hours"]) * 0.09, 4)},
                    {"feature": "screen_time_hours", "display_name": FEATURE_DISPLAY_NAMES["screen_time_hours"], "value": b["screen_time_hours"], "shap_value": round((b["screen_time_hours"] - 6.0) * 0.05, 4)},
                    {"feature": "work_study_hours", "display_name": FEATURE_DISPLAY_NAMES["work_study_hours"], "value": b["work_study_hours"], "shap_value": round((b["work_study_hours"] - 6.0) * 0.04, 4)},
                    {"feature": "self_reported_mood", "display_name": FEATURE_DISPLAY_NAMES["self_reported_mood"], "value": b["self_reported_mood"], "shap_value": round((3.0 - b["self_reported_mood"]) * 0.08, 4)},
                    {"feature": "break_frequency", "display_name": FEATURE_DISPLAY_NAMES["break_frequency"], "value": b["break_frequency"], "shap_value": round((3.0 - b["break_frequency"]) * 0.05, 4)},
                    {"feature": "physical_activity_mins", "display_name": FEATURE_DISPLAY_NAMES["physical_activity_mins"], "value": b["physical_activity_mins"], "shap_value": round((30.0 - b["physical_activity_mins"]) * 0.003, 4)},
                ]
                shap_items.sort(key=lambda s: abs(s["shap_value"]), reverse=True)

            facial_data = None
            if prof["facial_score"] is not None:
                facial_data = {
                    "face_detected": True,
                    "dominant_emotion": max(prof["emotions"], key=prof["emotions"].get),
                    "emotion_probabilities": prof["emotions"],
                    "eye_aspect_ratio": prof["ear"],
                    "facial_stress_score": prof["facial_score"],
                    "confidence": prof["confidence"]
                }

            assessment = Assessment(
                user_id=user.id,
                timestamp=ts,
                modality_mode=prof["mode"],
                facial_features=facial_data,
                behavioural_features=prof["beh"],
                facial_stress_score=prof["facial_score"],
                behavioural_stress_score=prof["beh_score"],
                fused_stress_score=prof["fused_score"],
                stress_category=prof["category"],
                confidence=prof["confidence"],
                shap_values=shap_items,
                gradcam_image=None,
                recommendations=[r.model_dump() for r in recs],
                notes=prof["notes"]
            )
            db.add(assessment)

        db.commit()
        print("Successfully seeded 8 historical assessments for Alex Sharma!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
