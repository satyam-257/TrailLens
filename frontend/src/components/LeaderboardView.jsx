import React, { useState } from 'react';
import { 
  Trophy, 
  TreePine, 
  Flame, 
  Sparkles, 
  Medal, 
  Clock, 
  CheckCircle2,
  Users
} from 'lucide-react';

export default function LeaderboardView({ leaderboardData }) {
  const [period, setPeriod] = useState('this_week');

  const rankColors = {
    1: 'from-amber-400 to-yellow-600 text-slate-950',
    2: 'from-slate-300 to-slate-400 text-slate-950',
    3: 'from-amber-600 to-amber-800 text-white'
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6 text-left">
      {/* Header */}
      <div className="glass-panel p-6 space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl">🏆</span>
              <h1 className="font-display font-extrabold text-2xl sm:text-3xl text-white">
                Nature Scouts Leaderboard
              </h1>
            </div>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Rankings based strictly on verified outdoor exploration and real-world sightings.
            </p>
          </div>

          {/* Period filter buttons */}
          <div className="flex items-center gap-1.5 bg-slate-900/90 border border-slate-800 p-1 rounded-xl">
            <button
              onClick={() => setPeriod('this_week')}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                period === 'this_week'
                  ? 'bg-emerald-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              This Week
            </button>
            <button
              onClick={() => setPeriod('this_month')}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                period === 'this_month'
                  ? 'bg-emerald-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              This Month
            </button>
            <button
              onClick={() => setPeriod('all_time')}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                period === 'all_time'
                  ? 'bg-emerald-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              All-Time
            </button>
          </div>
        </div>
      </div>

      {/* Leaderboard Table / Cards */}
      <div className="space-y-3">
        {leaderboardData?.map((user) => {
          const isTop3 = user.rank <= 3;
          const isCurrent = user.is_current_user;

          return (
            <div
              key={user.rank}
              className={`glass-panel p-4 rounded-2xl flex items-center justify-between gap-4 transition-all ${
                isCurrent 
                  ? 'border-emerald-500/70 bg-emerald-950/30 ring-1 ring-emerald-500/40' 
                  : 'border-slate-800/80 hover:border-slate-700'
              }`}
            >
              {/* Rank & User Info */}
              <div className="flex items-center gap-3 sm:gap-4">
                {/* Rank Badge */}
                <div
                  className={`w-9 h-9 rounded-xl flex items-center justify-center font-display font-black text-sm shrink-0 ${
                    isTop3
                      ? `bg-gradient-to-br ${rankColors[user.rank]} shadow-md`
                      : 'bg-slate-900 border border-slate-800 text-slate-400'
                  }`}
                >
                  {user.rank === 1 ? '🥇' : user.rank === 2 ? '🥈' : user.rank === 3 ? '🥉' : user.rank}
                </div>

                {/* Avatar & Name */}
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center text-xl shrink-0">
                    {user.avatar || '🌿'}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-display font-bold text-sm sm:text-base text-white">
                        {user.name}
                      </span>
                      {isCurrent && (
                        <span className="text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-1.5 py-0.2 rounded-md font-bold">
                          YOU
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-slate-400 flex items-center gap-2 mt-0.5">
                      <span className="text-emerald-400 font-medium">{user.title}</span>
                      <span>•</span>
                      <span className="flex items-center gap-1">
                        <Flame className="w-3 h-3 text-amber-400" />
                        {user.streak}d streak
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Stats: Hours Outside, Species, XP */}
              <div className="flex items-center gap-4 sm:gap-6 text-right shrink-0">
                <div className="hidden sm:block">
                  <div className="text-[10px] text-slate-400 uppercase font-bold">
                    Hours Outside
                  </div>
                  <div className="text-xs font-bold text-slate-200 flex items-center justify-end gap-1">
                    <TreePine className="w-3 h-3 text-emerald-400" />
                    {user.outdoor_hours}h
                  </div>
                </div>

                <div className="hidden sm:block">
                  <div className="text-[10px] text-slate-400 uppercase font-bold">
                    Species
                  </div>
                  <div className="text-xs font-bold text-amber-400">
                    {user.species_count} 🐦
                  </div>
                </div>

                <div>
                  <div className="text-[10px] text-slate-400 uppercase font-bold">
                    Score
                  </div>
                  <div className="font-display font-black text-emerald-400 text-sm sm:text-base">
                    {user.xp.toLocaleString()} XP
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
