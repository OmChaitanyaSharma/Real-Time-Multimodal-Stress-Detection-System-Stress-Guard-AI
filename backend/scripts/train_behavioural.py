import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import shap

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, roc_auc_score
)

def run_training():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "processed" / "stress_behavioural_data.csv"
    save_dir = base_dir / "app" / "ml" / "saved_models"
    save_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        print("Data file not found, generating dataset first...")
        from generate_datasets import generate_behavioural_dataset
        df = generate_behavioural_dataset(num_samples=3000)
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)

    feature_cols = [
        "sleep_hours",
        "screen_time_hours",
        "work_study_hours",
        "academic_work_pressure",
        "physical_activity_mins",
        "break_frequency",
        "self_reported_mood",
        "perceived_stress_level"
    ]

    X = df[feature_cols]
    y_raw = df["stress_category"]

    # Label encode classes: Low=0, Moderate=1, High=2
    label_mapping = {"Low": 0, "Moderate": 1, "High": 2}
    inverse_mapping = {0: "Low", 1: "Moderate", 2: "High"}
    y = y_raw.map(label_mapping)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4 Required Models
    models = {
        "RandomForest": RandomForestClassifier(
            n_estimators=150, max_depth=9, min_samples_split=4, random_state=42
        ),
        "XGBoost": XGBClassifier(
            n_estimators=120, max_depth=5, learning_rate=0.08, eval_metric="mlogloss", random_state=42
        ),
        "SupportVectorMachine": SVC(
            kernel="rbf", C=1.5, probability=True, random_state=42
        ),
        "LogisticRegression": LogisticRegression(
            max_iter=1000, C=1.0, random_state=42
        )
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        # 5-fold Cross-validation
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring="accuracy")
        print(f"5-Fold CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

        # Fit on full train set
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_prob = model.predict_proba(X_test_scaled)

        acc = accuracy_score(y_test, y_pred)
        prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_pred, average="macro")
        prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
        cm = confusion_matrix(y_test, y_pred).tolist()

        try:
            auc = roc_auc_score(y_test, y_prob, multi_class="ovr")
        except Exception:
            auc = 0.0

        results[name] = {
            "cv_accuracy_mean": round(float(cv_scores.mean()), 4),
            "cv_accuracy_std": round(float(cv_scores.std()), 4),
            "test_accuracy": round(float(acc), 4),
            "precision_macro": round(float(prec_macro), 4),
            "recall_macro": round(float(rec_macro), 4),
            "f1_macro": round(float(f1_macro), 4),
            "precision_weighted": round(float(prec_weighted), 4),
            "recall_weighted": round(float(rec_weighted), 4),
            "f1_weighted": round(float(f1_weighted), 4),
            "roc_auc": round(float(auc), 4),
            "confusion_matrix": cm,
            "classes": ["Low", "Moderate", "High"]
        }

        print(f"Test Accuracy: {acc:.4f} | F1-Macro: {f1_macro:.4f} | ROC-AUC: {auc:.4f}")

        if f1_macro > best_f1:
            best_f1 = f1_macro
            best_model_name = name

    print(f"\nOptimal Behavioural Model: {best_model_name} (F1-Macro: {best_f1:.4f})")

    # Save artifacts
    best_model = models[best_model_name]
    joblib.dump(best_model, save_dir / "best_behavioural_model.joblib")
    joblib.dump(models["RandomForest"], save_dir / "random_forest_stress.joblib")
    joblib.dump(models["XGBoost"], save_dir / "xgboost_stress.joblib")
    joblib.dump(scaler, save_dir / "scaler.joblib")

    # Fit and save SHAP Explainer
    print("Fitting SHAP TreeExplainer...")
    # Use TreeExplainer on RandomForest
    rf_model = models["RandomForest"]
    explainer = shap.TreeExplainer(rf_model)
    joblib.dump(explainer, save_dir / "shap_explainer.joblib")
    
    # Save a small background reference sample for quick SHAP baseline explanations
    background_sample = X_train_scaled[:100]
    joblib.dump(background_sample, save_dir / "shap_background.joblib")

    metadata = {
        "best_model": best_model_name,
        "feature_columns": feature_cols,
        "label_mapping": label_mapping,
        "inverse_mapping": inverse_mapping,
        "metrics": results
    }

    with open(save_dir / "model_comparison_metrics.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("Model training, comparison and SHAP artifacts successfully saved to:", save_dir)

if __name__ == "__main__":
    run_training()
