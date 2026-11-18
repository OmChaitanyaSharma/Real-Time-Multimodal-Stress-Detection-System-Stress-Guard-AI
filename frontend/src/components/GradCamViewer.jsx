import React, { useState } from 'react';
import { Eye, Layers, Info, CheckCircle2 } from 'lucide-react';

export const GradCamViewer = ({ gradcamBase64, originalBase64 = null, dominantEmotion = 'neutral' }) => {
  const [viewMode, setViewMode] = useState('overlay'); // 'overlay' or 'split'

  if (!gradcamBase64) {
    return (
      <div className="p-6 text-center text-slate-500 bg-slate-950/40 rounded-xl border border-slate-800">
        No Grad-CAM activation maps available for this modality.
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="space-y-0.5">
          <h4 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <Layers className="w-4 h-4 text-violet-400" />
            Explainable AI: Grad-CAM Saliency Map
          </h4>
          <p className="text-xs text-slate-400">
            Gradient-weighted class activation mapping on deepest CNN convolutional layers
          </p>
        </div>

        {originalBase64 && (
          <div className="flex items-center gap-1 bg-slate-800 p-1 rounded-lg text-xs">
            <button
              onClick={() => setViewMode('overlay')}
              className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                viewMode === 'overlay' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'
              }`}
            >
              Heatmap
            </button>
            <button
              onClick={() => setViewMode('split')}
              className={`px-2.5 py-1 rounded-md font-medium transition-all ${
                viewMode === 'split' ? 'bg-indigo-600 text-white shadow' : 'text-slate-400 hover:text-white'
              }`}
            >
              Side-by-Side
            </button>
          </div>
        )}
      </div>

      {/* Image Display */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4 bg-slate-950 p-4 rounded-xl border border-slate-800">
        {viewMode === 'split' && originalBase64 && (
          <div className="text-center space-y-1.5">
            <div className="w-48 h-48 rounded-xl overflow-hidden border border-slate-700 bg-black flex items-center justify-center">
              <img
                src={originalBase64}
                alt="Original Face Input"
                className="w-full h-full object-cover"
              />
            </div>
            <span className="text-[11px] font-medium text-slate-400">Original Face Crop</span>
          </div>
        )}

        <div className="text-center space-y-1.5">
          <div className="w-48 h-48 rounded-xl overflow-hidden border border-indigo-500/40 shadow-lg shadow-indigo-500/10 bg-black flex items-center justify-center relative">
            <img
              src={gradcamBase64}
              alt="Grad-CAM Activation Heatmap"
              className="w-full h-full object-cover"
            />
            <div className="absolute bottom-2 right-2 bg-slate-950/80 px-2 py-0.5 rounded text-[10px] text-indigo-300 font-semibold border border-indigo-500/30">
              Conv4 ReLU Saliency
            </div>
          </div>
          <span className="text-[11px] font-medium text-slate-300">
            Attentive Regions (<strong className="capitalize text-indigo-300">{dominantEmotion}</strong>)
          </span>
        </div>
      </div>

      {/* Biological Annotation Details */}
      <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80 space-y-2 text-xs text-slate-300">
        <div className="flex items-center gap-2 font-semibold text-slate-200">
          <Info className="w-3.5 h-3.5 text-indigo-400" />
          Neural Activation Interpretation
        </div>
        <p className="text-[11px] text-slate-400 leading-relaxed">
          High-intensity areas (red and yellow spectrum) indicate facial zones that predominantly guided the CNN model toward its classification. 
          In stress states, activation clusters typically concentrate around the <strong>corrugator supercilii</strong> (brow furrowing), 
          the <strong>orbicularis oculi</strong> (eyelid tension / fatigue), and the perioral jaw angles.
        </p>
      </div>

    </div>
  );
};
