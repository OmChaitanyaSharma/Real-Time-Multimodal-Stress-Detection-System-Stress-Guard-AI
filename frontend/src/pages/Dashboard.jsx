import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { stressAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  CartesianGrid,
  ReferenceArea
} from 'recharts';
import { 
  BarChart3, 
  Camera, 
  Clock, 
  FileText, 
  Sparkles, 
  Activity, 
  TrendingUp, 
  CheckCircle2,
  Calendar,
  Layers,
  ArrowRight
} from 'lucide-react';

export const Dashboard = () => {
  const { user } = useAuth();
  const [trends, setTrends] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [trendsRes, historyRes] = await Promise.all([
          stressAPI.getTrends(30),
          stressAPI.getHistory(30),
        ]);
        setTrends(trendsRes.data);
        setHistory(historyRes.data);
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Could not load historical assessment metrics.');
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  // Summary Metrics
  const totalAssessments = history.length;
  const latestAssessment = history[0];
  const avgScore = totalAssessments > 0
    ? Math.round(history.reduce((acc, curr) => acc + curr.fused_stress_score, 0) / totalAssessments * 100)
    : 0;

  // Custom Chart Tooltip
  const CustomChartTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-900 border border-slate-700 p-3 rounded-xl shadow-2xl text-xs space-y-1.5">
          <p className="font-semibold text-slate-200 border-b border-slate-800 pb-1 flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5 text-indigo-400" />
            {data.date}
          </p>
          <p className="text-slate-300">
            Fused Score: <strong className="text-indigo-400">{data.fused_stress_score}%</strong>
          </p>
          {data.facial_stress_score !== null && (
            <p className="text-slate-400">
              Facial Score: <span className="text-sky-300">{data.facial_stress_score}%</span>
            </p>
          )}
          {data.behavioural_stress_score !== null && (
            <p className="text-slate-400">
              Behavioural Score: <span className="text-violet-300">{data.behavioural_stress_score}%</span>
            </p>
          )}
          <span className={`inline-block text-[10px] px-2 py-0.5 rounded-full font-semibold ${
            data.stress_category === 'High' ? 'bg-rose-500/20 text-rose-300' : data.stress_category === 'Moderate' ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'
          }`}>
            {data.stress_category} Stress Indicator
          </span>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8 animate-fade-in">
      
      {/* Welcome Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            Assessment Analytics & Trends
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Welcome back, <strong className="text-slate-200">{user?.full_name}</strong>. Historical monitoring and longitudinal indicators.
          </p>
        </div>

        <Link
          to="/assessment"
          className="flex items-center gap-2 px-5 py-2.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 rounded-xl shadow-lg shadow-indigo-600/20 transition-all shrink-0"
        >
          <Camera className="w-4 h-4" />
          Start New Assessment
        </Link>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">Total Assessments</span>
          <div className="flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-white">{totalAssessments}</span>
            <Activity className="w-5 h-5 text-indigo-400" />
          </div>
          <span className="text-[11px] text-slate-500">Cross-modal records saved</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">Latest Stress Index</span>
          <div className="flex items-baseline justify-between">
            <span className={`text-3xl font-extrabold ${
              latestAssessment?.stress_category === 'High' ? 'text-rose-400' : latestAssessment?.stress_category === 'Moderate' ? 'text-amber-400' : 'text-emerald-400'
            }`}>
              {latestAssessment ? `${Math.round(latestAssessment.fused_stress_score * 100)}%` : '0%'}
            </span>
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${
              latestAssessment?.stress_category === 'High' ? 'bg-rose-500/10 text-rose-400' : latestAssessment?.stress_category === 'Moderate' ? 'bg-amber-500/10 text-amber-400' : 'bg-emerald-500/10 text-emerald-400'
            }`}>
              {latestAssessment?.stress_category || 'None'}
            </span>
          </div>
          <span className="text-[11px] text-slate-500">Most recent assessment</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">Average Historical Score</span>
          <div className="flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-slate-100">{avgScore}%</span>
            <TrendingUp className="w-5 h-5 text-violet-400" />
          </div>
          <span className="text-[11px] text-slate-500">Longitudinal baseline</span>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl space-y-2">
          <span className="text-xs font-medium text-slate-400">Modality Coverage</span>
          <div className="flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-white">100%</span>
            <Layers className="w-5 h-5 text-teal-400" />
          </div>
          <span className="text-[11px] text-slate-500">Vision + Lifestyle Ensemble</span>
        </div>

      </div>

      {/* Recharts Longitudinal Trend Chart */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-indigo-400" />
              Longitudinal Stress Score Progression
            </h3>
            <p className="text-xs text-slate-400">
              Tracking fused indicators against individual modality contributions over time
            </p>
          </div>

          <div className="flex items-center gap-4 text-[11px]">
            <span className="flex items-center gap-1.5 text-indigo-400">
              <span className="w-3 h-0.5 bg-indigo-500 inline-block"></span>
              Fused Score
            </span>
            <span className="flex items-center gap-1.5 text-sky-400">
              <span className="w-3 h-0.5 bg-sky-400 border-dashed inline-block"></span>
              Facial
            </span>
            <span className="flex items-center gap-1.5 text-violet-400">
              <span className="w-3 h-0.5 bg-violet-400 border-dashed inline-block"></span>
              Behavioural
            </span>
          </div>
        </div>

        <div className="h-72 w-full pt-2">
          {trends.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trends} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis 
                  dataKey="date" 
                  stroke="#64748b" 
                  tick={{ fill: '#94a3b8', fontSize: 10 }}
                />
                <YAxis 
                  stroke="#64748b" 
                  domain={[0, 100]} 
                  tick={{ fill: '#94a3b8', fontSize: 10 }}
                  tickFormatter={(v) => `${v}%`}
                />
                <Tooltip content={<CustomChartTooltip />} />
                
                {/* Visual Category Background Bands */}
                <ReferenceArea y1={0} y2={38} fill="#10b981" fillOpacity={0.04} />
                <ReferenceArea y1={38} y2={52} fill="#f59e0b" fillOpacity={0.04} />
                <ReferenceArea y1={52} y2={100} fill="#f43f5e" fillOpacity={0.04} />

                {/* Lines */}
                <Line 
                  type="monotone" 
                  dataKey="fused_stress_score" 
                  stroke="#6366f1" 
                  strokeWidth={3} 
                  dot={{ fill: '#6366f1', r: 4 }} 
                  activeDot={{ r: 6 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="facial_stress_score" 
                  stroke="#38bdf8" 
                  strokeWidth={1.5} 
                  strokeDasharray="4 4"
                  dot={false}
                />
                <Line 
                  type="monotone" 
                  dataKey="behavioural_stress_score" 
                  stroke="#a855f7" 
                  strokeWidth={1.5} 
                  strokeDasharray="4 4"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-slate-500">
              No historical trends recorded yet. Run your first assessment!
            </div>
          )}
        </div>
      </div>

      {/* Assessment History Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl space-y-4 p-6">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <Clock className="w-4 h-4 text-indigo-400" />
            Assessment Log History
          </h3>
          <span className="text-xs text-slate-400">{history.length} Records</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/60 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Date & Time</th>
                <th className="py-3 px-4">Modality Mode</th>
                <th className="py-3 px-4">Score</th>
                <th className="py-3 px-4">Classification</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {history.map((item) => (
                <tr key={item.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3.5 px-4 font-medium text-slate-200">
                    {new Date(item.timestamp).toLocaleString()}
                  </td>
                  <td className="py-3.5 px-4 capitalize">
                    <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-slate-800 text-slate-300">
                      {item.modality_mode.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-bold text-slate-100">
                    {Math.round(item.fused_stress_score * 100)}%
                  </td>
                  <td className="py-3.5 px-4">
                    <span className={`inline-block text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                      item.stress_category === 'High' 
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' 
                        : item.stress_category === 'Moderate' 
                        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' 
                        : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    }`}>
                      {item.stress_category} Stress
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-400">
                    {Math.round(item.confidence * 100)}%
                  </td>
                  <td className="py-3.5 px-4 text-right space-x-2">
                    <Link
                      to={`/report/${item.id}`}
                      aria-label={`View report for assessment on ${new Date(item.timestamp).toLocaleDateString()}`}
                      className="inline-flex items-center justify-center gap-1.5 min-h-[44px] px-3 py-2 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors"
                    >
                      <FileText className="w-3.5 h-3.5 text-indigo-400" />
                      Report
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
