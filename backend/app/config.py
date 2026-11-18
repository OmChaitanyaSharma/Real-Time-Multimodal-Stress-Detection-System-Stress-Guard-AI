import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME: str = "Real-Time Multimodal Stress Detection and Analysis System"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "btech_cse_stress_detection_secret_key_2026_secured")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'stress_system.db'}")
    
    # Model Artifacts
    SAVED_MODELS_DIR: Path = BASE_DIR / "app" / "ml" / "saved_models"
    DATA_RAW_DIR: Path = BASE_DIR / "data" / "raw"
    DATA_PROCESSED_DIR: Path = BASE_DIR / "data" / "processed"
    
    # CORS Origins (Frontend runs on port 5174, strictly not 5173)
    @property
    def CORS_ORIGINS(self) -> list[str]:
        default_origins = [
            "http://localhost:5555",
            "http://127.0.0.1:5555",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
        custom_origins = os.getenv("BACKEND_CORS_ORIGINS") or os.getenv("CORS_ORIGINS")
        if custom_origins:
            parsed = [o.strip() for o in custom_origins.split(",") if o.strip()]
            return default_origins + parsed
        return default_origins

settings = Settings()
settings.SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
settings.DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
settings.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
