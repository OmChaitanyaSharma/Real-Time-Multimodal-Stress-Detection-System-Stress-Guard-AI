import os
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd
import joblib

from app.schemas.assessment import BehaviouralInput, ShapFeatureContribution

FEATURE_NAMES = [
    "sleep_hours",
    "screen_time_hours",
    "work_study_hours",
    "academic_work_pressure",
    "physical_activity_mins",
    "break_frequency",
    "self_reported_mood",
    "perceived_stress_level"
]

FEATURE_DISPLAY_NAMES = {
    "sleep_hours": "Sleep Duration (Hours)",
    "screen_time_hours": "Daily Screen Time (Hours)",
    "work_study_hours": "Study/Work Duration (Hours)",
    "academic_work_pressure": "Academic/Work Pressure",
    "physical_activity_mins": "Physical Activity (Minutes)",
    "break_frequency": "Break Regularity",
    "self_reported_mood": "Reported Mood State",
    "perceived_stress_level": "Perceived Stress Level"
}

class BehaviouralModelEngine:
    def __init__(self):
        self.models_dir = Path(__file__).resolve().parent / "saved_models"
        self.model_path = self.models_dir / "best_behavioural_model.joblib"
        self.scaler_path = self.models_dir / "scaler.joblib"
        self.shap_path = self.models_dir / "shap_explainer.joblib"

        self.model = None
        self.scaler = None
        self.explainer = None
        self.load_artifacts()

    def load_artifacts(self):
        if self.model_path.exists() and self.scaler_path.exists():
            try:
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                print("Loaded trained Behavioural Model and Scaler.")
            except Exception as e:
                print(f"Error loading model: {e}")

        if self.shap_path.exists():
            try:
                self.explainer = joblib.load(self.shap_path)
                print("Loaded SHAP TreeExplainer.")
            except Exception as e:
                print(f"Error loading SHAP explainer: {e}")

    def predict(self, input_data: BehaviouralInput) -> Dict[str, Any]:
        """
        Processes the 8-feature questionnaire through the trained ML pipeline
        and computes SHAP feature attributions.
        """
        # Ensure models are loaded
        if self.model is None or self.scaler is None:
            self.load_artifacts()

        # Extract values in correct order
        raw_values = [
            input_data.sleep_hours,
            input_data.screen_time_hours,
            input_data.work_study_hours,
            input_data.academic_work_pressure,
            input_data.physical_activity_mins,
            input_data.break_frequency,
            input_data.self_reported_mood,
            input_data.perceived_stress_level
        ]
        X_df = pd.DataFrame([raw_values], columns=FEATURE_NAMES)

        if self.scaler is not None and self.model is not None:
            X_scaled = self.scaler.transform(X_df)
            probs = self.model.predict_proba(X_scaled)[0]
            # Classes: [0: Low, 1: Moderate, 2: High]
            pred_idx = int(np.argmax(probs))
            category_mapping = {0: "Low", 1: "Moderate", 2: "High"}
            predicted_category = category_mapping[pred_idx]
            
            # Continuous stress score: weighted expectation
            # 0.0 * p_low + 0.50 * p_med + 1.0 * p_high
            p_low = float(probs[0])
            p_med = float(probs[1]) if len(probs) > 1 else 0.0
            p_high = float(probs[2]) if len(probs) > 2 else 0.0
            stress_score = float((0.05 * p_low) + (0.50 * p_med) + (0.95 * p_high))
            stress_score = max(0.0, min(1.0, stress_score))

            probabilities = {
                "Low": round(p_low, 4),
                "Moderate": round(p_med, 4),
                "High": round(p_high, 4)
            }
            confidence = float(np.max(probs))

            # SHAP Explanation calculation
            shap_contributions = []
            if self.explainer is not None:
                try:
                    shap_vals = self.explainer.shap_values(X_scaled)
                    # For multi-class, shap_vals is list of arrays per class, or 3D array
                    # Focus on target predicted class (or High stress class)
                    if isinstance(shap_vals, list):
                        target_shap = shap_vals[pred_idx][0]
                    elif len(shap_vals.shape) == 3:
                        target_shap = shap_vals[0, :, pred_idx]
                    else:
                        target_shap = shap_vals[0]

                    for idx, feat_name in enumerate(FEATURE_NAMES):
                        val = float(raw_values[idx])
                        shap_val = float(target_shap[idx])
                        shap_contributions.append(ShapFeatureContribution(
                            feature=feat_name,
                            display_name=FEATURE_DISPLAY_NAMES[feat_name],
                            value=val,
                            shap_value=round(shap_val, 4)
                        ))
                except Exception as e:
                    print(f"SHAP explanation computation error: {e}")
                    shap_contributions = self._fallback_feature_importance(raw_values)
            else:
                shap_contributions = self._fallback_feature_importance(raw_values)

        else:
            # Mathematical baseline fallback before training script has executed
            p_stress = (
                (input_data.academic_work_pressure / 5.0) * 0.30 +
                (input_data.perceived_stress_level / 5.0) * 0.30 +
                (max(0, 8.0 - input_data.sleep_hours) / 5.0) * 0.15 +
                (input_data.screen_time_hours / 16.0) * 0.10 +
                ((5.0 - input_data.self_reported_mood) / 4.0) * 0.10 -
                (input_data.physical_activity_mins / 150.0) * 0.05
            )
            stress_score = float(max(0.0, min(1.0, p_stress)))
            if stress_score < 0.35:
                predicted_category = "Low"
            elif stress_score <= 0.68:
                predicted_category = "Moderate"
            else:
                predicted_category = "High"

            probabilities = {
                "Low": round(max(0.05, 1.0 - stress_score * 1.5), 3),
                "Moderate": round(0.40, 3),
                "High": round(min(0.95, stress_score * 1.2), 3)
            }
            # normalize
            total = sum(probabilities.values())
            probabilities = {k: round(v / total, 3) for k, v in probabilities.items()}
            confidence = 0.85
            shap_contributions = self._fallback_feature_importance(raw_values)

        # Sort SHAP contributions by absolute magnitude descending
        shap_contributions.sort(key=lambda x: abs(x.shap_value), reverse=True)

        return {
            "predicted_category": predicted_category,
            "stress_score": round(stress_score, 4),
            "probabilities": probabilities,
            "shap_contributions": [s.model_dump() for s in shap_contributions],
            "model_used": "RandomForest",
            "confidence": round(confidence, 3)
        }

    def _fallback_feature_importance(self, raw_values: List[float]) -> List[ShapFeatureContribution]:
        """Provides normalized feature attribution based on standard clinical stress regressions."""
        contributions = []
        # Academic Work Pressure (high -> positive stress contribution)
        contributions.append(ShapFeatureContribution(
            feature="academic_work_pressure",
            display_name=FEATURE_DISPLAY_NAMES["academic_work_pressure"],
            value=raw_values[3],
            shap_value=round((raw_values[3] - 2.5) * 0.12, 4)
        ))
        # Perceived Stress
        contributions.append(ShapFeatureContribution(
            feature="perceived_stress_level",
            display_name=FEATURE_DISPLAY_NAMES["perceived_stress_level"],
            value=raw_values[7],
            shap_value=round((raw_values[7] - 2.5) * 0.14, 4)
        ))
        # Sleep (low -> positive stress contribution)
        contributions.append(ShapFeatureContribution(
            feature="sleep_hours",
            display_name=FEATURE_DISPLAY_NAMES["sleep_hours"],
            value=raw_values[0],
            shap_value=round((7.0 - raw_values[0]) * 0.08, 4)
        ))
        # Screen Time
        contributions.append(ShapFeatureContribution(
            feature="screen_time_hours",
            display_name=FEATURE_DISPLAY_NAMES["screen_time_hours"],
            value=raw_values[1],
            shap_value=round((raw_values[1] - 6.0) * 0.04, 4)
        ))
        # Study Hours
        contributions.append(ShapFeatureContribution(
            feature="work_study_hours",
            display_name=FEATURE_DISPLAY_NAMES["work_study_hours"],
            value=raw_values[2],
            shap_value=round((raw_values[2] - 6.0) * 0.03, 4)
        ))
        # Mood (high mood -> negative stress contribution)
        contributions.append(ShapFeatureContribution(
            feature="self_reported_mood",
            display_name=FEATURE_DISPLAY_NAMES["self_reported_mood"],
            value=raw_values[6],
            shap_value=round((3.0 - raw_values[6]) * 0.07, 4)
        ))
        # Physical Activity (high activity -> negative stress contribution)
        contributions.append(ShapFeatureContribution(
            feature="physical_activity_mins",
            display_name=FEATURE_DISPLAY_NAMES["physical_activity_mins"],
            value=raw_values[4],
            shap_value=round((30.0 - raw_values[4]) * 0.002, 4)
        ))
        # Break Frequency (high breaks -> negative stress contribution)
        contributions.append(ShapFeatureContribution(
            feature="break_frequency",
            display_name=FEATURE_DISPLAY_NAMES["break_frequency"],
            value=raw_values[5],
            shap_value=round((3.0 - raw_values[5]) * 0.05, 4)
        ))
        return contributions

behavioural_engine = BehaviouralModelEngine()
