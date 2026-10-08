import React, { useState, useEffect } from 'react';
import { 
  TreePine, 
  Lock, 
  Sparkles, 
  Volume2, 
  VolumeX, 
  ArrowLeft, 
  CheckCircle,
  Eye,
  Footprints,
  Compass
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { soundEffects } from '../utils/audio';

export default function TouchGrassMode({ 
  isActive, 
  onEndSession, 
  onClose, 
  initialDiscoveries = 1 
}) {
  const [seconds, setSeconds] = useState(0);
  const [appSeconds, setAppSeconds] = useState(15);
  const [isCompleted, setIsCompleted] = useState(false);
  const [sessionSummary, setSessionSummary] = useState(null);
  const [ambientAudio, setAmbientAudio] = useState(true);

  // Outdoor stopwatch ticker
  useEffect(() => {
    let interval = null;
    if (isActive && !isCompleted) {
      interval = setInterval(() => {
        setSeconds((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isActive, isCompleted]);

  // Periodic soothing nature tone
  useEffect(() => {
    let audioTimer = null;
    if (isActive && !isCompleted && ambientAudio) {
      soundEffects.playNaturePulse();
      audioTimer = setInterval(() => {
        if (ambientAudio) soundEffects.playNaturePulse();
      }, 30000);
    }
    return () => clearInterval(audioTimer);
  }, [isActive, isCompleted, ambientAudio]);

  if (!isActive) return null;

  const formatTime = (totalSec) => {
    const mins = Math.floor(totalSec / 60);
    const secs = totalSec % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleFinishExploring = async () => {
    soundEffects.playDiscoveryChime();
    const durationMinutes = Math.max(1, Math.ceil(seconds / 60));
    const result = await onEndSession(durationMinutes, appSeconds, initialDiscoveries);

    setSessionSummary({
      durationMinutes,
      appSeconds,
      discoveries: initialDiscoveries,
      xpEarned: result?.awarded_xp || durationMinutes * 3 + 50,
      newBadges: result?.new_badges || []
    });
    setIsCompleted(true);

    try {
      confetti({
        particleCount: 70,
        spread: 80,
        origin: { y: 0.6 },
        colors: ['#10b981', '#34d399', '#f59e0b', '#84cc16']
      });
    } catch (e) {}
  };

  const resetAndClose = () => {
    setSeconds(0);
    setIsCompleted(false);
    setSessionSummary(null);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-between p-6 bg-slate-950/95 backdrop-blur-xl text-center select-none animate-fadeIn">
      {!isCompleted ? (
        <>
          {/* Top minimal status */}
          <div className="w-full max-w-md flex items-center justify-between pt-2">
            <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 bg-emerald-950/80 border border-emerald-800/40 px-3 py-1 rounded-full">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              TOUCH GRASS MODE
            </div>

            <button
              onClick={() => setAmbientAudio(!ambientAudio)}
              className="p-2 rounded-full bg-slate-900 border border-slate-800 text-slate-400 hover:text-emerald-400 transition-colors cursor-pointer"
              title="Toggle Ambient Nature Tone"
            >
              {ambientAudio ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            </button>
          </div>

          {/* Central Breathing Ring & Ambient Timer */}
          <div className="flex flex-col items-center justify-center my-auto space-y-6">
            <div className="relative flex items-center justify-center">
              {/* Outer glowing organic halo */}
              <div className="touch-grass-ring w-48 h-48 sm:w-60 sm:h-60 rounded-full bg-gradient-to-tr from-emerald-900/30 via-emerald-600/20 to-teal-500/30 border border-emerald-500/40 flex items-center justify-center">
                <div className="w-36 h-36 sm:w-48 sm:h-48 rounded-full bg-slate-950/90 border border-emerald-500/30 flex flex-col items-center justify-center shadow-2xl">
                  <div className="text-4xl mb-1">🌳</div>
                  <div className="font-display font-black text-3xl sm:text-4xl text-white tracking-widest tabular-nums">
                    {formatTime(seconds)}
                  </div>
                  <div className="text-[10px] text-emerald-400 font-bold uppercase tracking-widest mt-1">
                    TIME OUTDOORS
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-2 max-w-xs">
              <h2 className="font-display font-extrabold text-xl text-white">
                Keep exploring.
              </h2>
              <p className="text-xs text-slate-400 font-medium leading-relaxed">
                Look up at the branches. Listen to birdsong. Feel the breeze.
              </p>
            </div>

            <div className="inline-flex items-center gap-1.5 bg-slate-900/90 border border-slate-800 px-4 py-1.5 rounded-full text-xs font-semibold text-slate-400">
              <Lock className="w-3.5 h-3.5 text-emerald-400" />
              <span>Phone down • Screen dimmed</span>
            </div>
          </div>

          {/* Bottom Action */}
          <div className="w-full max-w-xs pb-4">
            <button
              onClick={handleFinishExploring}
              className="w-full py-4 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-display font-bold text-base shadow-xl shadow-emerald-950/80 transition-all hover:scale-105 active:scale-95 cursor-pointer flex items-center justify-center gap-2"
            >
              <CheckCircle className="w-5 h-5" />
              <span>I'm Back from Exploring</span>
            </button>
          </div>
        </>
      ) : (
        /* RETURN SUMMARY CELEBRATION */
        <div className="w-full max-w-md my-auto glass-panel p-6 border border-emerald-500/40 space-y-6 animate-scaleUp">
          <div className="text-center space-y-2">
            <div className="text-4xl">🌿</div>
            <h2 className="font-display font-black text-2xl sm:text-3xl text-white">
              WELCOME BACK
            </h2>
            <p className="text-xs text-emerald-400 font-semibold">
              You spent {sessionSummary?.durationMinutes} minutes exploring the real world.
            </p>
          </div>

          {/* Metrics comparison: Outdoor time vs Screen time */}
          <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl space-y-3">
            <div className="flex items-center justify-between text-xs py-1 border-b border-slate-800/80">
              <span className="text-slate-400 flex items-center gap-1.5 font-medium">
                <span>🌳</span> Time Outside
              </span>
              <span className="font-display font-bold text-emerald-400 text-sm">
                {sessionSummary?.durationMinutes} min
              </span>
            </div>

            <div className="flex items-center justify-between text-xs py-1 border-b border-slate-800/80">
              <span className="text-slate-400 flex items-center gap-1.5 font-medium">
                <span>🐦</span> Species Discoveries
              </span>
              <span className="font-display font-bold text-amber-400 text-sm">
                {sessionSummary?.discoveries}
              </span>
            </div>

            <div className="flex items-center justify-between text-xs py-1 border-b border-slate-800/80">
              <span className="text-slate-400 flex items-center gap-1.5 font-medium">
                <span>📱</span> Time in TrailLens
              </span>
              <span className="font-display font-bold text-teal-300 text-sm">
                {sessionSummary?.appSeconds} sec
              </span>
            </div>

            <div className="flex items-center justify-between text-xs pt-1">
              <span className="text-slate-300 font-bold flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" /> Total XP Earned
              </span>
              <span className="font-display font-black text-emerald-400 text-lg">
                +{sessionSummary?.xpEarned} XP
              </span>
            </div>
          </div>

          <button
            onClick={resetAndClose}
            className="w-full py-3.5 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-display font-bold text-sm shadow-lg shadow-emerald-950 transition-all cursor-pointer"
          >
            Return to Dashboard
          </button>
        </div>
      )}
    </div>
  );
}
