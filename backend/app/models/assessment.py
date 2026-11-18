from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    # Modality tracking: "multimodal", "facial_only", "behavioural_only"
    modality_mode = Column(String(50), default="multimodal")
    
    # Raw feature dictionaries
    facial_features = Column(JSON, nullable=True)
    behavioural_features = Column(JSON, nullable=True)
    
    # Stress scores in range [0.0, 1.0]
    facial_stress_score = Column(Float, nullable=True)
    behavioural_stress_score = Column(Float, nullable=True)
    fused_stress_score = Column(Float, nullable=False)
    
    # Classification: "Low", "Moderate", "High"
    stress_category = Column(String(50), nullable=False)
    confidence = Column(Float, default=0.85)
    
    # Explainable AI results
    shap_values = Column(JSON, nullable=True)
    gradcam_image = Column(Text, nullable=True)  # base64 encoded data URI or path
    
    # Recommendations & User notes
    recommendations = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="assessments")
