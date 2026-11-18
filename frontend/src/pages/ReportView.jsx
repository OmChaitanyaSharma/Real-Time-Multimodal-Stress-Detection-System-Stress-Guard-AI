import React, { useState, useEffect } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import { stressAPI } from '../services/api';
import { Printer, ArrowLeft, Activity, ShieldAlert, CheckCircle2, Clock, Calendar } from 'lucide-react';

export const ReportView = () => {
  const { id } = useParams();
  const location = useLocation();
  const [assessment, setAssessment] = useState(location.state?.assessment || null);
  const [loading, setLoading] = useState(!assessment);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!assessment && id) {
      const fetchAssessment = async () => {
        try {
          const res = (id === 'latest')
            ? await stressAPI.getLatestAssessment()
            : await stressAPI.getAssessmentDetail(id);
          setAssessment(res.data);
        } catch (err) {
          console.error('Failed to load assessment report:', err);
          setError('Failed to retrieve assessment record.');
        } finally {
          setLoading(false);
        }
      };
      fetchAssessment();
    } else {
      setLoading(false);
    }
  }, [id, assessment]);

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error || !assessment) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center p-6 text-center space-y-4">
        <Activity className="w-12 h-12 text-slate-600" />
        <h3 className="text-lg font-bold text-slate-200">{error || 'Assessment report not found.'}</h3>
        <Link to="/dashboard" className="px-4 py-2 text-xs font-semibold text-white bg-indigo-600 rounded-lg">
          Back to Dashboard
        </Link>
      </div>
    );
  }

  const {
    timestamp,
    modality_mode,
    fused_stress_score,
    stress_category,
    confidence,
    modality_weights,
    facial_stress_score,
    behavioural_stress_score,
    facial_features,
    behavioural_features,
    shap_contributions = [],
    gradcam_base64,
    recommendations = [],
    notes
  } = assessment;

  const formattedDate = timestamp ? new Date(timestamp).toLocaleString() : new Date().toLocaleString();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      
      {/* Interactive Controls (Hidden during print) */}
      <div className="flex items-center justify-between no-print border-b border-slate-800 pb-4">
        <Link
          to="/dashboard"
          className="flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>
        <button
          onClick={handlePrint}
          className="flex items-center gap-2 px-5 py-2.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 rounded-xl shadow-md shadow-indigo-600/20 transition-all"
        >
          <Printer className="w-4 h-4" />
          Print / Save PDF Report
        </button>
      </div>

      {/* Printable Report Document Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl space-y-8 text-slate-100 print:bg-white print:text-black print:border-none print:shadow-none print:p-0">
        
        {/* Document Header */}
        <div className="border-b border-slate-800 print:border-black pb-6 space-y-2 text-center sm:text-left flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <span className="text-[10px] uppercase font-bold tracking-widest text-indigo-400 print:text-indigo-700">
              Department of Computer Science & Engineering • B.Tech Major Project
            </span>
            <h1 className="text-2xl font-black tracking-tight text-white print:text-black mt-1">
              Multimodal Stress Assessment Report
            </h1>
            <p className="text-xs text-slate-400 print:text-slate-600">
              System ID: <code className="font-mono text-slate-300 print:text-black">MSDA-2026-REC#{assessment.id || 'LATEST'}</code>
            </p>
          </div>

          <div className="text-right text-xs text-slate-400 print:text-slate-600 space-y-1">
            <p className="flex items-center gap-1.5 justify-end">
              <Calendar className="w-3.5 h-3.5" />
              Generated: {formattedDate}
            </p>
            <p className="flex items-center gap-1.5 justify-end">
              <Activity className="w-3.5 h-3.5 text-indigo-400" />
              Evaluation Mode: <strong className="capitalize text-slate-200 print:text-black">{modality_mode.replace('_', ' ')}</strong>
            </p>
          </div>
        </div>

        {/* Primary Classification Strip */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 p-5 bg-slate-950 print:bg-slate-50 print:border print:border-slate-300 rounded-xl border border-slate-800">
          <div className="space-y-1 text-center sm:text-left">
            <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Overall Classification</span>
            <div className={`text-xl font-black ${
              stress_category === 'High' ? 'text-rose-400' : stress_category === 'Moderate' ? 'text-amber-400' : 'text-emerald-400'
            }`}>
              {stress_category} Stress Indicator
            </div>
          </div>

          <div className="space-y-1 text-center sm:text-left">
            <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Composite Stress Score</span>
            <div className="text-xl font-black text-slate-100 print:text-black">
              {Math.round(fused_stress_score * 100)} / 100
            </div>
          </div>

          <div className="space-y-1 text-center sm:text-left">
            <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Model Confidence</span>
            <div className="text-xl font-black text-indigo-400 print:text-indigo-700">
              {Math.round(confidence * 100)}%
            </div>
          </div>
        </div>

        {/* Quantitative Modality Decomposition Table */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-200 print:text-black border-b border-slate-800 print:border-slate-300 pb-2">
            1. Multimodal Feature Decomposition
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            {/* Visual Indicators */}
            <div className="bg-slate-950 print:bg-white p-4 rounded-xl border border-slate-800 print:border-slate-300 space-y-2">
              <h4 className="font-semibold text-indigo-300 print:text-indigo-800">Visual Facial Modality</h4>
              <ul className="space-y-1.5 text-slate-300 print:text-black">
                <li>Facial Stress Probability: <strong>{facial_stress_score !== null ? `${Math.round(facial_stress_score * 100)}%` : 'Not Captured'}</strong></li>
                <li>Dominant Facial Expression: <strong className="capitalize">{facial_features?.dominant_emotion || 'N/A'}</strong></li>
                <li>Eye Aspect Ratio (EAR): <strong>{facial_features?.eye_aspect_ratio || 'N/A'}</strong></li>
                <li>Ensemble Fusion Weight: <strong>{modality_weights?.facial ? Math.round(modality_weights.facial * 100) : 0}%</strong></li>
              </ul>
            </div>

            {/* Behavioural Indicators */}
            <div className="bg-slate-950 print:bg-white p-4 rounded-xl border border-slate-800 print:border-slate-300 space-y-2">
              <h4 className="font-semibold text-violet-300 print:text-violet-800">Behavioural Lifestyle Modality</h4>
              <ul className="space-y-1.5 text-slate-300 print:text-black">
                <li>Behavioural Stress Probability: <strong>{behavioural_stress_score !== null ? `${Math.round(behavioural_stress_score * 100)}%` : 'Not Captured'}</strong></li>
                <li>Sleep Duration: <strong>{behavioural_features?.sleep_hours ?? 'N/A'} hrs/night</strong></li>
                <li>Daily Screen Exposure: <strong>{behavioural_features?.screen_time_hours ?? 'N/A'} hrs</strong></li>
                <li>Academic Work Pressure: <strong>{behavioural_features?.academic_work_pressure ?? 'N/A'} / 5</strong></li>
                <li>Ensemble Fusion Weight: <strong>{modality_weights?.behavioural ? Math.round(modality_weights.behavioural * 100) : 0}%</strong></li>
              </ul>
            </div>
          </div>
        </div>

        {/* Explainable AI (SHAP & Grad-CAM) Summary */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-200 print:text-black border-b border-slate-800 print:border-slate-300 pb-2">
            2. Explainable AI (XAI) Attribution Breakdown
          </h3>

          {shap_contributions.length > 0 && (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300 print:text-black border border-slate-800 print:border-slate-300 rounded-lg">
                <thead className="bg-slate-950 print:bg-slate-100 text-[10px] uppercase font-bold text-slate-400 print:text-slate-700">
                  <tr>
                    <th className="py-2.5 px-3">Lifestyle Metric</th>
                    <th className="py-2.5 px-3">User Value</th>
                    <th className="py-2.5 px-3">SHAP Value</th>
                    <th className="py-2.5 px-3">Impact Vector</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 print:divide-slate-200">
                  {shap_contributions.map((s, idx) => (
                    <tr key={idx}>
                      <td className="py-2 px-3 font-medium">{s.display_name}</td>
                      <td className="py-2 px-3">{s.value}</td>
                      <td className="py-2 px-3 font-mono">{s.shap_value}</td>
                      <td className="py-2 px-3">
                        <span className={`inline-block text-[10px] font-semibold px-2 py-0.5 rounded ${
                          s.shap_value > 0 ? 'bg-rose-500/20 text-rose-300 print:bg-rose-100 print:text-rose-800' : 'bg-emerald-500/20 text-emerald-300 print:bg-emerald-100 print:text-emerald-800'
                        }`}>
                          {s.shap_value > 0 ? 'Increases Stress' : 'Buffers Stress'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {gradcam_base64 && (
            <div className="flex items-center gap-4 pt-2">
              <img
                src={gradcam_base64}
                alt="Grad-CAM Saliency"
                className="w-24 h-24 rounded-lg border border-slate-700 object-cover"
              />
              <p className="text-xs text-slate-400 print:text-slate-600 leading-relaxed">
                <strong>Grad-CAM Activation:</strong> Visual attention gradients localized to the ocular periorbital zone and brow furrows, consistent with observed tension vectors in validated FACS (Facial Action Coding System) literature.
              </p>
            </div>
          )}
        </div>

        {/* Personalized Recommendations Section */}
        {recommendations.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-200 print:text-black border-b border-slate-800 print:border-slate-300 pb-2">
              3. Tailored Wellness Interventions
            </h3>
            <div className="space-y-2 text-xs">
              {recommendations.map((rec, idx) => (
                <div key={idx} className="p-3 rounded-lg bg-slate-950 print:bg-slate-50 border border-slate-800 print:border-slate-300 space-y-1">
                  <div className="flex justify-between items-center">
                    <strong className="text-slate-100 print:text-black font-bold">
                      [{rec.category}] {rec.title}
                    </strong>
                    <span className="text-[10px] font-semibold text-slate-400 uppercase">
                      {rec.priority} Priority
                    </span>
                  </div>
                  <p className="text-slate-400 print:text-slate-700 leading-relaxed">
                    {rec.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Notes */}
        {notes && (
          <div className="space-y-1 text-xs">
            <h4 className="font-bold text-slate-200 print:text-black">User Session Notes:</h4>
            <p className="text-slate-400 print:text-slate-700 italic bg-slate-950 print:bg-slate-50 p-3 rounded-lg border border-slate-800 print:border-slate-300">
              "{notes}"
            </p>
          </div>
        )}

        {/* Ethical Non-Diagnostic Disclaimer */}
        <div className="pt-4 border-t border-slate-800 print:border-black text-[10px] text-slate-500 print:text-slate-600 space-y-1 leading-relaxed">
          <p className="font-bold uppercase tracking-wide text-slate-400 print:text-black">
            Academic Screening & Ethical Non-Diagnostic Disclaimer:
          </p>
          <p>
            This system evaluates observable multimodal indicators for informational self-awareness and major project evaluation. 
            Facial expressions and self-reported surveys cannot establish a clinical psychological or psychiatric diagnosis. 
            This assessment should not replace consultation with a qualified medical professional.
          </p>
        </div>

      </div>

    </div>
  );
};
