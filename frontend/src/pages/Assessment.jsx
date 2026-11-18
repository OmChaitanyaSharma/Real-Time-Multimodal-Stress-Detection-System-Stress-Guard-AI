import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { WebcamCapture } from '../components/WebcamCapture';
import { QuestionnaireWizard } from '../components/QuestionnaireWizard';
import { DisclaimerModal } from '../components/DisclaimerModal';
import { stressAPI } from '../services/api';
import { 
  Sparkles, 
  Camera, 
  ClipboardList, 
  Layers, 
  AlertCircle,
  ArrowRight,
  ShieldAlert
} from 'lucide-react';

export const Assessment = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('multimodal'); // 'multimodal', 'facial_only', 'behavioural_only'
  const [hasConsented, setHasConsented] = useState(false);
  const [showConsentModal, setShowConsentModal] = useState(!hasConsented);

  // Staged data
  const [facialData, setFacialData] = useState(null);
  const [facialBase64, setFacialBase64] = useState(null);
  const [behaviouralData, setBehaviouralData] = useState({
    sleep_hours: 6.5,
    screen_time_hours: 7.0,
    work_study_hours: 7.5,
    academic_work_pressure: 3,
    physical_activity_mins: 30,
    break_frequency: 3,
    self_reported_mood: 3,
    perceived_stress_level: 3,
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [userNotes, setUserNotes] = useState('');

  const handleFacialComplete = (analysisResult, base64Frame) => {
    setFacialData(analysisResult);
    setFacialBase64(base64Frame);
  };

  const handleSurveyComplete = (surveyValues) => {
    setBehaviouralData(surveyValues);
    if (activeTab === 'behavioural_only') {
      executeSubmission('behavioural_only', null, surveyValues);
    }
  };

  const executeSubmission = async (mode, faceImg, behData) => {
    setError(null);
    setSubmitting(true);

    try {
      const payload = {
        modality_mode: mode,
        notes: userNotes || undefined,
      };

      let effectiveMode = mode;
      const targetFace = faceImg || facialBase64;

      if (mode === 'facial_only') {
        if (!targetFace) {
          throw new Error('Please capture a face frame before submitting facial assessment.');
        }
        payload.facial_data = {
          image_base64: targetFace,
          client_ear: facialData?.eye_aspect_ratio,
        };
      } else if (mode === 'multimodal') {
        if (targetFace) {
          payload.facial_data = {
            image_base64: targetFace,
            client_ear: facialData?.eye_aspect_ratio,
          };
        } else {
          // Graceful fallback when webcam was skipped in multimodal mode
          effectiveMode = 'behavioural_only';
          payload.modality_mode = 'behavioural_only';
        }
      }

      if (effectiveMode === 'multimodal' || effectiveMode === 'behavioural_only') {
        payload.behavioural_data = behData || behaviouralData;
      }

      const res = await stressAPI.evaluateMultimodal(payload);
      
      // Navigate to results page with response state
      navigate('/results', {
        state: {
          assessment: res.data,
          originalFaceBase64: faceImg || facialBase64,
        },
      });
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || 'Assessment evaluation failed.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8 animate-fade-in">
      
      <DisclaimerModal
        isOpen={showConsentModal}
        onAccept={() => {
          setHasConsented(true);
          setShowConsentModal(false);
        }}
        onCancel={() => {
          setShowConsentModal(false);
        }}
      />

      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-2">
        <h2 className="text-3xl font-bold text-white tracking-tight">Stress Assessment Studio</h2>
        <p className="text-xs text-slate-400">
          Capture observable biometric cues alongside daily lifestyle patterns for multimodal fusion analysis.
        </p>
      </div>

      {/* Mode Selector Tabs */}
      <div className="flex items-center justify-center">
        <div className="bg-slate-900 border border-slate-800 p-1.5 rounded-2xl flex flex-wrap items-center gap-1">
          <button
            onClick={() => setActiveTab('multimodal')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'multimodal'
                ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md shadow-indigo-600/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Layers className="w-4 h-4" />
            Multimodal Fusion (Recommended)
          </button>
          
          <button
            onClick={() => setActiveTab('facial_only')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'facial_only'
                ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md shadow-indigo-600/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Camera className="w-4 h-4" />
            Facial Analysis Only
          </button>

          <button
            onClick={() => setActiveTab('behavioural_only')}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'behavioural_only'
                ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md shadow-indigo-600/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <ClipboardList className="w-4 h-4" />
            Behavioural Survey Only
          </button>
        </div>
      </div>

      {error && (
        <div className="max-w-3xl mx-auto p-4 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center gap-2.5">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* TAB CONTENT: Multimodal */}
      {activeTab === 'multimodal' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
            {/* Left Column: Webcam */}
            <div className="space-y-4">
              <WebcamCapture onAnalysisComplete={handleFacialComplete} />
            </div>

            {/* Right Column: Questionnaire */}
            <div className="space-y-4">
              <QuestionnaireWizard
                initialValues={behaviouralData}
                onComplete={setBehaviouralData}
                isSubmitting={false}
              />
            </div>
          </div>

          {/* Unified Submission Panel */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-xl">
            <div className="space-y-1 text-center sm:text-left">
              <span className="text-xs font-semibold text-slate-200 flex items-center gap-2 justify-center sm:justify-start">
                <Sparkles className="w-4 h-4 text-indigo-400" />
                Ready to compute multimodal fusion?
              </span>
              <p className="text-[11px] text-slate-400">
                {facialData ? 'Facial frame captured.' : 'Webcam frame pending (optional but recommended).'} Survey parameters configured.
              </p>
            </div>

            <button
              onClick={() => executeSubmission('multimodal', facialBase64, behaviouralData)}
              disabled={submitting}
              className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white font-semibold text-xs shadow-lg shadow-indigo-600/25 disabled:opacity-50 transition-all shrink-0 w-full sm:w-auto justify-center"
            >
              {submitting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Computing Decision Fusion...
                </>
              ) : (
                <>
                  Generate Multimodal Assessment
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* TAB CONTENT: Facial Only */}
      {activeTab === 'facial_only' && (
        <div className="max-w-xl mx-auto space-y-6">
          <WebcamCapture onAnalysisComplete={handleFacialComplete} />
          {facialData && (
            <button
              onClick={() => executeSubmission('facial_only', facialBase64, null)}
              disabled={submitting}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-lg shadow-indigo-600/20 transition-all"
            >
              {submitting ? 'Processing...' : 'Complete Facial-Only Assessment'}
              <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </div>
      )}

      {/* TAB CONTENT: Behavioural Only */}
      {activeTab === 'behavioural_only' && (
        <div className="max-w-2xl mx-auto space-y-6">
          <QuestionnaireWizard
            initialValues={behaviouralData}
            onComplete={(vals) => executeSubmission('behavioural_only', null, vals)}
            isSubmitting={submitting}
          />
        </div>
      )}

    </div>
  );
};
