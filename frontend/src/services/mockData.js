// Client-Side Autonomous Demo Fallback Data & Computation
// Ensures 100% functionality on Vercel preview environments even without a live Python backend.

export const BENCHMARKS_DATA = {
  best_model: "SupportVectorMachine",
  feature_columns: [
    "sleep_hours",
    "screen_time_hours",
    "work_study_hours",
    "academic_work_pressure",
    "physical_activity_mins",
    "break_frequency",
    "self_reported_mood",
    "perceived_stress_level"
  ],
  label_mapping: { "Low": 0, "Moderate": 1, "High": 2 },
  inverse_mapping: { "0": "Low", "1": "Moderate", "2": "High" },
  metrics: {
    RandomForest: {
      cv_accuracy_mean: 0.8325,
      cv_accuracy_std: 0.0081,
      test_accuracy: 0.8083,
      precision_macro: 0.804,
      recall_macro: 0.8011,
      f1_macro: 0.8025,
      precision_weighted: 0.8075,
      recall_weighted: 0.8083,
      f1_weighted: 0.8079,
      roc_auc: 0.9482,
      confusion_matrix: [[243, 34, 0], [39, 140, 20], [0, 22, 102]],
      classes: ["Low", "Moderate", "High"]
    },
    XGBoost: {
      cv_accuracy_mean: 0.8279,
      cv_accuracy_std: 0.0081,
      test_accuracy: 0.8317,
      precision_macro: 0.828,
      recall_macro: 0.8207,
      f1_macro: 0.8242,
      precision_weighted: 0.8316,
      recall_weighted: 0.8317,
      f1_weighted: 0.8315,
      roc_auc: 0.9514,
      confusion_matrix: [[249, 28, 0], [33, 149, 17], [0, 23, 101]],
      classes: ["Low", "Moderate", "High"]
    },
    SupportVectorMachine: {
      cv_accuracy_mean: 0.8358,
      cv_accuracy_std: 0.009,
      test_accuracy: 0.8367,
      precision_macro: 0.8352,
      recall_macro: 0.8258,
      f1_macro: 0.8301,
      precision_weighted: 0.8374,
      recall_weighted: 0.8367,
      f1_weighted: 0.8368,
      roc_auc: 0.9562,
      confusion_matrix: [[249, 28, 0], [32, 152, 15], [0, 23, 101]],
      classes: ["Low", "Moderate", "High"]
    },
    LogisticRegression: {
      cv_accuracy_mean: 0.8433,
      cv_accuracy_std: 0.0068,
      test_accuracy: 0.8233,
      precision_macro: 0.819,
      recall_macro: 0.8099,
      f1_macro: 0.814,
      precision_weighted: 0.8215,
      recall_weighted: 0.8233,
      f1_weighted: 0.822,
      roc_auc: 0.957,
      confusion_matrix: [[252, 25, 0], [39, 142, 18], [0, 24, 151]],
      classes: ["Low", "Moderate", "High"]
    }
  }
};

export const INITIAL_DEMO_HISTORY = [
  {
    id: 1,
    timestamp: new Date(Date.now() - 14 * 86400000).toISOString(),
    modality_mode: "multimodal",
    fused_stress_score: 0.22,
    facial_stress_score: 0.20,
    behavioural_stress_score: 0.24,
    stress_category: "Low",
    confidence: 0.91,
    modality_weights: { facial: 0.48, behavioural: 0.52 },
    facial_features: {
      dominant_emotion: "happy",
      emotion_probabilities: { happy: 0.65, neutral: 0.25, surprise: 0.05, sad: 0.02, fear: 0.01, disgust: 0.01, anger: 0.01 },
      eye_aspect_ratio: 0.31
    },
    behavioural_features: { sleep_hours: 8.0, screen_time_hours: 4.5, work_study_hours: 5.0, academic_work_pressure: 2, physical_activity_mins: 60, break_frequency: 4, self_reported_mood: 4, perceived_stress_level: 2 },
    shap_contributions: [
      { feature: "physical_activity_mins", display_name: "Physical Activity", value: 60, shap_value: -0.09 },
      { feature: "sleep_hours", display_name: "Sleep Duration", value: 8.0, shap_value: -0.07 },
      { feature: "academic_work_pressure", display_name: "Academic/Work Pressure", value: 2, shap_value: -0.05 }
    ],
    recommendations: [
      { category: "Physical Recovery", title: "Maintain Healthy Rhythm", advice: "Your physical and emotional baselines are well balanced. Keep your routine steady." }
    ],
    notes: "Weekend rest period, feeling energized."
  },
  {
    id: 2,
    timestamp: new Date(Date.now() - 12 * 86400000).toISOString(),
    modality_mode: "multimodal",
    fused_stress_score: 0.28,
    facial_stress_score: 0.25,
    behavioural_stress_score: 0.30,
    stress_category: "Low",
    confidence: 0.88,
    modality_weights: { facial: 0.50, behavioural: 0.50 },
    facial_features: {
      dominant_emotion: "happy",
      emotion_probabilities: { happy: 0.50, neutral: 0.35, surprise: 0.08, sad: 0.03, fear: 0.01, disgust: 0.01, anger: 0.02 },
      eye_aspect_ratio: 0.29
    },
    behavioural_features: { sleep_hours: 7.5, screen_time_hours: 5.0, work_study_hours: 6.0, academic_work_pressure: 2, physical_activity_mins: 45, break_frequency: 4, self_reported_mood: 4, perceived_stress_level: 2 },
    shap_contributions: [
      { feature: "break_frequency", display_name: "Break Regularity", value: 4, shap_value: -0.08 },
      { feature: "sleep_hours", display_name: "Sleep Duration", value: 7.5, shap_value: -0.06 }
    ],
    recommendations: [
      { category: "Cognitive Ergonomics", title: "Active Micro-Breaks", advice: "Regular study intervals are preserving high cognitive focus." }
    ],
    notes: "Starting project sprint."
  },
  {
    id: 3,
    timestamp: new Date(Date.now() - 10 * 86400000).toISOString(),
    modality_mode: "multimodal",
    fused_stress_score: 0.44,
    facial_stress_score: 0.40,
    behavioural_stress_score: 0.48,
    stress_category: "Moderate",
    confidence: 0.86,
    modality_weights: { facial: 0.49, behavioural: 0.51 },
    facial_features: {
      dominant_emotion: "neutral",
      emotion_probabilities: { neutral: 0.45, sad: 0.20, happy: 0.15, fear: 0.10, anger: 0.05, surprise: 0.03, disgust: 0.02 },
      eye_aspect_ratio: 0.25
    },
    behavioural_features: { sleep_hours: 6.0, screen_time_hours: 8.0, work_study_hours: 8.5, academic_work_pressure: 3, physical_activity_mins: 20, break_frequency: 2, self_reported_mood: 3, perceived_stress_level: 3 },
    shap_contributions: [
      { feature: "screen_time_hours", display_name: "Daily Screen Time", value: 8.0, shap_value: +0.07 },
      { feature: "sleep_hours", display_name: "Sleep Duration", value: 6.0, shap_value: +0.05 }
    ],
    recommendations: [
      { category: "Visual Health", title: "20-20-20 Eye Rest", advice: "Every 20 minutes look at an object 20 feet away for 20 seconds to relieve digital fatigue." }
    ],
    notes: "Lab report deadlines approaching."
  },
  {
    id: 4,
    timestamp: new Date(Date.now() - 8 * 86400000).toISOString(),
    modality_mode: "behavioural_only",
    fused_stress_score: 0.51,
    facial_stress_score: null,
    behavioural_stress_score: 0.51,
    stress_category: "Moderate",
    confidence: 0.85,
    modality_weights: { facial: 0.0, behavioural: 1.0 },
    behavioural_features: { sleep_hours: 5.5, screen_time_hours: 9.0, work_study_hours: 9.0, academic_work_pressure: 4, physical_activity_mins: 15, break_frequency: 2, self_reported_mood: 2, perceived_stress_level: 4 },
    shap_contributions: [
      { feature: "academic_work_pressure", display_name: "Academic Pressure", value: 4, shap_value: +0.11 },
      { feature: "sleep_hours", display_name: "Sleep Duration", value: 5.5, shap_value: +0.08 }
    ],
    recommendations: [
      { category: "Sleep Hygiene", title: "Target 7 Hours Rest", advice: "Gradually shift bedtime 30 minutes earlier to prevent cognitive accumulation." }
    ],
    notes: "Webcam disabled during late night assignment."
  },
  {
    id: 5,
    timestamp: new Date(Date.now() - 5 * 86400000).toISOString(),
    modality_mode: "multimodal",
    fused_stress_score: 0.72,
    facial_stress_score: 0.68,
    behavioural_stress_score: 0.76,
    stress_category: "High",
    confidence: 0.89,
    modality_weights: { facial: 0.49, behavioural: 0.51 },
    facial_features: {
      dominant_emotion: "fear",
      emotion_probabilities: { fear: 0.55, neutral: 0.20, sad: 0.12, anger: 0.08, happy: 0.02, surprise: 0.02, disgust: 0.01 },
      eye_aspect_ratio: 0.20
    },
    behavioural_features: { sleep_hours: 4.5, screen_time_hours: 11.5, work_study_hours: 12.0, academic_work_pressure: 5, physical_activity_mins: 0, break_frequency: 1, self_reported_mood: 1, perceived_stress_level: 5 },
    shap_contributions: [
      { feature: "academic_work_pressure", display_name: "Academic Pressure", value: 5, shap_value: +0.16 },
      { feature: "sleep_hours", display_name: "Sleep Deficit", value: 4.5, shap_value: +0.14 },
      { feature: "screen_time_hours", display_name: "Screen Time", value: 11.5, shap_value: +0.09 }
    ],
    recommendations: [
      { category: "Decompression", title: "4-4-4-4 Box Breathing", advice: "Engage in controlled vagal nerve pacing: inhale 4s, hold 4s, exhale 4s, hold 4s." },
      { category: "Task Management", title: "Eisenhower Prioritization", advice: "Postpone non-essential deliverables and consult advisors." }
    ],
    notes: "Midterm exam preparation crunch."
  },
  {
    id: 6,
    timestamp: new Date(Date.now() - 4 * 86400000).toISOString(),
    modality_mode: "multimodal",
    fused_stress_score: 0.64,
    facial_stress_score: 0.18,
    behavioural_stress_score: 0.79,
    stress_category: "High",
    confidence: 0.86,
    modality_weights: { facial: 0.25, behavioural: 0.75 },
    facial_features: {
      dominant_emotion: "happy",
      emotion_probabilities: { happy: 0.70, neutral: 0.20, surprise: 0.05, sad: 0.02, anger: 0.01, fear: 0.01, disgust: 0.01 },
      eye_aspect_ratio: 0.27
    },
    behavioural_features: { sleep_hours: 4.0, screen_time_hours: 10.0, work_study_hours: 11.0, academic_work_pressure: 5, physical_activity_mins: 0, break_frequency: 1, self_reported_mood: 2, perceived_stress_level: 5 },
    shap_contributions: [
      { feature: "academic_work_pressure", display_name: "Academic Pressure", value: 5, shap_value: +0.15 },
      { feature: "sleep_hours", display_name: "Sleep Deficit", value: 4.0, shap_value: +0.13 }
    ],
    recommendations: [
      { category: "Clinical Awareness", title: "Masked Stress Intervention", advice: "High chronic workload detected despite external neutral/smiling demeanor. Prioritize physical rest." }
    ],
    notes: "Smiling depression / masked stress validation case."
  },
  {
    id: 7,
    timestamp: new Date(Date.now() - 2 * 86400000).toISOString(),
    modality_mode: "multimodal",
    fused_stress_score: 0.46,
    facial_stress_score: 0.42,
    behavioural_stress_score: 0.50,
    stress_category: "Moderate",
    confidence: 0.87,
    modality_weights: { facial: 0.50, behavioural: 0.50 },
    facial_features: {
      dominant_emotion: "neutral",
      emotion_probabilities: { neutral: 0.55, happy: 0.25, sad: 0.10, surprise: 0.04, fear: 0.03, anger: 0.02, disgust: 0.01 },
      eye_aspect_ratio: 0.26
    },
    behavioural_features: { sleep_hours: 6.5, screen_time_hours: 7.5, work_study_hours: 8.0, academic_work_pressure: 3, physical_activity_mins: 30, break_frequency: 3, self_reported_mood: 3, perceived_stress_level: 3 },
    shap_contributions: [
      { feature: "physical_activity_mins", display_name: "Physical Activity", value: 30, shap_value: -0.05 },
      { feature: "academic_work_pressure", display_name: "Academic Pressure", value: 3, shap_value: +0.06 }
    ],
    recommendations: [
      { category: "Physical Recovery", title: "Post-Exam Stabilization", advice: "Continue reinstating structured aerobic movement." }
    ],
    notes: "Post-exam decompression day."
  },
  {
    id: 8,
    timestamp: new Date(Date.now() - 1 * 86400000).toISOString(),
    modality_mode: "multimodal",
    fused_stress_score: 0.35,
    facial_stress_score: 0.32,
    behavioural_stress_score: 0.38,
    stress_category: "Low",
    confidence: 0.89,
    modality_weights: { facial: 0.49, behavioural: 0.51 },
    facial_features: {
      dominant_emotion: "neutral",
      emotion_probabilities: { neutral: 0.60, happy: 0.30, surprise: 0.05, sad: 0.02, fear: 0.01, anger: 0.01, disgust: 0.01 },
      eye_aspect_ratio: 0.29
    },
    behavioural_features: { sleep_hours: 7.5, screen_time_hours: 6.0, work_study_hours: 6.5, academic_work_pressure: 2, physical_activity_mins: 45, break_frequency: 4, self_reported_mood: 4, perceived_stress_level: 2 },
    shap_contributions: [
      { feature: "sleep_hours", display_name: "Sleep Duration", value: 7.5, shap_value: -0.07 },
      { feature: "physical_activity_mins", display_name: "Physical Activity", value: 45, shap_value: -0.06 }
    ],
    recommendations: [
      { category: "Wellness Maintenance", title: "Sustained Baseline", advice: "Indicators show recovery to balanced physiological equilibrium." }
    ],
    notes: "Re-established regular schedule."
  }
];

// Client-side execution of actual project formulas
export function calculateClientAssessment(payload) {
  const mode = payload.modality_mode || "multimodal";
  const behData = payload.behavioural_data;
  const faceData = payload.facial_data;
  
  let facialScore = null;
  let facialConf = 0.85;
  let dominantEmotion = "neutral";
  let emotionProbs = { neutral: 0.62, happy: 0.15, sad: 0.08, surprise: 0.05, fear: 0.04, disgust: 0.03, anger: 0.03 };
  let ear = 0.28;

  if (faceData && faceData.image_base64) {
    ear = faceData.client_ear || 0.28;
    // Ocular strain formula from project
    let earStrain = 0.0;
    if (ear < 0.22) {
      earStrain = Math.min(0.35, (0.22 - ear) * 2.5);
    } else if (ear > 0.38) {
      earStrain = Math.min(0.20, (ear - 0.38) * 1.5);
    }
    // Emotion valence-arousal component
    const emotionStress = (0.03 * 0.95) + (0.04 * 0.90) + (0.08 * 0.70) + (0.03 * 0.75) + (0.05 * 0.30) + (0.62 * 0.15) + (0.15 * 0.02);
    facialScore = Math.max(0.0, Math.min(1.0, (0.75 * emotionStress) + (0.25 * earStrain)));
    facialConf = 0.88;
  }

  let behScore = null;
  let behConf = 0.87;
  let shapContributions = [];

  if (behData) {
    const sleep = Number(behData.sleep_hours) || 7.0;
    const screen = Number(behData.screen_time_hours) || 6.0;
    const work = Number(behData.work_study_hours) || 7.0;
    const pressure = Number(behData.academic_work_pressure) || 3;
    const activity = Number(behData.physical_activity_mins) || 30;
    const breaks = Number(behData.break_frequency) || 3;
    const mood = Number(behData.self_reported_mood) || 3;
    const pstress = Number(behData.perceived_stress_level) || 3;

    // Academic regression formula implemented in backend/app/ml/behavioural_model.py
    const rawBeh = (
      (pressure / 5.0) * 0.30 +
      (pstress / 5.0) * 0.30 +
      (Math.max(0, 8.0 - sleep) / 5.0) * 0.15 +
      (screen / 16.0) * 0.10 +
      ((5.0 - mood) / 4.0) * 0.10 -
      (activity / 150.0) * 0.05
    );
    behScore = Math.max(0.0, Math.min(1.0, rawBeh));

    shapContributions = [
      { feature: "academic_work_pressure", display_name: "Academic/Work Pressure", value: pressure, shap_value: Number(((pressure - 3) * 0.05).toFixed(3)) },
      { feature: "sleep_hours", display_name: "Sleep Duration", value: sleep, shap_value: Number(((7.5 - sleep) * 0.04).toFixed(3)) },
      { feature: "perceived_stress_level", display_name: "Perceived Stress Level", value: pstress, shap_value: Number(((pstress - 2.5) * 0.04).toFixed(3)) },
      { feature: "screen_time_hours", display_name: "Daily Screen Time", value: screen, shap_value: Number(((screen - 5) * 0.02).toFixed(3)) },
      { feature: "physical_activity_mins", display_name: "Physical Activity", value: activity, shap_value: Number(((30 - activity) * 0.002).toFixed(3)) },
      { feature: "break_frequency", display_name: "Break Regularity", value: breaks, shap_value: Number(((3 - breaks) * 0.02).toFixed(3)) }
    ].sort((a, b) => Math.abs(b.shap_value) - Math.abs(a.shap_value));
  }

  // Multimodal Fusion Logic
  let fusedScore = 0.30;
  let weights = { facial: 0.5, behavioural: 0.5 };
  let effectiveMode = mode;

  if (facialScore !== null && behScore !== null) {
    let wf = facialConf / (facialConf + behConf);
    let wb = behConf / (facialConf + behConf);
    // Dissonance override
    if (behScore > 0.70 && facialScore < 0.25) {
      wb = 0.75;
      wf = 0.25;
    }
    fusedScore = (wf * facialScore) + (wb * behScore);
    weights = { facial: Number(wf.toFixed(2)), behavioural: Number(wb.toFixed(2)) };
  } else if (facialScore !== null) {
    fusedScore = facialScore;
    effectiveMode = "facial_only";
    weights = { facial: 1.0, behavioural: 0.0 };
  } else if (behScore !== null) {
    fusedScore = behScore;
    effectiveMode = "behavioural_only";
    weights = { facial: 0.0, behavioural: 1.0 };
  }

  fusedScore = Math.max(0.0, Math.min(1.0, Number(fusedScore.toFixed(4))));

  // Project thresholds
  let category = "Moderate";
  if (fusedScore < 0.38) category = "Low";
  else if (fusedScore > 0.52) category = "High";

  // Recommendations
  const recs = [];
  if (category === "High") {
    recs.push({ category: "Acute Decompression", title: "4-4-4-4 Box Breathing", advice: "High acute strain detected. Perform 4-minute box breathing: inhale 4s, hold 4s, exhale 4s, hold 4s." });
    recs.push({ category: "Workload Triage", title: "Eisenhower Task Matrix", advice: "De-prioritize non-urgent academic tasks and schedule mandatory sleep blocks." });
  } else if (category === "Moderate") {
    recs.push({ category: "Visual Health", title: "20-20-20 Eye Rest", advice: "Every 20 minutes look at an object 20 feet away for 20 seconds to alleviate ocular fatigue." });
    recs.push({ category: "Postural Relief", title: "Micro-Breaks", advice: "Stand up, stretch thoracic spine, and hydrate every 45-60 minutes." });
  } else {
    recs.push({ category: "Baseline Preservation", title: "Maintain Healthy Routine", advice: "Your physical and behavioural indicators show optimal resilience. Continue your rest habits." });
  }

  const assessmentRecord = {
    id: Date.now(),
    timestamp: new Date().toISOString(),
    modality_mode: effectiveMode,
    fused_stress_score: fusedScore,
    facial_stress_score: facialScore !== null ? Number(facialScore.toFixed(4)) : null,
    behavioural_stress_score: behScore !== null ? Number(behScore.toFixed(4)) : null,
    stress_category: category,
    confidence: 0.88,
    modality_weights: weights,
    facial_features: facialScore !== null ? {
      dominant_emotion: dominantEmotion,
      emotion_probabilities: emotionProbs,
      eye_aspect_ratio: ear
    } : null,
    behavioural_features: behData || null,
    shap_contributions: shapContributions,
    recommendations: recs,
    notes: payload.notes || ""
  };

  // Save to localStorage history
  try {
    const existing = JSON.parse(localStorage.getItem('stress_demo_history') || '[]');
    existing.unshift(assessmentRecord);
    localStorage.setItem('stress_demo_history', JSON.stringify(existing.slice(0, 50)));
  } catch (e) {
    console.error("Local storage error:", e);
  }

  return assessmentRecord;
}

export function getClientHistory() {
  try {
    const stored = localStorage.getItem('stress_demo_history');
    if (stored) {
      return JSON.parse(stored);
    }
    // initialize with INITIAL_DEMO_HISTORY
    localStorage.setItem('stress_demo_history', JSON.stringify(INITIAL_DEMO_HISTORY));
    return INITIAL_DEMO_HISTORY;
  } catch (e) {
    return INITIAL_DEMO_HISTORY;
  }
}
