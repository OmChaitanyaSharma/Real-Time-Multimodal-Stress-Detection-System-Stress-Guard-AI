import React from 'react';
import { 
  Moon, 
  Coffee, 
  Briefcase, 
  Dumbbell, 
  Wind, 
  HeartHandshake, 
  Sparkles,
  ChevronRight
} from 'lucide-react';

export const RecommendationCard = ({ recommendation }) => {
  const { category, title, description, priority } = recommendation;

  const getCategoryConfig = () => {
    switch (category) {
      case 'Sleep':
        return { icon: Moon, color: 'text-indigo-400', bg: 'bg-indigo-500/10', border: 'border-indigo-500/20' };
      case 'Breaks':
        return { icon: Coffee, color: 'text-orange-400', bg: 'bg-orange-500/10', border: 'border-orange-500/20' };
      case 'Workload':
        return { icon: Briefcase, color: 'text-sky-400', bg: 'bg-sky-500/10', border: 'border-sky-500/20' };
      case 'Physical Activity':
        return { icon: Dumbbell, color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' };
      case 'Mindfulness':
        return { icon: Wind, color: 'text-teal-400', bg: 'bg-teal-500/10', border: 'border-teal-500/20' };
      case 'Support':
        return { icon: HeartHandshake, color: 'text-rose-400', bg: 'bg-rose-500/10', border: 'border-rose-500/20' };
      default:
        return { icon: Sparkles, color: 'text-violet-400', bg: 'bg-violet-500/10', border: 'border-violet-500/20' };
    }
  };

  const config = getCategoryConfig();
  const Icon = config.icon;

  const getPriorityBadge = () => {
    switch (priority) {
      case 'High':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      case 'Medium':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'Low':
      default:
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 hover:border-slate-700/80 rounded-xl p-4 transition-all space-y-2.5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className={`p-2 rounded-lg ${config.bg} ${config.color} border ${config.border}`}>
            <Icon className="w-4 h-4" />
          </div>
          <div>
            <span className="text-[10px] font-semibold tracking-wider text-slate-400 uppercase">
              {category}
            </span>
            <h5 className="text-xs font-bold text-slate-100">{title}</h5>
          </div>
        </div>

        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${getPriorityBadge()}`}>
          {priority} Priority
        </span>
      </div>

      <p className="text-xs text-slate-300 leading-relaxed pl-1">
        {description}
      </p>
    </div>
  );
};
