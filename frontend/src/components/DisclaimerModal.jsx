import React, { useEffect } from 'react';
import { ShieldCheck, Video, Lock, ArrowRight } from 'lucide-react';

export const DisclaimerModal = ({ isOpen, onAccept, onCancel }) => {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen && onCancel) {
        onCancel();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onCancel]);

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in"
      role="dialog"
      aria-modal="true"
      aria-labelledby="disclaimer-title"
    >
      <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5">
        
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 id="disclaimer-title" className="text-lg font-semibold text-white">Informed User Consent</h3>
            <p className="text-xs text-slate-400">Data Privacy & Evaluation Protocol</p>
          </div>
        </div>

        <div className="space-y-3 text-sm text-slate-300 leading-relaxed bg-slate-950/50 p-4 rounded-xl border border-slate-800/60">
          <div className="flex items-start gap-2.5">
            <Lock className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <p className="text-xs">
              <strong className="text-slate-100">Zero Video Storage:</strong> Webcam video frames are processed transiently in-memory for facial landmark and emotion inference, and are never saved to disk or shared with third parties.
            </p>
          </div>
          <div className="flex items-start gap-2.5">
            <Video className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
            <p className="text-xs">
              <strong className="text-slate-100">Local Edge Processing:</strong> Eye Aspect Ratio (EAR) and head-pose stability are computed client-side to protect your privacy.
            </p>
          </div>
          <div className="flex items-start gap-2.5">
            <ShieldCheck className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <p className="text-xs">
              <strong className="text-slate-100">Screening Indicator Only:</strong> This assessment evaluates observable markers. It does not replace professional medical or clinical evaluations.
            </p>
          </div>
        </div>

        <div className="flex items-center justify-end gap-3 pt-2">
          {onCancel && (
            <button
              onClick={onCancel}
              className="min-h-[44px] px-4 py-2 text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg transition-colors"
            >
              Cancel
            </button>
          )}
          <button
            onClick={onAccept}
            className="min-h-[44px] flex items-center gap-2 px-5 py-2.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 rounded-lg shadow-lg shadow-indigo-600/20 transition-all"
          >
            I Understand & Consent
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

      </div>
    </div>
  );
};
