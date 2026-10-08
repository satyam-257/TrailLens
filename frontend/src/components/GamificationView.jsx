import React, { useState } from 'react';
import { 
  Flame, 
  Award, 
  Sparkles, 
  CheckCircle2, 
  Lock, 
  Calendar, 
  Clock, 
  TreePine, 
  ArrowRight,
  Zap,
  Target
} from 'lucide-react';
import { soundEffects } from '../utils/audio';

export default function GamificationView({ 
  userProfile, 
  badgesList, 
  challengesList, 
  onStartTouchGrass 
}) {
  const [selectedBadge, setSelectedBadge] = useState(null);

  const level = userProfile?.level || 1;
  const title = userProfile?.title || 'Trail Scout';
  const xp = userProfile?.total_xp || 340;
  const streak = userProfile?.streak_days || 4;
  const outdoorMins = userProfile?.total_outdoor_minutes || 76;
  const unlockedBadges = new Set(userProfile?.unlocked_badges || ['first_steps', 'first_feather']);

  // Level thresholds
  const nextLevelXp = level * 150;
  const curLevelBaseXp = (level - 1) * 150;
  const xpIntoLevel = Math.max(0, xp - curLevelBaseXp);
  const xpRequiredForNext = 150;
  const levelProgress = Math.min(100, Math.round((xpIntoLevel / xpRequiredForNext) * 100));

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8 text-left">
      {/* Level & Streak Hero Card */}
      <div className="glass-panel p-6 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 p-0.5 shadow-xl shadow-emerald-950 flex items-center justify-center">
              <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center text-3xl">
                🦅
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-display font-extrabold text-2xl text-white">
                  {userProfile?.user_name || "Satyam"}
                </h1>
                <span className="text-xs font-bold text-emerald-400 bg-emerald-950/80 border border-emerald-800/50 px-2.5 py-0.5 rounded-full">
                  {title}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Level {level} Nature Explorer • {unlockedBadges.size} Badges Earned
              </p>
            </div>
          </div>

          {/* Outdoor Streak Flame Box */}
          <div className="flex items-center gap-3 bg-amber-950/40 border border-amber-800/40 p-3 rounded-2xl">
            <span className="streak-flame text-3xl">🔥</span>
            <div>
              <div className="text-xs font-bold text-amber-400 font-display">
                OUTDOOR STREAK
              </div>
              <div className="text-base font-black text-amber-200">
                {streak} Days in Nature
              </div>
            </div>
          </div>
        </div>

        {/* Level XP Progress Bar */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs">
            <span className="text-slate-400 font-medium">
              Level {level} Progress ({xpIntoLevel} / {xpRequiredForNext} XP)
            </span>
            <span className="font-bold text-emerald-400">
              Next: Level {level + 1}
            </span>
          </div>
          <div className="w-full h-3 rounded-full bg-slate-900 overflow-hidden border border-slate-800">
            <div
              className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-500 rounded-full"
              style={{ width: `${levelProgress}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* ROTATING DAILY & WEEKLY OUTDOOR CHALLENGES */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            <h2 className="font-display font-extrabold text-xl text-white">
              Outdoor Challenges
            </h2>
          </div>
          <span className="text-xs text-slate-400">
            Reward real outdoor activity
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {challengesList?.map((ch) => (
            <div
              key={ch.id}
              className="glass-panel p-4 rounded-2xl border border-slate-800/70 space-y-3"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2.5">
                  <span className="text-2xl">{ch.icon}</span>
                  <div>
                    <h3 className="font-display font-bold text-sm text-white">
                      {ch.title}
                    </h3>
                    <p className="text-[11px] text-slate-400 mt-0.5">
                      {ch.description}
                    </p>
                  </div>
                </div>
                <span className="shrink-0 text-xs font-bold text-amber-400 bg-amber-950/70 border border-amber-800/40 px-2 py-0.5 rounded-full">
                  +{ch.reward_xp} XP
                </span>
              </div>

              {/* Progress */}
              <div className="space-y-1">
                <div className="flex items-center justify-between text-[11px] text-slate-400">
                  <span>Progress</span>
                  <span className="font-bold text-slate-200">
                    {ch.current} / {ch.target}
                  </span>
                </div>
                <div className="w-full h-1.5 rounded-full bg-slate-900 overflow-hidden">
                  <div
                    className="h-full bg-emerald-500 rounded-full"
                    style={{ width: `${Math.min(100, (ch.current / ch.target) * 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* COLLECTIBLE BADGES VAULT */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-400" />
            <h2 className="font-display font-extrabold text-xl text-white">
              Explorer Badges
            </h2>
          </div>
          <span className="text-xs text-slate-400">
            {unlockedBadges.size} of {badgesList?.length || 9} unlocked
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {badgesList?.map((badge) => {
            const isUnlocked = unlockedBadges.has(badge.id);

            return (
              <div
                key={badge.id}
                onClick={() => setSelectedBadge(badge)}
                className={`glass-panel p-4 rounded-2xl cursor-pointer transition-all text-center space-y-2 flex flex-col justify-between ${
                  isUnlocked
                    ? 'border-emerald-500/40 hover:border-emerald-400'
                    : 'border-slate-800 opacity-60 hover:opacity-85'
                }`}
              >
                <div>
                  <div className={`w-14 h-14 rounded-2xl mx-auto flex items-center justify-center text-3xl mb-2 ${
                    isUnlocked ? 'bg-emerald-950/70 border border-emerald-500/50 shadow-md shadow-emerald-950' : 'bg-slate-900 border border-slate-800'
                  }`}>
                    {badge.icon}
                  </div>
                  <h3 className="font-display font-bold text-sm text-white">
                    {badge.title}
                  </h3>
                  <p className="text-[11px] text-slate-400 line-clamp-2 mt-1">
                    {badge.description}
                  </p>
                </div>

                <div className="pt-2">
                  {isUnlocked ? (
                    <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-300 bg-emerald-950/80 border border-emerald-600/40 px-2 py-0.5 rounded-md">
                      <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                      Unlocked
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-slate-400 bg-slate-900 border border-slate-800 px-2 py-0.5 rounded-md">
                      <Lock className="w-3 h-3 text-slate-500" />
                      Locked
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
