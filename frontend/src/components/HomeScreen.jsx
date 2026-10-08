import React from 'react';
import { 
  Camera, 
  TreePine, 
  Flame, 
  Sparkles, 
  Trophy, 
  BookOpen, 
  Clock, 
  Eye, 
  ArrowRight,
  ShieldCheck,
  Zap,
  MapPin
} from 'lucide-react';

export default function HomeScreen({ 
  userProfile, 
  demoSamples, 
  onSpotBird, 
  onSelectDemoBird, 
  onStartTouchGrass,
  onNavigate 
}) {
  const outdoorMinutes = userProfile?.total_outdoor_minutes || 42;
  const discoveredCount = userProfile?.discovered_species_ids?.length || 3;
  const xp = userProfile?.total_xp || 120;
  const streak = userProfile?.streak_days || 4;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Hero Header */}
      <div className="text-center space-y-3 pt-4">
        <div className="inline-flex items-center gap-2 bg-emerald-950/60 border border-emerald-800/40 px-3.5 py-1.5 rounded-full text-xs font-semibold text-emerald-300">
          <TreePine className="w-3.5 h-3.5 text-emerald-400" />
          <span>Hacktoberfest: Touch Grass Challenge</span>
        </div>
        <h1 className="font-display text-4xl sm:text-6xl font-black tracking-tight text-white">
          Go find something.
        </h1>
        <p className="text-slate-400 text-sm sm:text-base max-w-lg mx-auto font-medium">
          Identify birds with private, offline AI. Discover one fascinating field mark. Then put your phone down and keep exploring.
        </p>
      </div>

      {/* HERO PRIMARY ACTION: SPOT A BIRD */}
      <div className="flex flex-col items-center justify-center pt-2">
        <button
          onClick={onSpotBird}
          className="btn-hero-spot group relative w-full sm:w-auto sm:min-w-[340px] px-8 py-6 rounded-3xl bg-gradient-to-br from-emerald-600 via-emerald-500 to-teal-500 text-white font-display font-black text-2xl flex items-center justify-center gap-4 shadow-2xl transition-all duration-300 hover:scale-105 active:scale-95 border-2 border-emerald-300/40 cursor-pointer"
        >
          <div className="w-14 h-14 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center group-hover:rotate-12 transition-transform shadow-inner">
            <Camera className="w-8 h-8 text-white drop-shadow-md" />
          </div>
          <div className="text-left">
            <div className="text-xs uppercase tracking-widest text-emerald-100 font-bold">
              Hero Mode
            </div>
            <div className="tracking-wide drop-shadow-md">
              SPOT A BIRD
            </div>
          </div>
          <ArrowRight className="w-6 h-6 ml-2 text-white/80 group-hover:translate-x-1.5 transition-transform" />
        </button>

        <div className="mt-4 flex items-center gap-2 text-xs font-semibold text-slate-400">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>100% Offline AI • Zero Cloud Latency • Private</span>
        </div>
      </div>

      {/* TODAY'S OUTDOOR PROGRESS DASHBOARD */}
      <div className="glass-panel p-6">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-extrabold uppercase tracking-wider text-emerald-400 font-display">
              TODAY'S OUTDOOR PROGRESS
            </span>
          </div>
          <span className="text-xs font-medium text-slate-400">
            Keep phone time low
          </span>
        </div>

        <div className="grid grid-cols-3 gap-3 text-center">
          {/* Minutes Outside */}
          <div className="bg-slate-900/60 border border-slate-800/70 p-4 rounded-2xl hover:border-emerald-500/30 transition-all">
            <div className="text-2xl sm:text-3xl font-display font-black text-emerald-400 flex items-center justify-center gap-1">
              <span>🌳</span>
              <span>{outdoorMinutes}</span>
              <span className="text-xs text-slate-400 font-normal">min</span>
            </div>
            <div className="text-xs text-slate-400 font-medium mt-1">
              Time Outside
            </div>
          </div>

          {/* Species Spotted */}
          <div className="bg-slate-900/60 border border-slate-800/70 p-4 rounded-2xl hover:border-emerald-500/30 transition-all">
            <div className="text-2xl sm:text-3xl font-display font-black text-amber-400 flex items-center justify-center gap-1">
              <span>🐦</span>
              <span>{discoveredCount}</span>
            </div>
            <div className="text-xs text-slate-400 font-medium mt-1">
              Species Spotted
            </div>
          </div>

          {/* XP Gained */}
          <div className="bg-slate-900/60 border border-slate-800/70 p-4 rounded-2xl hover:border-emerald-500/30 transition-all">
            <div className="text-2xl sm:text-3xl font-display font-black text-teal-300 flex items-center justify-center gap-1">
              <span>⭐</span>
              <span>+{xp}</span>
            </div>
            <div className="text-xs text-slate-400 font-medium mt-1">
              XP Earned
            </div>
          </div>
        </div>

        {/* Enter Touch Grass Mode Quick Card */}
        <div className="mt-5 p-4 rounded-2xl bg-gradient-to-r from-emerald-950/60 via-slate-900 to-slate-900 border border-emerald-800/30 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3 text-left">
            <div className="w-11 h-11 rounded-xl bg-emerald-900/40 border border-emerald-700/50 flex items-center justify-center text-xl shrink-0">
              🌿
            </div>
            <div>
              <div className="font-display font-bold text-sm text-white flex items-center gap-2">
                Touch Grass Mode
                <span className="text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-1.5 py-0.2 rounded-md">
                  Active
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Lock your screen, step into nature, and earn bonus outdoor XP.
              </p>
            </div>
          </div>
          <button
            onClick={onStartTouchGrass}
            className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold font-display flex items-center justify-center gap-2 transition-all shadow-md shadow-emerald-950 cursor-pointer shrink-0"
          >
            <span>Start Exploring</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* 1-CLICK CURATED DEMO SAMPLES (FOR HACKATHON JUDGES) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-400" />
            <h2 className="font-display font-bold text-lg text-white">
              1-Click Demo Samples (Hackathon Test Bench)
            </h2>
          </div>
          <span className="text-xs text-slate-400">
            Instant offline AI evaluation
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {demoSamples.map((sample) => (
            <div
              key={sample.id}
              onClick={() => onSelectDemoBird(sample)}
              className="group glass-panel p-3 rounded-2xl cursor-pointer hover:border-emerald-400/50 transition-all text-left flex flex-col justify-between"
            >
              <div className="relative aspect-square rounded-xl overflow-hidden mb-2 bg-slate-900">
                <img
                  src={sample.thumbnail_base64 || sample.image_path}
                  alt={sample.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                {sample.test_type === 'uncertainty_demo' ? (
                  <span className="absolute bottom-1 left-1 bg-amber-950/90 border border-amber-600 text-amber-300 text-[9px] font-bold px-1.5 py-0.5 rounded-md">
                    Uncertainty Test
                  </span>
                ) : (
                  <span className="absolute bottom-1 left-1 bg-emerald-950/90 border border-emerald-600 text-emerald-300 text-[9px] font-bold px-1.5 py-0.5 rounded-md">
                    Iconic Match
                  </span>
                )}
              </div>
              <div>
                <h3 className="font-display font-bold text-xs text-slate-100 group-hover:text-emerald-300 transition-colors line-clamp-1">
                  {sample.title}
                </h3>
                <p className="text-[10px] text-slate-400 line-clamp-1 mt-0.5">
                  {sample.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* SECONDARY ACTION TILES */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div
          onClick={() => onNavigate('guide')}
          className="glass-panel p-4 rounded-2xl cursor-pointer hover:border-emerald-500/40 transition-all text-center space-y-1"
        >
          <div className="text-2xl">🎒</div>
          <div className="font-display font-bold text-sm text-slate-200">
            Field Guide
          </div>
          <div className="text-[11px] text-slate-400">
            200 Bird Catalog
          </div>
        </div>

        <div
          onClick={() => onNavigate('gamification')}
          className="glass-panel p-4 rounded-2xl cursor-pointer hover:border-emerald-500/40 transition-all text-center space-y-1"
        >
          <div className="text-2xl">🔥</div>
          <div className="font-display font-bold text-sm text-slate-200">
            {streak} Day Streak
          </div>
          <div className="text-[11px] text-slate-400">
            Outdoor Activity
          </div>
        </div>

        <div
          onClick={() => onNavigate('leaderboard')}
          className="glass-panel p-4 rounded-2xl cursor-pointer hover:border-emerald-500/40 transition-all text-center space-y-1"
        >
          <div className="text-2xl">🏆</div>
          <div className="font-display font-bold text-sm text-slate-200">
            Leaderboard
          </div>
          <div className="text-[11px] text-slate-400">
            Nature Scouts
          </div>
        </div>

        <div
          onClick={() => onNavigate('gamification')}
          className="glass-panel p-4 rounded-2xl cursor-pointer hover:border-emerald-500/40 transition-all text-center space-y-1"
        >
          <div className="text-2xl">🎖️</div>
          <div className="font-display font-bold text-sm text-slate-200">
            Badges
          </div>
          <div className="text-[11px] text-slate-400">
            Collect Achievements
          </div>
        </div>
      </div>
    </div>
  );
}
