from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.assessment import FacialAnalysisRequest, FacialAnalysisResponse
from app.ml.facial_model import facial_engine
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/facial", tags=["Facial Analysis"])

@router.post("/analyze", response_model=FacialAnalysisResponse)
def analyze_facial_expression(
    request: FacialAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyzes an incoming webcam snapshot frame:
    - Detects face and estimates Eye Aspect Ratio (EAR)
    - Predicts 7 standard emotions (MobileNetV2 / CNN)
    - Computes Grad-CAM explainability heatmap overlay
    - Computes ocular fatigue and facial stress score
    """
    try:
        result = facial_engine.analyze_frame(
            base64_str=request.image_base64,
            client_ear=request.client_ear
        )
        return FacialAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Facial analysis failed: {str(e)}"
        )
