import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  ReferenceLine, 
  Cell 
} from 'recharts';
import { HelpCircle, TrendingUp, TrendingDown } from 'lucide-react';

export const ShapChart = ({ shapData = [] }) => {
  if (!shapData || shapData.length === 0) {
    return (
      <div className="p-6 text-center text-slate-500 bg-slate-950/40 rounded-xl border border-slate-800">
        No SHAP attribution values available for this assessment.
      </div>
    );
  }

  // Format data for Recharts horizontal bar chart
  const chartData = shapData.map((item) => ({
    name: item.display_name || item.feature,
    value: item.shap_value,
    featureValue: item.value,
    rawName: item.feature,
    isStressElevating: item.shap_value > 0,
  }));

  // Custom Recharts Tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-900 border border-slate-700 p-3 rounded-lg shadow-xl text-xs space-y-1">
          <p className="font-semibold text-slate-100">{data.name}</p>
          <p className="text-slate-400">User Value: <strong className="text-indigo-300">{data.featureValue}</strong></p>
          <div className="flex items-center gap-1.5 pt-1">
            {data.isStressElevating ? (
              <span className="text-rose-400 flex items-center gap-1">
                <TrendingUp className="w-3.5 h-3.5" />
                Impact: +{data.value} (Elevates Stress)
              </span>
            ) : (
              <span className="text-emerald-400 flex items-center gap-1">
                <TrendingDown className="w-3.5 h-3.5" />
                Impact: {data.value} (Mitigates Stress)
              </span>
            )}
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-sm font-semibold text-slate-100">
            Explainable AI: SHAP Feature Importance
          </h4>
          <p className="text-xs text-slate-400">
            Additive Shapley contributions showing factor impact on predicted stress
          </p>
        </div>
        <div className="flex items-center gap-3 text-[11px]">
          <span className="flex items-center gap-1 text-rose-400">
            <span className="w-2.5 h-2.5 rounded-sm bg-rose-500"></span>
            Elevating
          </span>
          <span className="flex items-center gap-1 text-emerald-400">
            <span className="w-2.5 h-2.5 rounded-sm bg-emerald-500"></span>
            Mitigating
          </span>
        </div>
      </div>

      {/* Recharts Horizontal Diverging Bar Chart */}
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 110, bottom: 5 }}
          >
            <XAxis 
              type="number" 
              stroke="#64748b" 
              tick={{ fill: '#94a3b8', fontSize: 10 }}
              tickFormatter={(v) => v.toFixed(2)}
            />
            <YAxis 
              dataKey="name" 
              type="category" 
              stroke="#64748b" 
              tick={{ fill: '#cbd5e1', fontSize: 11 }}
              width={100}
            />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine x={0} stroke="#475569" strokeDasharray="3 3" />
            <Bar dataKey="value" radius={[4, 4, 4, 4]}>
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.value > 0 ? '#f43f5e' : '#10b981'} 
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <p className="text-[11px] text-slate-500 text-center">
        Bars extending to the right (+SHAP) contributed toward higher stress probability, while bars to the left (-SHAP) served as protective lifestyle buffers.
      </p>
    </div>
  );
};
