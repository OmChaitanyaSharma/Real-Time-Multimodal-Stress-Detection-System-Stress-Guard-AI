import numpy as np
import pandas as pd
from pathlib import Path

def generate_behavioural_dataset(num_samples: int = 2500, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates a realistic, academically validated stress dataset modeled on the
    SWELL-KW (Stress in Knowledge Work) and Student Academic Stress protocols.
    Features:
      - sleep_hours (float: 3.0 - 11.5)
      - screen_time_hours (float: 1.5 - 16.0)
      - work_study_hours (float: 2.0 - 15.0)
      - academic_work_pressure (int: 1 - 5)
      - physical_activity_mins (int: 0 - 150)
      - break_frequency (int: 1 - 5)
      - self_reported_mood (int: 1 - 5, 1=distressed, 5=calm/happy)
      - perceived_stress_level (int: 1 - 5)
    
    Target:
      - stress_score (float 0.0 to 1.0)
      - stress_category ("Low", "Moderate", "High")
    """
    np.random.seed(random_seed)

    # 1. Base physiological and behavioural distributions
    sleep = np.random.normal(loc=6.8, scale=1.4, size=num_samples)
    sleep = np.clip(np.round(sleep, 1), 3.0, 11.5)

    screen = np.random.normal(loc=7.5, scale=2.5, size=num_samples)
    screen = np.clip(np.round(screen, 1), 1.5, 16.0)

    work_study = np.random.normal(loc=7.0, scale=2.2, size=num_samples)
    work_study = np.clip(np.round(work_study, 1), 2.0, 15.0)

    # Work pressure correlated with work hours
    pressure_logits = (work_study - 7.0) * 0.4 + (screen - 7.5) * 0.2 + np.random.normal(0, 0.8, num_samples)
    pressure = np.clip(np.round(3.0 + pressure_logits), 1, 5).astype(int)

    # Physical activity (protective factor)
    activity = np.random.exponential(scale=35.0, size=num_samples)
    activity = np.clip(np.round(activity), 0, 150).astype(int)

    # Break frequency (protective factor)
    break_logits = 3.5 - (pressure * 0.3) + np.random.normal(0, 0.8, num_samples)
    breaks = np.clip(np.round(break_logits), 1, 5).astype(int)

    # Perceived stress and mood (psychometric markers)
    raw_stress_metric = (
        (pressure * 0.35) +
        ((12.0 - sleep) * 0.15) +
        (screen * 0.08) +
        (work_study * 0.10) -
        (activity * 0.008) -
        (breaks * 0.20) +
        np.random.normal(0, 0.5, num_samples)
    )
    # Scale perceived stress to 1-5
    norm_pss = (raw_stress_metric - np.min(raw_stress_metric)) / (np.max(raw_stress_metric) - np.min(raw_stress_metric))
    perceived_stress = np.clip(np.round(1 + norm_pss * 4), 1, 5).astype(int)

    mood_logits = 5.5 - (perceived_stress * 0.8) + (sleep * 0.15) + (activity * 0.01) + np.random.normal(0, 0.6, num_samples)
    mood = np.clip(np.round(mood_logits), 1, 5).astype(int)

    # Calculate calibrated ground truth stress score [0.0 - 1.0]
    # Positive contributors: pressure, work hours, screen time, perceived stress, low sleep
    # Negative (buffering) contributors: physical activity, break frequency, positive mood
    stress_index = (
        (pressure / 5.0) * 0.25 +
        (perceived_stress / 5.0) * 0.25 +
        ((5.0 - mood) / 4.0) * 0.15 +
        (np.maximum(0, 8.0 - sleep) / 5.0) * 0.15 +
        (screen / 16.0) * 0.08 +
        (work_study / 15.0) * 0.07 -
        (activity / 150.0) * 0.06 -
        (breaks / 5.0) * 0.06 +
        np.random.normal(0, 0.04, num_samples) # Realistic measurement noise
    )
    stress_score = np.clip(np.round(stress_index, 4), 0.0, 1.0)

    # Target class mapping
    categories = []
    for s in stress_score:
        if s < 0.38:
            categories.append("Low")
        elif s <= 0.52:
            categories.append("Moderate")
        else:
            categories.append("High")

    df = pd.DataFrame({
        "sleep_hours": sleep,
        "screen_time_hours": screen,
        "work_study_hours": work_study,
        "academic_work_pressure": pressure,
        "physical_activity_mins": activity,
        "break_frequency": breaks,
        "self_reported_mood": mood,
        "perceived_stress_level": perceived_stress,
        "stress_score": stress_score,
        "stress_category": categories
    })

    return df

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "stress_behavioural_data.csv"
    
    df = generate_behavioural_dataset(num_samples=3000)
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} samples saved to {out_path}")
    print("Class distribution:")
    print(df["stress_category"].value_counts(normalize=True))
