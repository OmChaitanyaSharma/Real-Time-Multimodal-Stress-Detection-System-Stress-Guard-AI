import React, { useState, useEffect } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { stressAPI } from '../services/api';
import { StressGauge } from '../components/StressGauge';
import { ShapChart } from '../components/ShapChart';
import { GradCamViewer } from '../components/GradCamViewer';
import { RecommendationCard } from '../components/RecommendationCard';
import { 
  FileText, 
  RotateCcw, 
  BarChart3, 
  Sparkles, 
  ShieldCheck, 
  Activity, 
  Clock, 
  Tag,
  ArrowRight
} from 'lucide-react';

export const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [assessment, setAssessment] = useState(location.state?.assessment || null);
  const [originalFaceBase64, setOriginalFaceBase64] = useState(location.state?.originalFaceBase64 || null);
  const [loading, setLoading] = useState(!assessment);

  useEffect(() => {
    if (!assessment) {
      const fetchLatest = async () => {
        try {
          const res = await stressAPI.getLatestAssessment();
          setAssessment(res.data);
          if (res.data?.facial_features?.gradcam_base64) {
            setOriginalFaceBase64(res.data.facial_features.gradcam_base64);
          }
        } catch (err) {
          console.error('No assessment state found or failed to fetch latest:', err);
        } finally {
          setLoading(false);
        }
      };
      fetchLatest();
    }
  }, [assessment]);

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!assessment) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center p-6 text-center space-y-4">
        <Activity className="w-12 h-12 text-slate-600 animate-pulse" />
        <h3 className="text-lg font-bold text-slate-200">No Assessment Loaded</h3>
        <p className="text-xs text-slate-400 max-w-sm">
          Please run an assessment through the studio or select a record from your history.
        </p>
        <Link
          to="/assessment"
          className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all"
        >
          Begin New Assessment
        </Link>
      </div>
    );
  }

  const {
    id,
    timestamp,
    modality_mode,
    fused_stress_score,
    stress_category,
    confidence,
    modality_weights,
    facial_stress_score,
    behavioural_stress_score,
    shap_contributions,
    gradcam_base64,
    recommendations = [],
  } = assessment;

  const formattedDate = timestamp ? new Date(timestamp).toLocaleString() : new Date().toLocaleString();

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8 animate-fade-in">
      
      {/* Top Action Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="inline-flex items-center gap-1.5 text-[11px] font-semibold text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded-full border border-indigo-500/20 mb-2">
            <Sparkles className="w-3.5 h-3.5" />
            Assessment Evaluation Complete
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">Multimodal Stress Report</h2>
          <p className="text-xs text-slate-400 flex items-center gap-2 mt-1">
            <Clock className="w-3.5 h-3.5" />
            Evaluated on {formattedDate} • Mode: <span className="text-slate-200 capitalize font-medium">{modality_mode.replace('_', ' ')}</span>
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <Link
            to={`/report/${id || 'latest'}`}
            state={{ assessment, originalFaceBase64 }}
            className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl transition-all"
          >
            <FileText className="w-4 h-4 text-indigo-400" />
            Print / Export Report
          </Link>

          <Link
            to="/assessment"
            className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 rounded-xl shadow-md shadow-indigo-600/20 transition-all"
          >
            <RotateCcw className="w-4 h-4" />
            New Assessment
          </Link>
        </div>
      </div>

      {/* Primary Score & Modality Contribution Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">
        
        {/* Card 1: Stress Gauge Radial */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col items-center justify-center shadow-xl">
          <StressGauge
            score={fused_stress_score}
            category={stress_category}
            confidence={confidence}
            size="lg"
          />
        </div>

        {/* Card 2: Modality Contribution Breakdown */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 lg:col-span-2 flex flex-col justify-between">
          <div>
            <h4 className="text-sm font-semibold text-slate-100">Modality Fusion Weights & Decomposition</h4>
            <p className="text-xs text-slate-400">Mathematical soft voting weights dynamically derived from data quality</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* Facial Modality Card */}
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-300">Facial Vision Modality</span>
                <span className="font-bold text-indigo-400">
                  {facial_stress_score !== null && facial_stress_score !== undefined
                    ? `${Math.round(facial_stress_score * 100)}%`
                    : 'N/A'}
                </span>
              </div>
              <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-indigo-500 transition-all duration-500"
                  style={{ width: `${Math.round((facial_stress_score || 0) * 100)}%` }}
                ></div>
              </div>
              <p className="text-[10px] text-slate-500">
                Weight in Ensemble: <strong>{modality_weights?.facial ? Math.round(modality_weights.facial * 100) : 0}%</strong>
              </p>
            </div>

            {/* Behavioural Modality Card */}
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-300">Behavioural Lifestyle Modality</span>
                <span className="font-bold text-violet-400">
                  {behavioural_stress_score !== null && behavioural_stress_score !== undefined
                    ? `${Math.round(behavioural_stress_score * 100)}%`
                    : 'N/A'}
                </span>
              </div>
              <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-violet-500 transition-all duration-500"
                  style={{ width: `${Math.round((behavioural_stress_score || 0) * 100)}%` }}
                ></div>
              </div>
              <p className="text-[10px] text-slate-500">
                Weight in Ensemble: <strong>{modality_weights?.behavioural ? Math.round(modality_weights.behavioural * 100) : 0}%</strong>
              </p>
            </div>

          </div>

          <div className="bg-slate-950/60 p-3 rounded-xl border border-slate-800 text-[11px] text-slate-400 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>
              Decision fusion formula: <code className="text-slate-300">S_fused = (w_f × S_face) + (w_b × S_beh)</code>. Calibrated thresholds: Low (&lt;38%), Moderate (38-52%), High (&gt;52%).
            </span>
          </div>
        </div>

      </div>

      {/* Explainable AI Strip */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
          <Activity className="w-5 h-5 text-indigo-400" />
          Explainable AI (XAI) Attribution
        </h3>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
          {/* SHAP Chart */}
          <ShapChart shapData={shap_contributions} />

          {/* Grad-CAM Viewer */}
          <GradCamViewer
            gradcamBase64={gradcam_base64}
            originalBase64={originalFaceBase64}
            dominantEmotion={assessment.facial_features?.dominant_emotion || 'neutral'}
          />
        </div>
      </div>

      {/* Personalized Wellness Recommendations */}
      {recommendations.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-amber-400" />
              Personalized Lifestyle Recommendations
            </h3>
            <span className="text-xs text-slate-400">
              Contextually triggered by your specific stressors
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.map((rec, idx) => (
              <RecommendationCard key={idx} recommendation={rec} />
            ))}
          </div>
        </div>
      )}

      {/* Bottom Footer Action */}
      <div className="pt-4 flex items-center justify-between border-t border-slate-800">
        <Link
          to="/dashboard"
          className="text-xs font-semibold text-slate-400 hover:text-white flex items-center gap-1.5 transition-colors"
        >
          <BarChart3 className="w-4 h-4" />
          Back to Assessment Dashboard
        </Link>
        <Link
          to={`/report/${id || 'latest'}`}
          state={{ assessment, originalFaceBase64 }}
          className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1.5 transition-colors"
        >
          View Full Printable Report
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

    </div>
  );
};
