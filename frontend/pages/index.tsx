import Head from 'next/head'
import React, { useEffect, useState, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  LineChart, Line, CartesianGrid
} from 'recharts'
import { 
  Upload, PieChart, Activity, TrendingUp, Target, 
  Zap, AlertCircle, CheckCircle2, ChevronRight, 
  LayoutDashboard, Database, History, RefreshCw,
  MoreVertical, Search, Bell
} from 'lucide-react'

// --- Interfaces ---
interface StatSummary {
  total_hands: number;
  win_rate: number;
  net_result: number;
}

interface PreflopStats {
  vpip: number;
  pfr: number;
  three_bet: number;
}

interface PostflopStats {
  cbet: number;
  af: number;
}

interface ShowdownStats {
  wtsd: number;
  wsd: number;
}

interface PositionalStats {
  summary: StatSummary;
  preflop: PreflopStats;
  postflop: PostflopStats;
  showdown: ShowdownStats;
}

const API_BASE = 'http://localhost:8000';

// --- UI Components ---

const GlassCard = ({ children, className = "" }: { children: React.ReactNode, className?: string }) => (
  <motion.div 
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className={`bg-white/80 backdrop-blur-md border border-slate-200/50 rounded-2xl shadow-xl shadow-slate-200/40 ${className}`}
  >
    {children}
  </motion.div>
);

const StatBadge = ({ label, value, colorClass = "text-slate-800" }: { label: string, value: any, colorClass?: string }) => (
  <div className="flex flex-col">
    <span className="text-[10px] uppercase tracking-widest font-bold text-slate-400 mb-0.5">{label}</span>
    <span className={`text-lg font-black font-mono ${colorClass}`}>{value}</span>
  </div>
);

// --- Main Application ---

export default function Home() {
  const [data, setData] = useState<Record<string, PositionalStats>>({});
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchStats = useCallback(() => {
    setLoading(true);
    fetch(`${API_BASE}/stats/position`)
      .then(res => res.json())
      .then(json => {
        setData(json);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setError('Connection to backend failed.');
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  const handleFileUpload = async (file: File) => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE}/upload-log/`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        fetchStats();
      } else {
        throw new Error('Upload failed');
      }
    } catch (err) {
      console.error(err);
      alert('Error uploading file.');
    } finally {
      setUploading(false);
    }
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  // Prepare data for visualization
  const chartData = Object.entries(data).map(([pos, stats]) => ({
    name: pos,
    vpip: stats.preflop.vpip,
    pfr: stats.preflop.pfr,
    winRate: stats.summary.win_rate,
    profit: stats.summary.net_result
  }));

  return (
    <div className="min-h-screen bg-[#f8fafc] text-[#1e293b] font-sans selection:bg-indigo-100 selection:text-indigo-600">
      <Head>
        <title>Action Tracker | 1% Better</title>
      </Head>

      {/* --- SIDEBAR --- */}
      <aside className="fixed left-0 top-0 h-full w-20 bg-white border-r border-slate-200/60 z-50 flex flex-col items-center py-8 gap-10">
        <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-200">
          <Zap size={22} fill="currentColor" />
        </div>
        <nav className="flex flex-col gap-6">
          <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl cursor-pointer transition-all hover:bg-indigo-100">
            <LayoutDashboard size={22} />
          </div>
          <div className="p-3 text-slate-400 rounded-xl cursor-pointer transition-all hover:bg-slate-50 hover:text-slate-600">
            <PieChart size={22} />
          </div>
          <div className="p-3 text-slate-400 rounded-xl cursor-pointer transition-all hover:bg-slate-50 hover:text-slate-600">
            <History size={22} />
          </div>
          <div className="p-3 text-slate-400 rounded-xl cursor-pointer transition-all hover:bg-slate-50 hover:text-slate-600">
            <Database size={22} />
          </div>
        </nav>
        <div className="mt-auto p-3 text-slate-300">
          <Bell size={22} />
        </div>
      </aside>

      <div className="pl-20">
        {/* --- HEADER --- */}
        <header className="px-10 py-6 sticky top-0 bg-white/60 backdrop-blur-xl border-b border-slate-200/40 z-40 flex justify-between items-center">
          <div className="flex flex-col">
            <h1 className="text-xl font-black tracking-tight text-slate-900 flex items-center gap-2">
              ACTION TRACKER <span className="px-2 py-0.5 bg-indigo-600 text-[10px] text-white rounded-md">V1.0</span>
            </h1>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="relative group">
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={(e) => e.target.files && handleFileUpload(e.target.files[0])} 
                className="hidden" 
                accept=".txt"
              />
              <button 
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold transition-all ${
                  uploading 
                    ? 'bg-slate-100 text-slate-400' 
                    : 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-lg shadow-indigo-100 active:scale-95'
                }`}
              >
                <Upload size={18} className={uploading ? 'animate-bounce' : ''} />
                {uploading ? 'PARSING ENGINE...' : 'UPLOAD NEW LOG'}
              </button>
            </div>
            <div className="h-10 w-10 rounded-full bg-slate-200 border-2 border-white overflow-hidden shadow-inner">
              <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix" alt="avatar" />
            </div>
          </div>
        </header>

        {/* --- MAIN DASHBOARD --- */}
        <main className="p-10 max-w-[1600px] mx-auto space-y-10">
          
          {/* DRAG & DROP AREA */}
          <motion.div 
            onDragOver={(e) => { e.preventDefault(); setIsDragActive(true); }}
            onDragLeave={() => setIsDragActive(false)}
            onDrop={onDrop}
            animate={{ 
              borderColor: isDragActive ? '#4f46e5' : '#e2e8f0',
              backgroundColor: isDragActive ? '#f5f3ff' : '#ffffff'
            }}
            className="group relative border-2 border-dashed rounded-3xl p-12 transition-all flex flex-col items-center justify-center gap-6 text-center overflow-hidden"
          >
            <div className={`p-4 rounded-2xl transition-all duration-500 ${isDragActive ? 'bg-indigo-600 text-white scale-125' : 'bg-slate-50 text-slate-400 group-hover:bg-indigo-50 group-hover:text-indigo-600'}`}>
              <Upload size={32} />
            </div>
            <div>
              <h3 className="text-xl font-bold text-slate-800">Drag & Drop Hand Histories</h3>
              <p className="text-slate-500 font-medium">Process multiple files in GGPoker .txt format instantly.</p>
            </div>
            {isDragActive && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="absolute inset-0 bg-indigo-600/5 backdrop-blur-[2px] pointer-events-none"
              />
            )}
          </motion.div>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-10">
            {/* LEFT STATS COLUMN */}
            <div className="xl:col-span-2 space-y-10">
              <header className="flex justify-between items-end">
                <div>
                  <h2 className="text-3xl font-black text-slate-900 tracking-tight italic">POSITIONAL INTELLIGENCE</h2>
                  <p className="text-slate-500 font-medium mt-1">Real-time performance metrics across the table.</p>
                </div>
                <div className="flex gap-2">
                  <button className="p-2 text-slate-400 hover:text-slate-900 transition-colors"><RefreshCw size={20} /></button>
                  <button className="p-2 text-slate-400 hover:text-slate-900 transition-colors"><MoreVertical size={20} /></button>
                </div>
              </header>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <AnimatePresence>
                  {Object.entries(data).map(([pos, stats], index) => (
                    <GlassCard key={pos} className="overflow-hidden border-indigo-100/30 group">
                      <div className="p-6 space-y-6">
                        <div className="flex justify-between items-center">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-[10px] font-black text-white">
                              {pos.substring(0, 2).toUpperCase()}
                            </div>
                            <span className="font-black text-slate-800 tracking-tight uppercase">{pos}</span>
                          </div>
                          <span className="text-[10px] font-bold text-slate-400 bg-slate-50 px-2 py-1 rounded-md">
                            {stats.summary.total_hands} HANDS
                          </span>
                        </div>

                        <div className="grid grid-cols-2 gap-x-8 gap-y-6">
                          <div className="space-y-4">
                            <StatBadge label="VPIP" value={`${stats.preflop.vpip}%`} colorClass={stats.preflop.vpip > 30 ? "text-rose-500" : "text-indigo-600"} />
                            <StatBadge label="PFR" value={`${stats.preflop.pfr}%`} />
                            <StatBadge label="3-BET" value={`${stats.preflop.three_bet}%`} />
                          </div>
                          <div className="space-y-4 border-l border-slate-100 pl-8">
                            <StatBadge label="C-BET" value={`${stats.postflop.cbet}%`} />
                            <StatBadge label="AF" value={stats.postflop.af} colorClass={stats.postflop.af > 2.5 ? "text-emerald-500" : "text-slate-800"} />
                            <StatBadge label="WIN %" value={`${stats.summary.win_rate}%`} colorClass="text-emerald-600" />
                          </div>
                        </div>

                        <div className="pt-6 border-t border-slate-100 flex justify-between items-center">
                          <div className="flex items-center gap-2">
                            <TrendingUp size={14} className={stats.summary.net_result >= 0 ? "text-emerald-500" : "text-rose-500"} />
                            <span className="text-xs font-bold text-slate-400 uppercase tracking-tighter">Profit Curve</span>
                          </div>
                          <span className={`text-xl font-black font-mono ${stats.summary.net_result >= 0 ? "text-emerald-600" : "text-rose-600"}`}>
                            {stats.summary.net_result > 0 ? "+" : ""}{stats.summary.net_result.toLocaleString()}
                          </span>
                        </div>
                      </div>
                    </GlassCard>
                  ))}
                </AnimatePresence>
              </div>
            </div>

            {/* RIGHT ANALYTICS COLUMN */}
            <div className="space-y-10">
              <h2 className="text-3xl font-black text-slate-900 tracking-tight italic">DATA VIS</h2>
              
              <GlassCard className="p-8 space-y-8 h-fit sticky top-32">
                <div className="space-y-6">
                  <div className="flex items-center gap-2 text-indigo-600">
                    <Target size={20} />
                    <span className="text-xs font-black uppercase tracking-widest">VPIP vs PFR Gap</span>
                  </div>
                  <div className="h-[250px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 700 }} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fontWeight: 700 }} />
                        <Tooltip 
                          contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                        />
                        <Bar dataKey="vpip" fill="#4f46e5" radius={[4, 4, 0, 0]} barSize={20} />
                        <Bar dataKey="pfr" fill="#e2e8f0" radius={[4, 4, 0, 0]} barSize={20} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="pt-8 border-t border-slate-100 space-y-6">
                  <div className="flex items-center gap-2 text-indigo-600">
                    <Activity size={20} />
                    <span className="text-xs font-black uppercase tracking-widest">Aggression Matrix</span>
                  </div>
                  <div className="h-[250px] w-full flex justify-center items-center">
                    <ResponsiveContainer width="100%" height="100%">
                      <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                        <PolarGrid stroke="#f1f5f9" />
                        <PolarAngleAxis dataKey="name" tick={{ fontSize: 10, fontWeight: 700, fill: '#64748b' }} />
                        <Radar name="VPIP" dataKey="vpip" stroke="#4f46e5" fill="#4f46e5" fillOpacity={0.6} />
                        <Radar name="PFR" dataKey="pfr" stroke="#94a3b8" fill="#94a3b8" fillOpacity={0.1} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </GlassCard>
            </div>
          </div>
        </main>

        <footer className="p-10 border-t border-slate-200/60 mt-20 bg-white">
          <div className="max-w-[1600px] mx-auto flex justify-between items-center opacity-30">
            <div className="flex items-center gap-4 text-[10px] font-black tracking-[0.2em] uppercase italic">
              <span>EST. 2026</span>
              <div className="w-1 h-1 rounded-full bg-slate-900" />
              <span>SYST: STABLE</span>
            </div>
            <div className="text-[10px] font-black uppercase tracking-widest">One Percent Better Every Day</div>
          </div>
        </footer>
      </div>
    </div>
  )
}
