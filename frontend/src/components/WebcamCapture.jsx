import React, { useRef, useState, useEffect } from 'react';
import { Camera, CameraOff, RefreshCw, Sun, Eye, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';
import { stressAPI } from '../services/api';

export const WebcamCapture = ({ onAnalysisComplete, autoStart = true }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [lightingScore, setLightingScore] = useState('Optimal');
  const [lastResult, setLastResult] = useState(null);

  // Initialize camera
  const startCamera = async () => {
    setError(null);
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user',
        },
        audio: false,
      });
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setStream(mediaStream);
      setCameraActive(true);
    } catch (err) {
      console.error('Camera access error:', err);
      setError('Camera access unavailable. Grant camera permissions in browser settings, or evaluate using the Behavioural Survey tab.');
      setCameraActive(false);
    }
  };

  // Stop camera
  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setCameraActive(false);
  };

  useEffect(() => {
    if (autoStart) {
      startCamera();
    }
    return () => {
      stopCamera();
    };
  }, []);

  // Periodic lighting evaluation
  useEffect(() => {
    if (!cameraActive) return;
    const interval = setInterval(() => {
      checkLighting();
    }, 2500);
    return () => clearInterval(interval);
  }, [cameraActive]);

  const checkLighting = () => {
    if (!videoRef.current || !canvasRef.current) return;
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (video.videoWidth === 0) return;

    const ctx = canvas.getContext('2d');
    canvas.width = 64;
    canvas.height = 48;
    ctx.drawImage(video, 0, 0, 64, 48);
    const imgData = ctx.getImageData(0, 0, 64, 48);
    const data = imgData.data;

    let brightnessSum = 0;
    for (let i = 0; i < data.length; i += 4) {
      brightnessSum += (data[i] * 0.299 + data[i + 1] * 0.587 + data[i + 2] * 0.114);
    }
    const avgBrightness = brightnessSum / (data.length / 4);

    if (avgBrightness < 55) {
      setLightingScore('Dim Lighting');
    } else if (avgBrightness > 215) {
      setLightingScore('Overexposed');
    } else {
      setLightingScore('Optimal');
    }
  };

  // Capture current frame and send to backend
  const captureAndAnalyze = async () => {
    if (!videoRef.current) return;
    setAnalyzing(true);
    setError(null);

    try {
      const video = videoRef.current;
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const base64Image = canvas.toDataURL('image/jpeg', 0.85);

      // Call FastAPI facial analysis engine
      const res = await stressAPI.analyzeFacial(base64Image);
      setLastResult(res.data);

      if (onAnalysisComplete) {
        onAnalysisComplete(res.data, base64Image);
      }
    } catch (err) {
      console.error('Facial analysis failed:', err);
      setError('Analysis could not detect clear facial landmarks. Ensure your face is centered and illuminated.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 sm:p-6 space-y-4 shadow-xl">
      {/* Header Controls */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Camera className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-slate-100">Live Facial Analysis</h4>
            <p className="text-[11px] text-slate-400 font-mono">EmotionCNN & Eye Aspect Ratio (EAR)</p>
          </div>
        </div>

        {/* Ambient lighting badge & camera toggle */}
        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1.5 text-[11px] font-mono px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-300">
            <Sun className="w-3 h-3 text-amber-400" />
            <span className="hidden sm:inline">Lighting:</span> <strong className="text-slate-200">{lightingScore}</strong>
          </span>
          {cameraActive ? (
            <button
              onClick={stopCamera}
              className="min-w-[40px] min-h-[40px] flex items-center justify-center p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-xl transition-colors"
              title="Pause Camera"
              aria-label="Pause Camera"
            >
              <CameraOff className="w-4 h-4" />
            </button>
          ) : (
            <button
              onClick={startCamera}
              className="min-w-[40px] min-h-[40px] flex items-center justify-center p-2 text-slate-400 hover:text-indigo-400 hover:bg-slate-800 rounded-xl transition-colors"
              title="Activate Camera"
              aria-label="Activate Camera"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Video Viewport (Responsive 4:3 to 16:9 on mobile) */}
      <div className="relative w-full aspect-[4/3] sm:aspect-video rounded-2xl overflow-hidden bg-slate-950 border border-slate-800 flex items-center justify-center">
        {cameraActive ? (
          <>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              aria-label="Live webcam video stream"
              className="w-full h-full object-cover -scale-x-100"
            />
            {/* Guide overlay */}
            <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
              <div className="w-40 sm:w-48 h-56 sm:h-64 border-2 border-dashed border-indigo-500/40 rounded-3xl animate-pulse"></div>
            </div>
            {/* Live Indicator */}
            <div className="absolute top-3 left-3 flex items-center gap-2 bg-slate-950/80 backdrop-blur-md px-2.5 py-1 rounded-lg text-[10px] font-mono font-medium text-emerald-400 border border-slate-800">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              Live Tracking
            </div>
          </>
        ) : (
          <div className="text-center p-6 space-y-3">
            <CameraOff className="w-12 h-12 text-slate-700 mx-auto" />
            <p className="text-xs text-slate-400">Webcam stream currently inactive</p>
            <button
              onClick={startCamera}
              className="min-h-[44px] px-5 py-2.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-500 rounded-xl transition-all shadow-md shadow-indigo-600/20"
            >
              Activate Camera Feed
            </button>
          </div>
        )}
        <canvas ref={canvasRef} className="hidden" />
      </div>

      {error && (
        <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Action Button: Minimum 48px touch target for mobile */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pt-1">
        <p className="text-[11px] text-slate-400 text-center sm:text-left">
          Look straight into the frame with neutral expression.
        </p>
        <button
          onClick={captureAndAnalyze}
          disabled={!cameraActive || analyzing}
          className="min-h-[48px] flex items-center justify-center gap-2 px-6 py-3 text-xs font-bold text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 rounded-xl shadow-lg shadow-indigo-600/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
        >
          {analyzing ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Processing Convolutional Layers...
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              Capture & Analyze State
            </>
          )}
        </button>
      </div>

      {/* Real-time Result Summary Strip */}
      {lastResult && (
        <div className="p-4 rounded-2xl bg-slate-950/80 border border-slate-800 space-y-3 animate-fade-in">
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
            <span className="font-semibold text-slate-200 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Expression: <strong className="text-indigo-300 capitalize">{lastResult.dominant_emotion}</strong>
            </span>
            <span className="text-slate-400 font-mono text-[11px] flex items-center gap-1">
              <Eye className="w-3.5 h-3.5 text-slate-400" />
              EAR: <strong className="text-slate-200">{lastResult.eye_aspect_ratio}</strong>
            </span>
          </div>

          <div className="space-y-1.5 pt-1">
            <div className="flex justify-between text-[11px] font-mono text-slate-400">
              <span>Visual Stress Arousal</span>
              <span>{Math.round(lastResult.facial_stress_score * 100)}%</span>
            </div>
            <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
              <div
                className={`h-full transition-all duration-500 ${
                  lastResult.facial_stress_score > 0.52
                    ? 'bg-rose-500'
                    : lastResult.facial_stress_score > 0.38
                    ? 'bg-amber-500'
                    : 'bg-emerald-500'
                }`}
                style={{ width: `${Math.round(lastResult.facial_stress_score * 100)}%` }}
              ></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
