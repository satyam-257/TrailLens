import React from 'react';
import { 
  Compass, 
  BookOpen, 
  Trophy, 
  Flame, 
  TreePine, 
  Cpu, 
  Info,
  Sparkles
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, userProfile, onOpenSpotModal, onOpenHUD }) {
  const level = userProfile?.level || 1;
  const title = userProfile?.title || 'Trail Scout';
  const xp = userProfile?.total_xp || 0;
  const streak = userProfile?.streak_days || 0;

  return (
    <header className="sticky top-0 z-40 backdrop-blur-xl bg-slate-950/80 border-b border-emerald-950/40 px-4 py-3">
      <div className="max-w-6xl mx-auto flex items-center justify-between gap-2">
        {/* Brand */}
        <div 
          onClick={() => setActiveTab('home')}
          className="flex items-center gap-2.5 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 p-0.5 shadow-lg shadow-emerald-900/40 group-hover:scale-105 transition-transform flex items-center justify-center">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center text-xl">
              🌲
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-display font-extrabold text-xl tracking-tight text-white flex items-center gap-1.5">
                Trail<span className="text-emerald-400">Lens</span>
              </span>
              <span className="inline-flex items-center gap-1 text-[10px] font-bold uppercase tracking-wider bg-emerald-950/80 text-emerald-400 border border-emerald-800/50 px-2 py-0.5 rounded-full">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                Offline AI
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium hidden sm:block">
              Identify birds. Put your phone down.
            </p>
          </div>
        </div>

        {/* Navigation Tabs (Desktop & Tablet) */}
        <nav className="hidden md:flex items-center gap-1 bg-slate-900/90 border border-slate-800/80 p-1 rounded-2xl">
          <button
            onClick={() => setActiveTab('home')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'home' 
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-900/50' 
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Compass className="w-4 h-4" />
            Explore
          </button>
          <button
            onClick={() => setActiveTab('guide')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'guide' 
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-900/50' 
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <BookOpen className="w-4 h-4" />
            Field Guide
          </button>
          <button
            onClick={() => setActiveTab('gamification')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'gamification' 
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-900/50' 
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Flame className="w-4 h-4 text-amber-400" />
            Streaks & Badges
          </button>
          <button
            onClick={() => setActiveTab('leaderboard')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'leaderboard' 
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-900/50' 
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Trophy className="w-4 h-4 text-amber-400" />
            Leaderboard
          </button>
          <button
            onClick={() => setActiveTab('about')}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              activeTab === 'about' 
                ? 'bg-emerald-600 text-white shadow-md shadow-emerald-900/50' 
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Info className="w-4 h-4" />
            Open AI
          </button>
        </nav>

        {/* User Stats & Action Pill */}
        <div className="flex items-center gap-2">
          {/* Streak pill */}
          <div 
            onClick={() => setActiveTab('gamification')}
            className="flex items-center gap-1 bg-amber-950/30 border border-amber-800/40 px-2.5 py-1 rounded-full cursor-pointer hover:bg-amber-900/30 transition-colors"
            title="Outdoor streak days"
          >
            <span className="streak-flame text-sm">🔥</span>
            <span className="text-xs font-extrabold text-amber-300 font-display">
              {streak}d
            </span>
          </div>

          {/* Level & XP pill */}
          <div 
            onClick={() => setActiveTab('gamification')}
            className="hidden sm:flex items-center gap-1.5 bg-slate-900/90 border border-emerald-900/40 px-3 py-1 rounded-full cursor-pointer hover:border-emerald-500/50 transition-colors"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span className="text-xs font-bold text-slate-200">
              Lv.{level}
            </span>
            <span className="text-[11px] text-emerald-400 font-medium">
              {xp} XP
            </span>
          </div>

          {/* Developer HUD Button */}
          <button
            onClick={onOpenHUD}
            className="p-2 text-slate-400 hover:text-emerald-400 hover:bg-slate-900 rounded-xl transition-colors border border-slate-800/60"
            title="Model Diagnostics & Performance HUD"
          >
            <Cpu className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Mobile Sub Navigation Bar */}
      <div className="md:hidden flex items-center justify-around pt-2 mt-2 border-t border-slate-900 text-xs">
        <button
          onClick={() => setActiveTab('home')}
          className={`flex flex-col items-center gap-0.5 py-1 px-2 ${activeTab === 'home' ? 'text-emerald-400 font-bold' : 'text-slate-400'}`}
        >
          <Compass className="w-4 h-4" />
          <span>Explore</span>
        </button>
        <button
          onClick={() => setActiveTab('guide')}
          className={`flex flex-col items-center gap-0.5 py-1 px-2 ${activeTab === 'guide' ? 'text-emerald-400 font-bold' : 'text-slate-400'}`}
        >
          <BookOpen className="w-4 h-4" />
          <span>Field Guide</span>
        </button>
        <button
          onClick={() => setActiveTab('gamification')}
          className={`flex flex-col items-center gap-0.5 py-1 px-2 ${activeTab === 'gamification' ? 'text-emerald-400 font-bold' : 'text-slate-400'}`}
        >
          <Flame className="w-4 h-4 text-amber-400" />
          <span>Badges</span>
        </button>
        <button
          onClick={() => setActiveTab('leaderboard')}
          className={`flex flex-col items-center gap-0.5 py-1 px-2 ${activeTab === 'leaderboard' ? 'text-emerald-400 font-bold' : 'text-slate-400'}`}
        >
          <Trophy className="w-4 h-4 text-amber-400" />
          <span>Ranks</span>
        </button>
        <button
          onClick={() => setActiveTab('about')}
          className={`flex flex-col items-center gap-0.5 py-1 px-2 ${activeTab === 'about' ? 'text-emerald-400 font-bold' : 'text-slate-400'}`}
        >
          <Info className="w-4 h-4" />
          <span>About</span>
        </button>
      </div>
    </header>
  );
}
