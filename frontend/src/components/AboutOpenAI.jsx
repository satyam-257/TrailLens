import React from 'react';
import { 
  ShieldCheck, 
  Cpu, 
  WifiOff, 
  Eye, 
  Code2, 
  BookOpen, 
  Layers, 
  CheckCircle2,
  TreePine,
  ExternalLink
} from 'lucide-react';

export default function AboutOpenAI({ onOpenHUD }) {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8 text-left">
      {/* Header */}
      <div className="glass-panel p-6 space-y-3">
        <div className="inline-flex items-center gap-2 text-xs font-bold text-emerald-400 bg-emerald-950/80 border border-emerald-800/50 px-3 py-1 rounded-full">
          <Code2 className="w-3.5 h-3.5" />
          <span>Open-Source AI Architecture</span>
        </div>
        <h1 className="font-display font-black text-3xl sm:text-4xl text-white">
          Why Open-Source AI for Nature?
        </h1>
        <p className="text-sm text-slate-300 max-w-2xl leading-relaxed">
          TrailLens uses lightweight, open-weight vision models that run entirely on your local machine. No proprietary black-box APIs, no cloud dependencies, and zero privacy compromises.
        </p>
      </div>

      {/* Core Pillars */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Pillar 1 */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-700/50 flex items-center justify-center text-emerald-400">
            <WifiOff className="w-5 h-5" />
          </div>
          <h3 className="font-display font-bold text-base text-white">
            100% Offline Wilderness Operation
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            The best birding spots are deep in national parks, dense forests, and remote mountain trails where cell reception is zero. Local AI guarantees instant identification anywhere on Earth.
          </p>
        </div>

        {/* Pillar 2 */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-700/50 flex items-center justify-center text-emerald-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <h3 className="font-display font-bold text-base text-white">
            Outdoor Privacy Guarantee
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Your photos and exploration journals remain strictly on your device. We do not harvest user observations to train closed commercial products.
          </p>
        </div>

        {/* Pillar 3 */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-700/50 flex items-center justify-center text-emerald-400">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="font-display font-bold text-base text-white">
            Pluggable Model Architecture
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Built upon the abstract <code className="text-emerald-300 font-mono">BirdClassifierBase</code>. Anyone can inspect the weights, swap the backbone (MobileNet, EfficientNet, ResNet), or fine-tune custom regional bird datasets.
          </p>
        </div>

        {/* Pillar 4 */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-700/50 flex items-center justify-center text-emerald-400">
            <Eye className="w-5 h-5" />
          </div>
          <h3 className="font-display font-bold text-base text-white">
            Calibrated Uncertainty (No Hallucinations)
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Unlike generative chatbots that pretend to know everything, TrailLens computes entropy and confidence thresholds, honestly telling you when a photo is too blurry or distant to be certain.
          </p>
        </div>
      </div>

      {/* Dataset & Licenses Summary */}
      <div className="glass-panel p-6 border border-emerald-900/40 space-y-4">
        <h2 className="font-display font-bold text-lg text-white flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-emerald-400" />
          <span>Dataset Licenses & Attribution</span>
        </h2>
        
        <div className="space-y-2 text-xs text-slate-300 leading-relaxed">
          <p>
            • <strong>CUB-200-2011</strong> (Caltech-UCSD Birds): Used for non-commercial research & educational bird classification evaluation under Caltech-UCSD terms.
          </p>
          <p>
            • <strong>NABirds</strong> (Cornell Lab of Ornithology): Standardized benchmark for North American avian taxonomy.
          </p>
          <p>
            • <strong>MobileNetV3 / PyTorch Weights</strong>: Open weights licensed under Apache 2.0 / BSD 3-Clause.
          </p>
        </div>

        <div className="pt-2 flex items-center gap-3">
          <button
            onClick={onOpenHUD}
            className="btn-adventure text-xs !py-2 !px-4"
          >
            <Cpu className="w-3.5 h-3.5" />
            Open Model Diagnostics HUD
          </button>
        </div>
      </div>
    </div>
  );
}
