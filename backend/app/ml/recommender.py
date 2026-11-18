from typing import List, Dict, Any, Optional
from app.schemas.assessment import RecommendationItem

def generate_recommendations(
    stress_category: str,
    fused_score: float,
    facial_score: Optional[float] = None,
    ear: Optional[float] = None,
    behavioural_features: Optional[Dict[str, Any]] = None
) -> List[RecommendationItem]:
    """
    Generates non-diagnostic, supportive wellness recommendations
    tailored to specific detected facial fatigue and self-reported lifestyle stressors.
    """
    recommendations: List[RecommendationItem] = []

    # Category 1: Sleep Optimization
    if behavioural_features:
        sleep = behavioural_features.get("sleep_hours", 7.0)
        if sleep < 6.0:
            recommendations.append(RecommendationItem(
                category="Sleep",
                title="Consistent Sleep Opportunity Window",
                description=(
                    f"Your reported sleep duration of {sleep:.1f} hours is below the recommended 7-9 hours. "
                    "Establish a fixed 30-minute pre-bed wind-down routine without screens to promote restorative slow-wave sleep."
                ),
                priority="High" if sleep < 5.0 else "Medium"
            ))
        elif sleep > 10.0:
            recommendations.append(RecommendationItem(
                category="Sleep",
                title="Circadian Rhythm Alignment",
                description=(
                    "Excessive sleep duration can sometimes indicate accumulated exhaustion or disrupted sleep architecture. "
                    "Aim for morning natural sunlight exposure within 20 minutes of waking."
                ),
                priority="Low"
            ))

    # Category 2: Screen Time & Ocular Rest (incorporates EAR and Screen Time)
    screen_time = behavioural_features.get("screen_time_hours", 6.0) if behavioural_features else 6.0
    if screen_time >= 8.0 or (ear is not None and ear < 0.23):
        ear_str = f"{ear:.2f}" if ear is not None else "N/A"
        recommendations.append(RecommendationItem(
            category="Breaks",
            title="Implement the 20-20-20 Rule",
            description=(
                f"With {screen_time:.1f} hours of daily screen time and observable ocular strain (EAR: {ear_str}), "
                "every 20 minutes look at an object 20 feet away for at least 20 seconds to alleviate ciliary muscle tension."
            ),
            priority="High" if screen_time >= 10.0 else "Medium"
        ))

    # Category 3: Break Frequency & Workload Distribution
    if behavioural_features:
        breaks = behavioural_features.get("break_frequency", 3)
        pressure = behavioural_features.get("academic_work_pressure", 3)
        work_hours = behavioural_features.get("work_study_hours", 6.0)

        if breaks <= 2 or work_hours > 8.0:
            recommendations.append(RecommendationItem(
                category="Workload",
                title="Structured Interval Pacing (Pomodoro Technique)",
                description=(
                    "Continuous long work sessions without regular pauses increase cognitive fatigue. "
                    "Try working in 45-50 minute focused blocks separated by 5-10 minute complete mental disconnects."
                ),
                priority="High" if pressure >= 4 else "Medium"
            ))

        if pressure >= 4:
            recommendations.append(RecommendationItem(
                category="Workload",
                title="Cognitive Offloading & Task Chunking",
                description=(
                    "High subjective academic/work pressure detected. Break large upcoming milestones into atomic sub-tasks "
                    "using the Eisenhower Matrix (urgent vs. important) to reduce executive overwhelm."
                ),
                priority="High"
            ))

    # Category 4: Physical Activity
    if behavioural_features:
        activity = behavioural_features.get("physical_activity_mins", 30)
        if activity < 20:
            recommendations.append(RecommendationItem(
                category="Physical Activity",
                title="Brisk Aerobic Movement or Stretching",
                description=(
                    "Light physical activity (even a 15-minute brisk walk) naturally reduces circulating cortisol "
                    "and stimulates endorphin release to buffer against stress accumulation."
                ),
                priority="Medium"
            ))

    # Category 5: Acute Stress De-escalation (Mindfulness & Breathing)
    if stress_category in ["Moderate", "High"] or (facial_score is not None and facial_score > 0.60):
        recommendations.append(RecommendationItem(
            category="Mindfulness",
            title="Physiological Sigh / Box Breathing",
            description=(
                "Practice 2-3 minutes of the 'Physiological Sigh': two quick consecutive inhales through the nose, "
                "followed by one extended, unhurried exhale through the mouth to rapidly lower autonomic heart rate."
            ),
            priority="High" if stress_category == "High" else "Medium"
        ))

    # Category 6: Social & Academic Support
    if stress_category == "High":
        recommendations.append(RecommendationItem(
            category="Support",
            title="Reach Out to Your Academic or Peer Support Network",
            description=(
                "Persistently elevated stress indicators suggest you may benefit from external perspective. "
                "Consider discussing workload distribution with a faculty mentor, academic advisor, or counselor."
            ),
            priority="High"
        ))

    # Baseline maintenance recommendation if stress is Low
    if stress_category == "Low" and len(recommendations) == 0:
        recommendations.append(RecommendationItem(
            category="Mindfulness",
            title="Sustain Your Current Equilibrium",
            description=(
                "Your observable facial and behavioural indicators reflect a balanced state. "
                "Continue maintaining your positive sleep hygiene, active physical routine, and regular breaks."
            ),
            priority="Low"
        ))

    return recommendations
