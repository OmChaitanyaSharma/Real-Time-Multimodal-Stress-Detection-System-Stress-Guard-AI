import React from 'react';
import { Smile, AlertCircle, AlertTriangle, ShieldCheck } from 'lucide-react';

export const StressGauge = ({ score = 0.0, category = 'Low', confidence = 0.85, size = 'lg' }) => {
  const percentage = Math.round(score * 100);

  // Theme styling based on category
  const getTheme = () => {
    switch (category) {
      case 'High':
        return {
          textColor: 'text-rose-400',
          bgColor: 'bg-rose-500/10',
          borderColor: 'border-rose-500/30',
          progressColor: '#f43f5e',
          badgeText: 'High Stress Indicators',
          Icon: AlertTriangle,
          gradient: 'from-rose-500 to-red-600',
        };
      case 'Moderate':
        return {
          textColor: 'text-amber-400',
          bgColor: 'bg-amber-500/10',
          borderColor: 'border-amber-500/30',
          progressColor: '#f59e0b',
          badgeText: 'Moderate Stress Indicators',
          Icon: AlertCircle,
          gradient: 'from-amber-400 to-orange-500',
        };
      case 'Low':
      default:
        return {
          textColor: 'text-emerald-400',
          bgColor: 'bg-emerald-500/10',
          borderColor: 'border-emerald-500/30',
          progressColor: '#10b981',
          badgeText: 'Low Stress Indicators',
          Icon: Smile,
          gradient: 'from-emerald-400 to-teal-500',
        };
    }
  };

  const theme = getTheme();
  const Icon = theme.Icon;

  // SVG circular gauge geometry
  const radius = size === 'sm' ? 44 : 70;
  const strokeWidth = size === 'sm' ? 8 : 12;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center text-center">
      <div className="relative flex items-center justify-center">
        {/* SVG Circular Progress */}
        <svg
          className="transform -rotate-90"
          width={radius * 2 + strokeWidth * 2}
          height={radius * 2 + strokeWidth * 2}
        >
          {/* Background track */}
          <circle
            cx={radius + strokeWidth}
            cy={radius + strokeWidth}
            r={radius}
            stroke="#1e293b"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Colored progress bar */}
          <circle
            cx={radius + strokeWidth}
            cy={radius + strokeWidth}
            r={radius}
            stroke={theme.progressColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center score readout */}
        <div className="absolute flex flex-col items-center justify-center">
          <span className={`font-extrabold tracking-tight ${size === 'sm' ? 'text-2xl' : 'text-4xl'} ${theme.textColor}`}>
            {percentage}%
          </span>
          <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
            Stress Index
          </span>
        </div>
      </div>

      {/* Category Badge */}
      <div className={`mt-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-semibold ${theme.bgColor} ${theme.borderColor} ${theme.textColor}`}>
        <Icon className="w-4 h-4" />
        <span>{theme.badgeText}</span>
      </div>

      {/* Confidence metric */}
      {confidence && (
        <p className="mt-1.5 text-[11px] text-slate-400 flex items-center gap-1">
          <ShieldCheck className="w-3 h-3 text-slate-400" />
          Model Confidence: {Math.round(confidence * 100)}%
        </p>
      )}
    </div>
  );
};
