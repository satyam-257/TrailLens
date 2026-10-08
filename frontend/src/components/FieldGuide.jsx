import React, { useState, useMemo } from 'react';
import { 
  Search, 
  Filter, 
  Volume2, 
  Sparkles, 
  MapPin, 
  BookOpen, 
  CheckCircle2, 
  Lock, 
  X,
  Compass
} from 'lucide-react';
import { soundEffects } from '../utils/audio';

const FAMILY_FILTERS = [
  { id: 'all', label: 'All Birds' },
  { id: 'discovered', label: 'Discovered ✨' },
  { id: 'undiscovered', label: 'Undiscovered 🔒' },
  { id: 'Trochilidae', label: 'Hummingbirds' },
  { id: 'Cardinalidae', label: 'Cardinals & Buntings' },
  { id: 'Picidae', label: 'Woodpeckers' },
  { id: 'Corvidae', label: 'Jays & Crows' },
  { id: 'Diomedeidae', label: 'Albatrosses' },
  { id: 'Passerellidae', label: 'Sparrows' }
];

export default function FieldGuide({ speciesList, userProfile, onSpotBird }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [selectedSpecies, setSelectedSpecies] = useState(null);

  const discoveredSet = useMemo(() => {
    return new Set(userProfile?.discovered_species_ids || []);
  }, [userProfile]);

  const filteredSpecies = useMemo(() => {
    return speciesList.filter((s) => {
      const isDiscovered = discoveredSet.has(s.id);
      
      // Filter tab check
      if (selectedFilter === 'discovered' && !isDiscovered) return false;
      if (selectedFilter === 'undiscovered' && isDiscovered) return false;
      if (selectedFilter !== 'all' && selectedFilter !== 'discovered' && selectedFilter !== 'undiscovered') {
        if (s.family !== selectedFilter) return false;
      }

      // Search query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        return (
          s.common_name.toLowerCase().includes(q) ||
          s.family.toLowerCase().includes(q) ||
          s.habitat.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [speciesList, discoveredSet, selectedFilter, searchQuery]);

  const totalCatalog = speciesList.length || 200;
  const discoveredTotal = discoveredSet.size;
  const percentage = Math.round((discoveredTotal / totalCatalog) * 100);

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-6">
      {/* Header & Catalog Progress Bar */}
      <div className="glass-panel p-6 space-y-4 text-left">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl">🎒</span>
              <h1 className="font-display font-extrabold text-2xl sm:text-3xl text-white">
                Avian Field Guide
              </h1>
            </div>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Your collectible bird log. Discover species outdoors to illuminate your guide.
            </p>
          </div>

          <div className="flex items-center gap-3 bg-slate-900/90 border border-emerald-900/40 px-4 py-2.5 rounded-2xl">
            <div className="text-right">
              <div className="text-xs font-bold text-slate-300 font-display">
                FIELD PROGRESS
              </div>
              <div className="text-sm font-black text-emerald-400">
                {discoveredTotal} / {totalCatalog} Species
              </div>
            </div>
            <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-500/30 flex items-center justify-center font-display font-black text-xs text-emerald-300">
              {percentage}%
            </div>
          </div>
        </div>

        {/* Visual Progress Bar */}
        <div className="w-full h-2.5 rounded-full bg-slate-900 overflow-hidden border border-slate-800">
          <div 
            className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-500"
            style={{ width: `${Math.max(2, percentage)}%` }}
          ></div>
        </div>
      </div>

      {/* Search & Category Filter Tabs */}
      <div className="space-y-3">
        {/* Search Bar */}
        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by bird name, family, or habitat..."
            className="w-full pl-10 pr-4 py-3 rounded-2xl bg-slate-900/80 border border-slate-800 focus:border-emerald-500 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none transition-colors"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-slate-400 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
          {FAMILY_FILTERS.map((f) => (
            <button
              key={f.id}
              onClick={() => setSelectedFilter(f.id)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
                selectedFilter === f.id
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-950'
                  : 'bg-slate-900/80 border border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800'
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Species Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        {filteredSpecies.map((bird) => {
          const isDiscovered = discoveredSet.has(bird.id);
          const stars = "★".repeat(bird.rarity || 2);

          return (
            <div
              key={bird.id}
              onClick={() => setSelectedSpecies(bird)}
              className={`group glass-panel p-3 rounded-2xl cursor-pointer transition-all text-left flex flex-col justify-between ${
                isDiscovered 
                  ? 'hover:border-emerald-400/60 border-emerald-900/40' 
                  : 'border-slate-800/60 opacity-85 hover:opacity-100'
              }`}
            >
              {/* Card visual container */}
              <div className="relative aspect-square rounded-xl overflow-hidden mb-2 bg-slate-900 flex items-center justify-center">
                {isDiscovered ? (
                  <div className="w-full h-full bg-gradient-to-tr from-emerald-950/80 to-slate-900 flex items-center justify-center text-4xl">
                    🐦
                  </div>
                ) : (
                  <div className="w-full h-full bg-slate-950 flex flex-col items-center justify-center p-2 text-center">
                    <Lock className="w-6 h-6 text-slate-600 mb-1" />
                    <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">
                      Undiscovered
                    </span>
                  </div>
                )}

                {/* Status badge */}
                <div className="absolute top-1.5 right-1.5">
                  {isDiscovered ? (
                    <span className="bg-emerald-950/90 border border-emerald-500/50 text-emerald-300 text-[10px] font-bold px-1.5 py-0.5 rounded-md flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                      Discovered
                    </span>
                  ) : (
                    <span className="bg-slate-950/90 border border-slate-700 text-slate-400 text-[10px] font-semibold px-1.5 py-0.5 rounded-md">
                      #{bird.id}
                    </span>
                  )}
                </div>

                <div className="absolute bottom-1.5 left-1.5 text-amber-400 text-[11px]">
                  {stars}
                </div>
              </div>

              {/* Title & Info */}
              <div>
                <h3 className="font-display font-bold text-xs text-white group-hover:text-emerald-300 transition-colors line-clamp-1">
                  {bird.common_name}
                </h3>
                <p className="text-[10px] text-slate-400 line-clamp-1 mt-0.5">
                  {bird.family} • {bird.habitat}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* SPECIES DETAIL DRAWER MODAL */}
      {selectedSpecies && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md animate-fadeIn">
          <div className="relative w-full max-w-md glass-panel p-6 border border-emerald-500/40 text-left space-y-4">
            <button
              onClick={() => setSelectedSpecies(null)}
              className="absolute top-4 right-4 p-2 rounded-full bg-slate-900 text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="space-y-1">
              <div className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-400 bg-emerald-950/80 border border-emerald-800/50 px-2.5 py-0.5 rounded-full">
                <span>{selectedSpecies.family}</span>
                <span>•</span>
                <span>Tier {selectedSpecies.rarity}★</span>
              </div>
              <h2 className="font-display font-extrabold text-2xl text-white">
                {selectedSpecies.common_name}
              </h2>
              <p className="text-xs text-slate-400 italic">
                {selectedSpecies.scientific_name}
              </p>
            </div>

            {/* Fact Box */}
            <div className="bg-emerald-950/40 border border-emerald-800/40 p-4 rounded-2xl space-y-1">
              <div className="text-[10px] font-bold uppercase text-emerald-400 font-display">
                Field Observation Fact
              </div>
              <p className="text-xs sm:text-sm text-slate-200 leading-relaxed font-medium">
                {selectedSpecies.fact}
              </p>
            </div>

            {/* Habitat & Audio */}
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900 border border-slate-800 text-xs">
                <span className="text-slate-400 font-medium flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-emerald-400" /> Habitat
                </span>
                <span className="text-slate-200 font-semibold text-right">
                  {selectedSpecies.habitat}
                </span>
              </div>

              <button
                onClick={() => soundEffects.playBirdChirp()}
                className="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-emerald-500/40 text-emerald-300 font-bold font-display text-xs flex items-center justify-center gap-2 transition-colors cursor-pointer"
              >
                <Volume2 className="w-4 h-4 text-amber-400" />
                <span>Play Simulated Call 🔊</span>
              </button>
            </div>

            {/* Action */}
            <div className="pt-2">
              <button
                onClick={() => {
                  setSelectedSpecies(null);
                  onSpotBird();
                }}
                className="w-full py-3.5 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-display font-bold text-sm flex items-center justify-center gap-2 shadow-lg shadow-emerald-950 transition-all cursor-pointer"
              >
                <span>Spot This Bird in Nature</span>
                <span>📷</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
