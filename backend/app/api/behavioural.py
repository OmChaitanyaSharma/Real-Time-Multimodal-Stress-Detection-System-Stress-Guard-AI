from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.assessment import BehaviouralInput, BehaviouralAnalysisResponse
from app.ml.behavioural_model import behavioural_engine
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/behavioural", tags=["Behavioural Analysis"])

@router.post("/analyze", response_model=BehaviouralAnalysisResponse)
def analyze_behaviour(
    input_data: BehaviouralInput,
    current_user: User = Depends(get_current_user)
):
    """
    Analyzes self-reported lifestyle metrics:
    - Sleep, screen time, workload, pressure, physical activity, breaks, mood
    - Runs inference via trained Random Forest ML model
    - Computes SHAP feature importance attributions
    """
    try:
        result = behavioural_engine.predict(input_data)
        return BehaviouralAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Behavioural analysis failed: {str(e)}"
        )
