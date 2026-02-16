'use client';
import { useRef } from 'react';
import Webcam from 'react-webcam';
import { Camera } from 'lucide-react';

export function WebcamStage() {
    const webcamRef = useRef<Webcam>(null);

    return (
        <div className="relative w-full aspect-video rounded-xl overflow-hidden bg-black/50 border border-white/10 shadow-2xl">
            <Webcam
                ref={webcamRef}
                audio={false}
                className="w-full h-full object-cover"
                screenshotFormat="image/jpeg"
            />



            {/* Floating Status Pill */}
            <div className="absolute top-4 right-4 flex items-center gap-3 px-4 py-2 bg-black/60 backdrop-blur-md rounded-full border border-white/10">
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
                    <span className="text-xs font-mono text-white">LIVE</span>
                </div>
                <div className="w-px h-3 bg-white/20" />
                <span className="text-xs font-mono text-text-secondary">30 FPS</span>
            </div>

            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-2 text-white/50 text-sm">
                <Camera className="w-4 h-4" />
                <span>Align your full body in frame</span>
            </div>
        </div>
    );
}
