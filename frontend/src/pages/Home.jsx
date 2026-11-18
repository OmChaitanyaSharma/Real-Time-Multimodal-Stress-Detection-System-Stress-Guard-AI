import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Activity, 
  Camera, 
  BarChart2, 
  Cpu, 
  ShieldCheck, 
  Sparkles, 
  ArrowRight,
  Eye,
  Layers,
  CheckCircle2,
  Lock,
  Flame,
  Moon
} from 'lucide-react';

export const Home = () => {
  const { user } = useAuth();

  return (
    <div className="space-y-20 sm:space-y-28 py-10 sm:py-16 overflow-x-hidden">
      
      {/* Editorial Hero Section */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6 sm:space-y-8">
        
        {/* Subtle Overline Tag */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-mono font-medium tracking-wide">
          <span className="w-2 h-2 rounded-full bg-indigo-400 animate-ping"></span>
          B.Tech CSE Major Project • Multimodal Architecture
        </div>
        
        {/* Anti-Convergence Headline */}
        <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-[1.12]">
          Real-Time Multimodal <br className="hidden sm:inline" />
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-300 via-violet-200 to-teal-200">
            Stress Detection & Saliency Analysis
          </span>
        </h1>

        <p className="text-sm sm:text-base lg:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed font-normal">
          Synthesizing observable facial kinematics and ocular fatigue with daily lifestyle rhythms through 
          decision-level machine learning and Explainable AI (<span className="text-indigo-300 font-mono">SHAP</span> & <span className="text-violet-300 font-mono">Grad-CAM</span>).
        </p>

        {/* Ergonomic Mobile-First Action Area */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4 max-w-md mx-auto sm:max-w-none">
          {user ? (
            <Link
              to="/assessment"
              className="w-full sm:w-auto min-h-[48px] flex items-center justify-center gap-2.5 px-7 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs sm:text-sm shadow-xl shadow-indigo-600/25 transition-all duration-300 hover:scale-[1.02]"
            >
              Start Multimodal Assessment
              <ArrowRight className="w-4 h-4" />
            </Link>
          ) : (
            <>
              <Link
                to="/login"
                className="w-full sm:w-auto min-h-[48px] flex items-center justify-center gap-2.5 px-7 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs sm:text-sm shadow-xl shadow-indigo-600/25 transition-all duration-300 hover:scale-[1.02]"
              >
                Launch Studio / Pre-Seeded Demo
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/benchmarks"
                className="w-full sm:w-auto min-h-[48px] flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 font-semibold text-xs sm:text-sm border border-slate-800 hover:border-slate-700 transition-all duration-200"
              >
                <Cpu className="w-4 h-4 text-indigo-400" />
                Algorithm Benchmarks
              </Link>
            </>
          )}
        </div>

        {/* Live System Guarantees Strip */}
        <div className="pt-6 flex flex-wrap items-center justify-center gap-6 text-[11px] font-mono text-slate-400">
          <span className="flex items-center gap-1.5">
            <Lock className="w-3.5 h-3.5 text-emerald-400" />
            Zero Video Storage
          </span>
          <span className="flex items-center gap-1.5">
            <Cpu className="w-3.5 h-3.5 text-indigo-400" />
            &lt;30ms CPU Inference
          </span>
          <span className="flex items-center gap-1.5">
            <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
            Non-Diagnostic Screening
          </span>
        </div>
      </section>

      {/* Asymmetric 60/40 Split Architecture Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
          
          {/* 60% Anchor: Multimodal Paradigm Breakdown */}
          <div className="lg:col-span-7 bg-slate-900/70 border border-slate-800 rounded-3xl p-6 sm:p-10 space-y-6 flex flex-col justify-between shadow-2xl">
            <div className="space-y-4">
              <span className="text-xs font-mono text-indigo-400 font-semibold tracking-wider uppercase">
                Dual-Modality Synergy
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                Why Unimodal Stress Classifiers Fail
              </h2>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                Computer vision alone cannot distinguish a deliberate social smile from genuine relaxation ("masked depression"). 
                Self-reported surveys alone lack real-time physiological grounding. StressGuard AI resolves this by binding 
                transient facial landmarks and Eye Aspect Ratio (EAR) with 8 validated lifestyle determinants.
              </p>
            </div>

            {/* Interactive Metrics Comparison */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800/80 space-y-2">
                <div className="flex items-center gap-2 text-indigo-400 font-semibold text-xs">
                  <Camera className="w-4 h-4" />
                  Visual Modality
                </div>
                <p className="text-[11px] text-slate-400 leading-normal">
                  468-landmark mesh, Eye Aspect Ratio fatigue detection, and deep 7-class EmotionCNN.
                </p>
              </div>

              <div className="bg-slate-950/80 p-4 rounded-2xl border border-slate-800/80 space-y-2">
                <div className="flex items-center gap-2 text-violet-400 font-semibold text-xs">
                  <BarChart2 className="w-4 h-4" />
                  Behavioural Modality
                </div>
                <p className="text-[11px] text-slate-400 leading-normal">
                  Circadian sleep duration, screen exposure, workload pressure, and physical buffering.
                </p>
              </div>
            </div>

            {/* Dissonance Rule Callout */}
            <div className="p-4 rounded-2xl bg-indigo-950/30 border border-indigo-500/25 text-xs text-indigo-200 flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
              <p className="leading-relaxed text-[11px]">
                <strong>Automated Dissonance Detection:</strong> If a user reports critical workload strain (sleep &lt; 4h, pressure = 5) while maintaining a smiling facial expression, the decision fusion engine reweights behavioural signals to 75% to eliminate false negatives.
              </p>
            </div>
          </div>

          {/* 40% Lateral Anchor: Real ML Benchmarks Card */}
          <div className="lg:col-span-5 bg-gradient-to-b from-slate-900 to-slate-950 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6 flex flex-col justify-between shadow-2xl">
            <div className="space-y-2">
              <span className="text-xs font-mono text-emerald-400 font-semibold tracking-wider uppercase">
                Empirical Validation
              </span>
              <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                Model Cross-Validation
              </h3>
              <p className="text-xs text-slate-400">
                Trained on standardized SWELL-KW and academic stress protocols (N=3000 samples, 20% holdout).
              </p>
            </div>

            <div className="space-y-3 font-mono text-xs">
              {[
                { name: 'Support Vector Machine (RBF)', acc: '83.67%', auc: '0.956', highlight: true },
                { name: 'XGBoost Classifier', acc: '83.17%', auc: '0.951', highlight: false },
                { name: 'Logistic Regression (L2)', acc: '82.33%', auc: '0.957', highlight: false },
                { name: 'Random Forest (150 trees)', acc: '80.83%', auc: '0.948', highlight: false },
              ].map((m, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-xl border flex items-center justify-between ${
                    m.highlight
                      ? 'bg-indigo-600/15 border-indigo-500/40 text-indigo-200 font-bold'
                      : 'bg-slate-950/60 border-slate-800 text-slate-300'
                  }`}
                >
                  <span className="text-[11px] truncate">{m.name}</span>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className="text-emerald-400">{m.acc}</span>
                    <span className="text-slate-500 text-[10px]">AUC {m.auc}</span>
                  </div>
                </div>
              ))}
            </div>

            <Link
              to="/benchmarks"
              className="inline-flex items-center justify-center gap-2 w-full py-2.5 text-xs font-semibold text-slate-300 hover:text-white bg-slate-800/80 hover:bg-slate-800 rounded-xl transition-all"
            >
              Inspect Confusion Matrices & ROC Curves
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

        </div>
      </section>

      {/* Explainable AI (XAI) Deep-Dive Row */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-slate-900/60 border border-slate-800 rounded-3xl p-6 sm:p-10 space-y-8">
          <div className="max-w-2xl space-y-2">
            <span className="text-xs font-mono text-violet-400 font-semibold tracking-wider uppercase">
              Zero Black-Box Opacity
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
              Bi-Directional Explainable AI
            </h2>
            <p className="text-xs sm:text-sm text-slate-400">
              Users and academic evaluators understand exactly which physiological and lifestyle factors drove the prediction.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Grad-CAM Pillar */}
            <div className="bg-slate-950 p-6 rounded-2xl border border-slate-800/80 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 flex items-center justify-center">
                <Eye className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">Grad-CAM Convolutional Heatmaps</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Backpropagating classification gradients into the terminal 256-channel convolution layer maps attentive regions onto the corrugator supercilii (brow tension) and orbicularis oculi (eyelid strain).
              </p>
            </div>

            {/* SHAP Pillar */}
            <div className="bg-slate-950 p-6 rounded-2xl border border-slate-800/80 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-violet-500/10 text-violet-400 border border-violet-500/20 flex items-center justify-center">
                <Layers className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">SHAP Additive Factor Attribution</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Game-theoretic Shapley values isolate the exact positive contribution of sleep deprivation and work pressure against the protective buffering of physical activity and rest intervals.
              </p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
};
