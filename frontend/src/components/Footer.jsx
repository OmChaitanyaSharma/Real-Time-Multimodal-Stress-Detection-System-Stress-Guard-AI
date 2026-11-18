import React from 'react';
import { ShieldAlert, BookOpen, HeartHandshake } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="bg-slate-950 border-t border-slate-900 text-slate-400 text-xs py-8 no-print mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        
        {/* Ethical / Medical Notice Box */}
        <div className="bg-slate-900/60 border border-slate-800/80 rounded-xl p-4 flex flex-col sm:flex-row items-start sm:items-center gap-3 text-slate-300">
          <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20 shrink-0">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div className="space-y-1">
            <p className="font-semibold text-slate-200">
              Academic Research & Non-Diagnostic Awareness Notice
            </p>
            <p className="text-slate-400 leading-relaxed text-[11px]">
              This application is developed as a final-year B.Tech Computer Science & Engineering major project. 
              The system identifies potential stress indicators by analyzing observable facial patterns and lifestyle responses. 
              It is designed exclusively for wellness awareness and educational demonstration. It is not an authorized medical, 
              psychological, or clinical diagnosis. If you experience severe or chronic distress, consult a qualified healthcare professional.
            </p>
          </div>
        </div>

        {/* Footer bottom bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-900 text-slate-500">
          <p>
            Real-Time Multimodal Stress Detection and Analysis System &copy; 2026.
          </p>
          <div className="flex items-center gap-6">
            <span className="flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
              B.Tech CSE Major Project
            </span>
            <span className="flex items-center gap-1.5">
              <HeartHandshake className="w-3.5 h-3.5 text-rose-400" />
              Privacy-Preserving Biometrics
            </span>
          </div>
        </div>

      </div>
    </footer>
  );
};
