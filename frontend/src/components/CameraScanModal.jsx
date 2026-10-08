import React, { useState, useRef, useEffect } from 'react';
import { 
  Camera, 
  Upload, 
  X, 
  Zap, 
  Sparkles, 
  ShieldCheck, 
  RefreshCw,
  Image as ImageIcon
} from 'lucide-react';
import { soundEffects } from '../utils/audio';

const SCAN_MICROCOPY = [
  "Scanning plumage patterns...",
  "Checking beak and bill geometry...",
  "Comparing wing field marks...",
  "Consulting local offline guide...",
  "Analyzing avian taxonomies...",
  "Almost identified..."
];

export default function CameraScanModal({ 
  isOpen, 
  onClose, 
  onIdentify, 
  demoSamples, 
  initialSample = null 
}) {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scanStepIndex, setScanStepIndex] = useState(0);
  const [useLiveCamera, setUseLiveCamera] = useState(false);
  const [cameraError, setCameraError] = useState(null);

  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    if (initialSample) {
      handleSelectSample(initialSample);
    }
  }, [initialSample]);

  // Microcopy animation ticker
  useEffect(() => {
    let interval;
    if (isScanning) {
      interval = setInterval(() => {
        setScanStepIndex((prev) => (prev + 1) % SCAN_MICROCOPY.length);
      }, 400);
    }
    return () => clearInterval(interval);
  }, [isScanning]);

  // Handle Live Camera Stream
  useEffect(() => {
    let stream = null;
    if (useLiveCamera && isOpen) {
      navigator.mediaDevices?.getUserMedia({ video: { facingMode: 'environment' } })
        .then((s) => {
          stream = s;
          if (videoRef.current) {
            videoRef.current.srcObject = s;
          }
        })
        .catch((err) => {
          console.warn("Camera access failed", err);
          setCameraError("Camera unavailable. You can upload an image or choose a demo photo!");
          setUseLiveCamera(false);
        });
    }

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [useLiveCamera, isOpen]);

  if (!isOpen) return null;

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setSelectedImage(event.target.result);
        setUseLiveCamera(false);
        startIdentification(event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSelectSample = (sample) => {
    const imgData = sample.thumbnail_base64 || sample.image_path;
    setSelectedImage(imgData);
    setUseLiveCamera(false);
    startIdentification(imgData, sample);
  };

  const captureCameraFrame = () => {
    if (videoRef.current && canvasRef.current) {
      soundEffects.playShutter();
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataUrl = canvas.toDataURL('image/jpeg', 0.85);
      setSelectedImage(dataUrl);
      setUseLiveCamera(false);
      startIdentification(dataUrl);
    }
  };

  const startIdentification = async (imgData, sampleData = null) => {
    soundEffects.playShutter();
    setIsScanning(true);
    
    // Simulate natural visual scan feel
    setTimeout(async () => {
      await onIdentify(imgData, sampleData);
      setIsScanning(false);
    }, 900);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-lg glass-panel p-6 overflow-hidden border border-emerald-500/30">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors z-20"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="text-center space-y-1 mb-5">
          <div className="inline-flex items-center gap-1.5 text-[11px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950/80 border border-emerald-800/40 px-3 py-0.5 rounded-full">
            <ShieldCheck className="w-3.5 h-3.5" />
            Local Edge Vision AI
          </div>
          <h2 className="font-display font-extrabold text-2xl text-white">
            Spot a Bird
          </h2>
          <p className="text-xs text-slate-400 font-medium">
            Capture or choose a bird to identify instantly on-device.
          </p>
        </div>

        {/* Viewfinder / Capture Box */}
        <div className="relative aspect-[4/3] rounded-2xl overflow-hidden bg-slate-900/90 border-2 border-dashed border-slate-700 flex items-center justify-center mb-5">
          {isScanning && (
            <div className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-slate-950/75 backdrop-blur-sm">
              <div className="radar-scanner"></div>
              <div className="w-16 h-16 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin mb-3"></div>
              <div className="font-display font-bold text-sm text-emerald-300 animate-pulse">
                {SCAN_MICROCOPY[scanStepIndex]}
              </div>
              <div className="text-[11px] text-slate-400 mt-1">
                Running MobileNetV3 on CPU (under 30ms)
              </div>
            </div>
          )}

          {useLiveCamera ? (
            <div className="relative w-full h-full">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className="w-full h-full object-cover"
              />
              <button
                onClick={captureCameraFrame}
                className="absolute bottom-4 left-1/2 -translate-x-1/2 px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-full shadow-xl flex items-center gap-2 font-display text-sm cursor-pointer"
              >
                <Camera className="w-4 h-4" />
                Capture Photo
              </button>
            </div>
          ) : selectedImage ? (
            <img
              src={selectedImage}
              alt="Selected bird"
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="text-center p-6 space-y-4">
              <div className="w-14 h-14 rounded-2xl bg-emerald-950/60 border border-emerald-800/50 flex items-center justify-center mx-auto text-2xl">
                📷
              </div>
              <div>
                <div className="font-display font-bold text-sm text-slate-200">
                  Select an image or take a photo
                </div>
                <div className="text-xs text-slate-400 mt-1">
                  High-resolution photo yields best field mark recognition
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="btn-secondary text-xs"
                >
                  <Upload className="w-3.5 h-3.5 text-emerald-400" />
                  Upload Photo
                </button>
                <button
                  onClick={() => setUseLiveCamera(true)}
                  className="btn-adventure text-xs !py-2 !px-3.5"
                >
                  <Camera className="w-3.5 h-3.5" />
                  Open Camera
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Hidden File Input & Canvas */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={handleFileUpload}
        />
        <canvas ref={canvasRef} className="hidden" />

        {/* 1-Click Iconic Demo Birds (Quick Tap Selector) */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
            <span className="flex items-center gap-1.5">
              <Zap className="w-3.5 h-3.5 text-amber-400" />
              1-Click Demo Birds:
            </span>
            <span className="text-[10px] text-slate-400">Tap to test AI</span>
          </div>

          <div className="grid grid-cols-4 gap-2">
            {demoSamples?.slice(0, 4).map((sample) => (
              <button
                key={sample.id}
                onClick={() => handleSelectSample(sample)}
                className="group relative rounded-xl overflow-hidden aspect-square border border-slate-800 hover:border-emerald-400 transition-all text-left bg-slate-900"
              >
                <img
                  src={sample.thumbnail_base64 || sample.image_path}
                  alt={sample.title}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-1">
                  <span className="text-[9px] font-bold text-white line-clamp-1">
                    {sample.title.split(' ')[0]}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
