from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.assessment import Assessment
from app.schemas.assessment import MultimodalEvaluationRequest, AssessmentResponse, ShapFeatureContribution
from app.ml.facial_model import facial_engine
from app.ml.behavioural_model import behavioural_engine
from app.ml.fusion_model import fusion_engine
from app.ml.recommender import generate_recommendations
from app.utils.security import get_current_user

router = APIRouter(prefix="/fusion", tags=["Multimodal Fusion"])

@router.post("/evaluate", response_model=AssessmentResponse)
def evaluate_multimodal_stress(
    request: MultimodalEvaluationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Evaluates multimodal stress indicators:
    - Ingests facial snapshot (if enabled)
    - Ingests behavioural lifestyle survey (if completed)
    - Dynamically balances modalities using weighted soft voting
    - Evaluates missing modality gracefully
    - Attaches SHAP and Grad-CAM explanations
    - Produces personalized, non-diagnostic wellness recommendations
    - Saves historical assessment to database
    """
    facial_res = None
    facial_score = None
    facial_conf = None
    gradcam_b64 = None
    ear_val = None

    if request.facial_data and request.facial_data.image_base64:
        try:
            facial_res = facial_engine.analyze_frame(
                base64_str=request.facial_data.image_base64,
                client_ear=request.facial_data.client_ear
            )
            # Only incorporate facial metrics into fusion if a face was detected
            if facial_res.get("face_detected", False):
                facial_score = facial_res["facial_stress_score"]
                facial_conf = facial_res["confidence"]
                gradcam_b64 = facial_res.get("gradcam_base64")
                ear_val = facial_res.get("eye_aspect_ratio")
            else:
                facial_score = None
                facial_conf = None
        except Exception as e:
            print(f"Facial analysis error in fusion: {e}")

    beh_res = None
    beh_score = None
    beh_conf = None
    shap_items = None
    beh_dict = None

    if request.behavioural_data:
        try:
            beh_res = behavioural_engine.predict(request.behavioural_data)
            beh_score = beh_res["stress_score"]
            beh_conf = beh_res["confidence"]
            shap_items = [ShapFeatureContribution(**s) for s in beh_res["shap_contributions"]]
            beh_dict = request.behavioural_data.model_dump()
        except Exception as e:
            print(f"Behavioural analysis error in fusion: {e}")

    if facial_score is None and beh_score is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Neither facial nor behavioural data could be analyzed. At least one valid modality is required."
        )

    # Perform multimodal fusion
    fusion_result = fusion_engine.fuse(
        facial_score=facial_score,
        facial_conf=facial_conf,
        behavioural_score=beh_score,
        behavioural_conf=beh_conf,
        requested_mode=request.modality_mode
    )

    fused_score = fusion_result["fused_stress_score"]
    stress_cat = fusion_result["stress_category"]
    confidence = fusion_result["confidence"]
    weights = fusion_result["modality_weights"]
    effective_mode = fusion_result["effective_mode"]

    # Generate supportive lifestyle recommendations
    recs = generate_recommendations(
        stress_category=stress_cat,
        fused_score=fused_score,
        facial_score=facial_score,
        ear=ear_val,
        behavioural_features=beh_dict
    )

    # Save to database
    assessment = Assessment(
        user_id=current_user.id,
        timestamp=datetime.now(timezone.utc),
        modality_mode=effective_mode,
        facial_features=facial_res,
        behavioural_features=beh_dict,
        facial_stress_score=facial_score,
        behavioural_stress_score=beh_score,
        fused_stress_score=fused_score,
        stress_category=stress_cat,
        confidence=confidence,
        shap_values=[s.model_dump() for s in shap_items] if shap_items else None,
        gradcam_image=gradcam_b64,
        recommendations=[r.model_dump() for r in recs],
        notes=request.notes
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return AssessmentResponse(
        id=assessment.id,
        timestamp=assessment.timestamp,
        modality_mode=effective_mode,
        facial_stress_score=facial_score,
        behavioural_stress_score=beh_score,
        fused_stress_score=fused_score,
        stress_category=stress_cat,
        confidence=confidence,
        modality_weights=weights,
        facial_features=facial_res,
        behavioural_features=beh_dict,
        shap_contributions=shap_items,
        gradcam_base64=gradcam_b64,
        recommendations=recs,
        notes=request.notes
    )
