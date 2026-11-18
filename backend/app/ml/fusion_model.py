from typing import Dict, Any, Optional, Tuple

class MultimodalFusionEngine:
    """
    Multimodal Stress Fusion Engine.
    Combines visual indicators (facial expression probabilities, Eye Aspect Ratio / EAR)
    with self-reported lifestyle metrics (sleep, workload, screen time, physical activity).
    
    Provides:
    1. Weighted Soft Voting based on modality data quality.
    2. Dynamic Fallback for missing modalities (facial-only or behavioural-only).
    3. Dissonance / Masked-Stress Detection (e.g. smiling face under extreme workload).
    """

    def __init__(self):
        # Calibrated stress category thresholds
        self.LOW_THRESHOLD = 0.38
        self.HIGH_THRESHOLD = 0.52

    def calculate_facial_stress_score(
        self,
        emotion_probs: Dict[str, float],
        ear: float,
        blink_rate: Optional[float] = None
    ) -> Tuple[float, float]:
        """
        Derives an academic facial stress score from validated emotion valence/arousal weights
        and ocular fatigue indicators (EAR).
        Returns: (facial_stress_score [0..1], facial_confidence [0..1])
        """
        # Academic valence-arousal stress weights for 7 standard emotions
        # High arousal + negative valence = strong stress indicator
        anger = emotion_probs.get("anger", 0.0)
        fear = emotion_probs.get("fear", 0.0)
        disgust = emotion_probs.get("disgust", 0.0)
        sadness = emotion_probs.get("sad", 0.0)
        neutral = emotion_probs.get("neutral", 0.0)
        surprise = emotion_probs.get("surprise", 0.0)
        happy = emotion_probs.get("happy", 0.0)

        # Negative emotions heavily weight toward stress
        emotion_stress_component = (
            (anger * 0.95) +
            (fear * 0.90) +
            (sadness * 0.70) +
            (disgust * 0.75) +
            (surprise * 0.30) +
            (neutral * 0.15) +
            (happy * 0.02)
        )

        # Ocular fatigue modulation from Eye Aspect Ratio (EAR)
        # Nominal relaxed open eye EAR is ~0.28 to 0.35.
        # Prolonged drooping (EAR < 0.22) indicates drowsiness/eyestrain.
        # Excessive squinting / tension (EAR < 0.20) or erratic blinks elevate strain.
        ear_strain = 0.0
        if ear < 0.22:
            ear_strain = min(0.35, (0.22 - ear) * 2.5)
        elif ear > 0.38:
            # Wide-eyed tension (hyper-vigilance)
            ear_strain = min(0.20, (ear - 0.38) * 1.5)

        raw_facial_score = (0.75 * emotion_stress_component) + (0.25 * ear_strain)
        facial_stress_score = float(max(0.0, min(1.0, raw_facial_score)))

        # Facial confidence based on emotion peak certainty
        max_prob = max(emotion_probs.values()) if emotion_probs else 0.5
        facial_confidence = float(min(0.98, max(0.60, max_prob + 0.15)))

        return facial_stress_score, facial_confidence

    def fuse(
        self,
        facial_score: Optional[float] = None,
        facial_conf: Optional[float] = None,
        behavioural_score: Optional[float] = None,
        behavioural_conf: Optional[float] = None,
        requested_mode: str = "multimodal"
    ) -> Dict[str, Any]:
        """
        Executes multimodal fusion with automatic missing-modality handling.
        """
        has_facial = facial_score is not None
        has_beh = behavioural_score is not None

        # Mode fallback checks
        if not has_facial and not has_beh:
            raise ValueError("At least one modality (facial or behavioural) must be provided.")

        if has_facial and not has_beh:
            effective_mode = "facial_only"
            fused_score = facial_score
            confidence = facial_conf or 0.80
            weights = {"facial": 1.0, "behavioural": 0.0}
        elif has_beh and not has_facial:
            effective_mode = "behavioural_only"
            fused_score = behavioural_score
            confidence = behavioural_conf or 0.85
            weights = {"facial": 0.0, "behavioural": 1.0}
        else:
            effective_mode = "multimodal"
            f_conf = facial_conf if facial_conf else 0.80
            b_conf = behavioural_conf if behavioural_conf else 0.85

            # Dynamic confidence weighting
            total_conf = f_conf + b_conf
            if total_conf <= 0:
                w_face = 0.5
                w_beh = 0.5
            else:
                w_face = f_conf / total_conf
                w_beh = b_conf / total_conf

            # Dissonance check: "Smiling depression" / Masked stress scenario
            # If behavioural lifestyle indicators indicate high chronic strain
            # (e.g. sleep < 4 hrs, pressure=5, work=14 hrs -> beh_score > 0.70)
            # but face shows momentary smile/neutral (facial_score < 0.25),
            # reweight to prevent false negative masking.
            if behavioural_score > 0.70 and facial_score < 0.25:
                w_beh = 0.75
                w_face = 0.25
                dissonance_flag = True
            else:
                dissonance_flag = False

            fused_score = (w_face * facial_score) + (w_beh * behavioural_score)
            confidence = (w_face * f_conf) + (w_beh * b_conf)
            weights = {
                "facial": round(float(w_face), 3),
                "behavioural": round(float(w_beh), 3)
            }

        fused_score = float(max(0.0, min(1.0, fused_score)))

        # Classification into 3 distinct indicator levels
        if fused_score < self.LOW_THRESHOLD:
            category = "Low"
        elif fused_score <= self.HIGH_THRESHOLD:
            category = "Moderate"
        else:
            category = "High"

        return {
            "effective_mode": effective_mode,
            "fused_stress_score": round(fused_score, 4),
            "stress_category": category,
            "confidence": round(float(confidence), 3),
            "modality_weights": weights,
            "facial_stress_score": round(float(facial_score), 4) if facial_score is not None else None,
            "behavioural_stress_score": round(float(behavioural_score), 4) if behavioural_score is not None else None,
        }

fusion_engine = MultimodalFusionEngine()
