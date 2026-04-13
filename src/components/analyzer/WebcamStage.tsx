'use client';
import { useRef, useEffect } from 'react';
import Webcam from 'react-webcam';
import { Camera } from 'lucide-react';
import { useAnalyzerStore } from '@/store/useAnalyzerStore';
import { API_BASE_URL } from '@/lib/api';

export function WebcamStage() {
    const webcamRef = useRef<Webcam>(null);
    const { exercise, setLiveResults } = useAnalyzerStore();

    useEffect(() => {
        let abortController = new AbortController();
        let isProcessing = false;

        const processFrame = async () => {
            if (isProcessing || !webcamRef.current) return;
            
            const imageSrc = webcamRef.current.getScreenshot();
            if (!imageSrc) return;

            isProcessing = true;
            abortController.abort(); // Cancel any existing in-flight request
            abortController = new AbortController();

            try {
                // Convert base64 to Blob
                const res = await fetch(imageSrc);
                const blob = await res.blob();

                const formData = new FormData();
                formData.append('file', blob, 'frame.jpg');

                const endpoint = `${API_BASE_URL}/analyze/image?exercise=${exercise}`;
                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData,
                    signal: abortController.signal
                });

                if (response.ok) {
                    const data = await response.json();
                    setLiveResults(data);
                }
            } catch (err: any) {
                if (err.name !== 'AbortError') {
                    // Ignore abort errors
                    console.error('Frame processing error:', err);
                }
            } finally {
                isProcessing = false;
            }
        };

        const intervalId = setInterval(processFrame, 500); // 2 FPS

        return () => {
            clearInterval(intervalId);
            abortController.abort();
        };
    }, [exercise, setLiveResults]);

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
                <span className="text-xs font-mono text-text-secondary">2 FPS</span>
            </div>

            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-2 text-white/50 text-sm">
                <Camera className="w-4 h-4" />
                <span>Align your full body in frame</span>
            </div>
        </div>
    );
}
