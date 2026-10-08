import React, { useEffect } from 'react';
import { 
  Sparkles, 
  Volume2, 
  TreePine, 
  ArrowRight, 
  X, 
  ShieldAlert, 
  CheckCircle2, 
  MapPin, 
  Award,
  BookOpen,
  Share2
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { soundEffects } from '../utils/audio';

export default function ResultModal({ 
  isOpen, 
  result, 
  imageSrc, 
  onClose, 
  onAddToFieldGuide, 
  onEnterTouchGrass 
}) {
  useEffect(() => {
    if (isOpen && result?.is_confident) {
      soundEffects.playDiscoveryChime();
      try {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.7 },
          colors: ['#10b981', '#34d399', '#f59e0b', '#38bdf8']
        });
      } catch (e) {}
    }
  }, [isOpen, result]);

  if (!isOpen || !result) return null;

  const top = result.top_prediction;
  const species = top?.species || {};
  const isConfident = result.is_confident;
  const uncertainty = result.uncertainty_notice;
  const rarityStars = "★".repeat(species.rarity || 2) + "☆".repeat(5 - (species.rarity || 2));

  const handlePlayBirdCall = () => {
    soundEffects.playBirdChirp();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-md glass-panel p-6 border border-emerald-500/40 max-h-[90vh] overflow-y-auto">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors z-20"
        >
          <X className="w-5 h-5" />
        </button>

        {/* HIGH CONFIDENCE RESULT */}
        {isConfident ? (
          <div className="space-y-5">
            {/* Top Celebration Badge */}
            <div className="text-center space-y-1">
              <div className="inline-flex items-center gap-1.5 bg-emerald-950/90 text-emerald-300 border border-emerald-700/60 px-3 py-1 rounded-full text-xs font-bold font-display">
                <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                NEW DISCOVERY! 🎉
              </div>
              <h2 className="font-display font-extrabold text-2xl text-white">
                {species.common_name}
              </h2>
              <p className="text-xs text-slate-400 italic">
                {species.scientific_name} • {species.family}
              </p>
            </div>

            {/* Bird Photo with Confidence Tag */}
            <div className="relative aspect-[4/3] rounded-2xl overflow-hidden bg-slate-900 border border-slate-800 shadow-xl">
              {imageSrc && (
                <img
                  src={imageSrc}
                  alt={species.common_name}
                  className="w-full h-full object-cover"
                />
              )}
              <div className="absolute top-3 left-3 bg-slate-950/85 backdrop-blur-md border border-emerald-500/40 text-emerald-300 text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1.5 shadow-md">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>{top.confidence_percentage}% Match</span>
              </div>
              <div className="absolute bottom-3 right-3 bg-amber-950/90 backdrop-blur-md border border-amber-500/40 text-amber-300 text-xs font-bold px-2.5 py-1 rounded-full">
                {rarityStars}
              </div>
            </div>

            {/* "DID YOU KNOW?" PUNCHY FACT BOX */}
            <div className="bg-emerald-950/40 border border-emerald-800/40 p-4 rounded-2xl space-y-1.5 text-left">
              <div className="text-[11px] font-extrabold uppercase tracking-wider text-emerald-400 font-display flex items-center gap-1.5">
                <span>💡 DID YOU KNOW?</span>
              </div>
              <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-medium">
                {species.fact}
              </p>
            </div>

            {/* Habitat & Audio Call Simulation */}
            <div className="grid grid-cols-2 gap-2 text-left">
              <div className="bg-slate-900/80 border border-slate-800 p-3 rounded-xl">
                <div className="text-[10px] text-slate-400 uppercase font-bold flex items-center gap-1">
                  <MapPin className="w-3 h-3 text-emerald-400" /> Habitat
                </div>
                <div className="text-xs font-semibold text-slate-200 mt-0.5 line-clamp-1">
                  {species.habitat}
                </div>
              </div>

              <button
                onClick={handlePlayBirdCall}
                className="bg-slate-900/80 hover:bg-slate-800 border border-slate-800 hover:border-emerald-500/50 p-3 rounded-xl flex items-center justify-between transition-colors text-left group"
              >
                <div>
                  <div className="text-[10px] text-slate-400 uppercase font-bold flex items-center gap-1">
                    <Volume2 className="w-3 h-3 text-amber-400" /> Bird Call
                  </div>
                  <div className="text-xs font-semibold text-emerald-300 mt-0.5 group-hover:underline">
                    Listen to call
                  </div>
                </div>
                <span className="text-sm">🔊</span>
              </button>
            </div>

            {/* XP Awarded Pill */}
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/90 border border-emerald-900/30 text-xs">
              <span className="text-slate-400 font-medium">Field Explorer Reward</span>
              <span className="text-emerald-400 font-bold font-display text-sm flex items-center gap-1">
                <Sparkles className="w-4 h-4 text-amber-400" />
                +{species.base_xp || 100} XP
              </span>
            </div>

            {/* THE PHILOSOPHICAL HERO ACTION: PUT PHONE DOWN */}
            <div className="pt-2 space-y-3">
              <div className="p-3.5 rounded-2xl bg-gradient-to-r from-emerald-900/60 to-teal-950/60 border border-emerald-500/50 text-left">
                <div className="text-xs font-bold text-emerald-300 font-display flex items-center gap-1.5">
                  <TreePine className="w-4 h-4 text-emerald-400" />
                  Your Outdoor Mission:
                </div>
                <p className="text-xs text-slate-300 mt-1">
                  Find this bird again in real life without looking at your phone.
                </p>
              </div>

              <button
                onClick={onEnterTouchGrass}
                className="w-full py-4 rounded-2xl bg-gradient-to-r from-emerald-600 via-emerald-500 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white font-display font-black text-lg flex items-center justify-center gap-2 shadow-xl shadow-emerald-950/80 transition-all hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
              >
                <span>I'M GOING EXPLORING</span>
                <span className="text-xl">🌳</span>
              </button>

              <button
                onClick={onAddToFieldGuide}
                className="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white text-xs font-bold font-display flex items-center justify-center gap-1.5 transition-colors border border-slate-800 cursor-pointer"
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>Save to Field Guide & Continue</span>
              </button>
            </div>
          </div>
        ) : (
          /* UNCERTAIN PREDICTION BOUNDARY (HONEST AI CALIBRATION) */
          <div className="space-y-5 text-left">
            <div className="text-center space-y-2">
              <div className="w-12 h-12 rounded-2xl bg-amber-950/70 border border-amber-700/60 flex items-center justify-center mx-auto text-2xl">
                🤔
              </div>
              <h2 className="font-display font-extrabold text-2xl text-white">
                {uncertainty?.headline || "I'm not confident yet."}
              </h2>
              <p className="text-xs text-amber-300 font-medium">
                {uncertainty?.message || `I think this might be ${top?.species?.common_name} (${top?.confidence_percentage}%), but the signal is fuzzy.`}
              </p>
            </div>

            {/* Photo preview */}
            <div className="relative aspect-[4/3] rounded-2xl overflow-hidden bg-slate-900 border border-amber-800/40">
              {imageSrc && (
                <img
                  src={imageSrc}
                  alt="Uncertain sighting"
                  className="w-full h-full object-cover"
                />
              )}
              <div className="absolute top-3 left-3 bg-amber-950/90 border border-amber-600/60 text-amber-300 text-xs font-bold px-2.5 py-1 rounded-full flex items-center gap-1">
                <ShieldAlert className="w-3.5 h-3.5" />
                <span>Low AI Confidence</span>
              </div>
            </div>

            {/* Tips for better capture */}
            <div className="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl space-y-2">
              <div className="text-xs font-bold text-slate-200 font-display">
                Try these outdoor observation tips:
              </div>
              <ul className="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                {uncertainty?.tips?.map((tip, idx) => (
                  <li key={idx}>{tip}</li>
                )) || (
                  <>
                    <li>Move closer or zoom in gently without startling the bird</li>
                    <li>Ensure the head and beak profile are in clear focus</li>
                    <li>Improve lighting to avoid backlit silhouettes</li>
                  </>
                )}
              </ul>
            </div>

            {/* Action buttons */}
            <div className="pt-2 space-y-2">
              <button
                onClick={onEnterTouchGrass}
                className="w-full py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-display font-bold text-sm flex items-center justify-center gap-2 transition-all cursor-pointer shadow-lg shadow-emerald-950"
              >
                <span>Explore Nature Instead</span>
                <span>🌳</span>
              </button>
              <button
                onClick={onClose}
                className="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white text-xs font-semibold transition-colors border border-slate-800 cursor-pointer"
              >
                Try Another Photo
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
