import React, { useState } from 'react';
import { 
  Moon, 
  Monitor, 
  Briefcase, 
  Flame, 
  Dumbbell, 
  Coffee, 
  Smile, 
  AlertCircle,
  ArrowRight,
  ArrowLeft,
  Sparkles
} from 'lucide-react';

export const QuestionnaireWizard = ({ onComplete, initialValues = null, isSubmitting = false }) => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState(initialValues || {
    sleep_hours: 7.0,
    screen_time_hours: 6.5,
    work_study_hours: 7.0,
    academic_work_pressure: 3,
    physical_activity_mins: 30,
    break_frequency: 3,
    self_reported_mood: 3,
    perceived_stress_level: 3,
  });

  const handleChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: parseFloat(value),
    }));
  };

  const handleNext = () => setStep((s) => Math.min(3, s + 1));
  const handlePrev = () => setStep((s) => Math.max(1, s - 1));

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onComplete) {
      onComplete(formData);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 sm:p-7 space-y-6 shadow-xl">
      
      {/* Wizard Header & Progress Dots */}
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-4">
        <div>
          <h4 className="text-sm font-bold text-slate-100">Lifestyle Survey Wizard</h4>
          <p className="text-[11px] text-slate-400 font-mono">
            Phase {step} of 3: {step === 1 ? 'Sleep & Screen Rest' : step === 2 ? 'Workload & Activity' : 'Subjective Wellbeing'}
          </p>
        </div>
        <div className="flex items-center gap-1.5">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`h-2 rounded-full transition-all duration-300 ${
                step === s ? 'bg-indigo-500 w-8' : step > s ? 'bg-emerald-500 w-3' : 'bg-slate-800 w-3'
              }`}
            />
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* STEP 1: Sleep & Screen Time */}
        {step === 1 && (
          <div className="space-y-6 animate-fade-in">
            {/* Sleep Hours */}
            <div className="space-y-2.5">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-2">
                  <Moon className="w-4 h-4 text-indigo-400" />
                  Nightly Sleep Duration
                </span>
                <span className="font-mono font-bold text-indigo-300 text-sm">{formData.sleep_hours} hrs</span>
              </div>
              <input
                type="range"
                min="3"
                max="12"
                step="0.5"
                value={formData.sleep_hours}
                onChange={(e) => handleChange('sleep_hours', e.target.value)}
                className="w-full accent-indigo-500 h-3 bg-slate-950 rounded-lg cursor-pointer"
                aria-label="Nightly Sleep Duration"
              />
              <div className="flex justify-between text-[10px] font-mono text-slate-500">
                <span>3h (Severe Deficit)</span>
                <span>7-8h (Healthy)</span>
                <span>12h (Prolonged)</span>
              </div>
            </div>

            {/* Screen Time Hours */}
            <div className="space-y-2.5 pt-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-2">
                  <Monitor className="w-4 h-4 text-violet-400" />
                  Daily Screen Exposure (Work + Leisure)
                </span>
                <span className="font-mono font-bold text-violet-300 text-sm">{formData.screen_time_hours} hrs</span>
              </div>
              <input
                type="range"
                min="1"
                max="16"
                step="0.5"
                value={formData.screen_time_hours}
                onChange={(e) => handleChange('screen_time_hours', e.target.value)}
                className="w-full accent-violet-500 h-3 bg-slate-950 rounded-lg cursor-pointer"
                aria-label="Daily Screen Time"
              />
              <div className="flex justify-between text-[10px] font-mono text-slate-500">
                <span>1h (Minimal)</span>
                <span>6-8h (Average)</span>
                <span>16h (Heavy Glare)</span>
              </div>
            </div>
          </div>
        )}

        {/* STEP 2: Workload, Physical Activity & Breaks */}
        {step === 2 && (
          <div className="space-y-5 animate-fade-in">
            {/* Study / Work Hours */}
            <div className="space-y-2.5">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-2">
                  <Briefcase className="w-4 h-4 text-sky-400" />
                  Daily Study / Workload Duration
                </span>
                <span className="font-mono font-bold text-sky-300 text-sm">{formData.work_study_hours} hrs</span>
              </div>
              <input
                type="range"
                min="2"
                max="15"
                step="0.5"
                value={formData.work_study_hours}
                onChange={(e) => handleChange('work_study_hours', e.target.value)}
                className="w-full accent-sky-500 h-3 bg-slate-950 rounded-lg cursor-pointer"
                aria-label="Study or Work Duration"
              />
            </div>

            {/* Academic / Work Pressure */}
            <div className="space-y-2.5 pt-1">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-2">
                  <Flame className="w-4 h-4 text-amber-400" />
                  Subjective Academic / Work Pressure
                </span>
                <span className="font-mono font-bold text-amber-300 text-sm">Level {formData.academic_work_pressure} / 5</span>
              </div>
              <div className="grid grid-cols-5 gap-2" role="radiogroup" aria-label="Academic or Work Pressure Level">
                {[1, 2, 3, 4, 5].map((lvl) => (
                  <button
                    key={lvl}
                    type="button"
                    role="radio"
                    aria-checked={formData.academic_work_pressure === lvl}
                    aria-label={`Pressure level ${lvl} of 5`}
                    onClick={() => handleChange('academic_work_pressure', lvl)}
                    className={`min-h-[44px] py-2 text-xs font-mono font-bold rounded-xl border transition-all ${
                      formData.academic_work_pressure === lvl
                        ? 'bg-amber-500/20 text-amber-300 border-amber-500/50 shadow-md shadow-amber-500/10'
                        : 'bg-slate-950 text-slate-400 border-slate-800 hover:bg-slate-800'
                    }`}
                  >
                    {lvl}
                  </button>
                ))}
              </div>
              <div className="flex justify-between text-[10px] font-mono text-slate-500">
                <span>1: Low</span>
                <span>3: Moderate</span>
                <span>5: Extreme</span>
              </div>
            </div>

            {/* Physical Activity Minutes */}
            <div className="space-y-2.5 pt-1">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-2">
                  <Dumbbell className="w-4 h-4 text-emerald-400" />
                  Physical Activity / Exercise
                </span>
                <span className="font-mono font-bold text-emerald-300 text-sm">{formData.physical_activity_mins} mins</span>
              </div>
              <input
                type="range"
                min="0"
                max="120"
                step="5"
                value={formData.physical_activity_mins}
                onChange={(e) => handleChange('physical_activity_mins', e.target.value)}
                className="w-full accent-emerald-500 h-3 bg-slate-950 rounded-lg cursor-pointer"
                aria-label="Physical Activity Minutes"
              />
            </div>

            {/* Break Frequency */}
            <div className="space-y-2.5 pt-1">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-2">
                  <Coffee className="w-4 h-4 text-orange-400" />
                  Break Regularity
                </span>
                <span className="font-mono font-bold text-orange-300 text-sm">Rating {formData.break_frequency} / 5</span>
              </div>
              <div className="grid grid-cols-5 gap-2" role="radiogroup" aria-label="Break Frequency Rating">
                {[1, 2, 3, 4, 5].map((lvl) => (
                  <button
                    key={lvl}
                    type="button"
                    role="radio"
                    aria-checked={formData.break_frequency === lvl}
                    aria-label={`Break frequency rating ${lvl} of 5`}
                    onClick={() => handleChange('break_frequency', lvl)}
                    className={`min-h-[44px] py-2 text-xs font-mono font-bold rounded-xl border transition-all ${
                      formData.break_frequency === lvl
                        ? 'bg-orange-500/20 text-orange-300 border-orange-500/50 shadow-md shadow-orange-500/10'
                        : 'bg-slate-950 text-slate-400 border-slate-800 hover:bg-slate-800'
                    }`}
                  >
                    {lvl}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* STEP 3: Mood & Perceived Stress */}
        {step === 3 && (
          <div className="space-y-5 animate-fade-in">
            {/* Self-reported Mood */}
            <div className="space-y-2.5">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-2">
                  <Smile className="w-4 h-4 text-teal-400" />
                  Self-Reported Mood State
                </span>
                <span className="font-mono font-bold text-teal-300 text-sm">Score {formData.self_reported_mood} / 5</span>
              </div>
              <div className="grid grid-cols-5 gap-2" role="radiogroup" aria-label="Self-Reported Mood State">
                {[
                  { lvl: 1, label: 'Low' },
                  { lvl: 2, label: 'Mild' },
                  { lvl: 3, label: 'Neutral' },
                  { lvl: 4, label: 'Good' },
                  { lvl: 5, label: 'Upbeat' },
                ].map((item) => (
                  <button
                    key={item.lvl}
                    type="button"
                    role="radio"
                    aria-checked={formData.self_reported_mood === item.lvl}
                    aria-label={`Mood rating ${item.lvl} of 5 (${item.label})`}
                    onClick={() => handleChange('self_reported_mood', item.lvl)}
                    className={`min-h-[48px] py-2 text-xs font-semibold rounded-xl border flex flex-col items-center justify-center gap-0.5 transition-all ${
                      formData.self_reported_mood === item.lvl
                        ? 'bg-teal-500/20 text-teal-300 border-teal-500/50 shadow-md shadow-teal-500/10'
                        : 'bg-slate-950 text-slate-400 border-slate-800 hover:bg-slate-800'
                    }`}
                  >
                    <span className="font-mono font-bold">{item.lvl}</span>
                    <span className="text-[9px] font-normal tracking-tight">{item.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Perceived Stress Level */}
            <div className="space-y-2.5 pt-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-slate-200 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-rose-400" />
                  Perceived Stress Index (PSS-8 Baseline)
                </span>
                <span className="font-mono font-bold text-rose-300 text-sm">Rating {formData.perceived_stress_level} / 5</span>
              </div>
              <div className="grid grid-cols-5 gap-2" role="radiogroup" aria-label="Perceived Stress Index">
                {[
                  { lvl: 1, label: 'Relaxed' },
                  { lvl: 2, label: 'Mild' },
                  { lvl: 3, label: 'Moderate' },
                  { lvl: 4, label: 'High' },
                  { lvl: 5, label: 'Severe' },
                ].map((item) => (
                  <button
                    key={item.lvl}
                    type="button"
                    role="radio"
                    aria-checked={formData.perceived_stress_level === item.lvl}
                    aria-label={`Perceived stress rating ${item.lvl} of 5 (${item.label})`}
                    onClick={() => handleChange('perceived_stress_level', item.lvl)}
                    className={`min-h-[48px] py-2 text-xs font-semibold rounded-xl border flex flex-col items-center justify-center gap-0.5 transition-all ${
                      formData.perceived_stress_level === item.lvl
                        ? 'bg-rose-500/20 text-rose-300 border-rose-500/50 shadow-md shadow-rose-500/10'
                        : 'bg-slate-950 text-slate-400 border-slate-800 hover:bg-slate-800'
                    }`}
                  >
                    <span className="font-mono font-bold">{item.lvl}</span>
                    <span className="text-[9px] font-normal tracking-tight">{item.label}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Wizard Navigation: 48px Touch Targets for Ergonomics */}
        <div className="flex items-center justify-between pt-4 border-t border-slate-800/80 gap-3">
          {step > 1 ? (
            <button
              type="button"
              onClick={handlePrev}
              className="min-h-[44px] flex items-center gap-1.5 px-4 py-2.5 text-xs font-semibold text-slate-300 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-xl transition-all"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Previous
            </button>
          ) : (
            <div></div>
          )}

          {step < 3 ? (
            <button
              type="button"
              onClick={handleNext}
              className="min-h-[44px] flex items-center gap-1.5 px-6 py-2.5 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-500 rounded-xl transition-all shadow-md shadow-indigo-600/20"
            >
              Next Step
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              type="submit"
              disabled={isSubmitting}
              className="min-h-[48px] flex items-center gap-2 px-6 py-3 text-xs font-bold text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 rounded-xl shadow-lg shadow-indigo-600/20 disabled:opacity-50 transition-all active:scale-[0.98]"
            >
              {isSubmitting ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Evaluating Features...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  Evaluate Survey Inputs
                </>
              )}
            </button>
          )}
        </div>

      </form>
    </div>
  );
};
