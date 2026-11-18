from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict

# Facial analysis request & response
class FacialAnalysisRequest(BaseModel):
    image_base64: str = Field(..., description="JPEG/PNG Base64 encoded camera frame")
    client_ear: Optional[float] = Field(None, description="Client-side computed Eye Aspect Ratio")
    client_blink_rate: Optional[float] = Field(None, description="Client-side detected blinks per minute")

class EmotionDistribution(BaseModel):
    neutral: float
    happy: float
    sad: float
    surprise: float
    fear: float
    disgust: float
    anger: float

class FacialAnalysisResponse(BaseModel):
    face_detected: bool
    dominant_emotion: str
    emotion_probabilities: EmotionDistribution
    eye_aspect_ratio: float
    blink_frequency: Optional[float] = None
    facial_stress_score: float  # 0.0 (calm) to 1.0 (high stress indicator)
    gradcam_base64: Optional[str] = None
    confidence: float
    message: str = "Analysis successful"

# Behavioural questionnaire input & response
class BehaviouralInput(BaseModel):
    sleep_hours: float = Field(..., ge=0.0, le=24.0, description="Average sleep per night in hours")
    screen_time_hours: float = Field(..., ge=0.0, le=24.0, description="Daily screen time in hours")
    work_study_hours: float = Field(..., ge=0.0, le=24.0, description="Daily work/study hours")
    academic_work_pressure: int = Field(..., ge=1, le=5, description="Work/academic pressure (1: low to 5: severe)")
    physical_activity_mins: int = Field(..., ge=0, le=600, description="Exercise/physical activity per day in minutes")
    break_frequency: int = Field(..., ge=1, le=5, description="Break frequency (1: almost never to 5: regular)")
    self_reported_mood: int = Field(..., ge=1, le=5, description="General mood (1: very low to 5: positive)")
    perceived_stress_level: int = Field(..., ge=1, le=5, description="Self perceived stress (1: calm to 5: extreme)")

class ShapFeatureContribution(BaseModel):
    feature: str
    display_name: str
    value: float
    shap_value: float  # Positive increases stress, negative decreases stress

class BehaviouralAnalysisResponse(BaseModel):
    predicted_category: str  # "Low", "Moderate", "High"
    stress_score: float      # 0.0 to 1.0
    probabilities: Dict[str, float]
    shap_contributions: List[ShapFeatureContribution]
    model_used: str = "RandomForest"
    confidence: float

# Multimodal Fusion schemas
class MultimodalEvaluationRequest(BaseModel):
    modality_mode: str = Field("multimodal", description="'multimodal', 'facial_only', or 'behavioural_only'")
    facial_data: Optional[FacialAnalysisRequest] = None
    behavioural_data: Optional[BehaviouralInput] = None
    notes: Optional[str] = None

class RecommendationItem(BaseModel):
    category: str  # "Sleep", "Breaks", "Physical Activity", "Workload", "Mindfulness"
    title: str
    description: str
    priority: str  # "High", "Medium", "Low"

class AssessmentResponse(BaseModel):
    id: Optional[int] = None
    timestamp: datetime
    modality_mode: str
    facial_stress_score: Optional[float] = None
    behavioural_stress_score: Optional[float] = None
    fused_stress_score: float
    stress_category: str  # "Low", "Moderate", "High"
    confidence: float
    modality_weights: Dict[str, float]
    facial_features: Optional[Dict[str, Any]] = None
    behavioural_features: Optional[Dict[str, Any]] = None
    shap_contributions: Optional[List[ShapFeatureContribution]] = None
    gradcam_base64: Optional[str] = None
    recommendations: List[RecommendationItem]
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class AssessmentHistoryItem(BaseModel):
    id: int
    timestamp: datetime
    modality_mode: str
    fused_stress_score: float
    stress_category: str
    confidence: float
    facial_stress_score: Optional[float] = None
    behavioural_stress_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
