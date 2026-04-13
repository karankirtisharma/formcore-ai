'use client';
import { AnimatePresence, motion } from 'framer-motion';
import { useAnalyzerStore } from '@/store/useAnalyzerStore';
import { API_BASE_URL } from '@/lib/api';
import { ModeSelector } from './ModeSelector';
import { DropZone } from './DropZone';
import { WebcamStage } from './WebcamStage';
import { ResultsView } from './ResultsView';
import { BentoCard } from '@/components/ui/BentoCard';
import { ScanLine } from 'lucide-react';

export function AnalyzerContainer() {
    const { mode, setMode, status, setStatus, setResults, exercise, resultData } = useAnalyzerStore();

    const handleFileSelect = async (file: File) => {
        setStatus('uploading');

        try {
            const formData = new FormData();
            formData.append('file', file);

            const endpoint = file.type.startsWith('video/')
                ? `${API_BASE_URL}/analyze/video?exercise=${exercise}`
                : `${API_BASE_URL}/analyze/image?exercise=${exercise}`;

            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Analysis failed');
            }

            const data = await response.json();

            if (file.type.startsWith('video/')) {
                setStatus('processing');
                const jobId = data.job_id;
                
                // Poll for result
                const pollInterval = setInterval(async () => {
                    try {
                        const pollRes = await fetch(`${API_BASE_URL}/result/${jobId}`);
                        const pollData = await pollRes.json();
                        
                        if (pollData.status === 'complete') {
                            clearInterval(pollInterval);
                            setResults(pollData.result);
                        } else if (pollData.status === 'error') {
                            clearInterval(pollInterval);
                            setStatus('idle');
                            alert('Video analysis failed: ' + pollData.message);
                        }
                    } catch (e) {
                        clearInterval(pollInterval);
                        setStatus('idle');
                        alert('Error polling status');
                    }
                }, 2000);
            } else {
                setStatus('processing');
                setTimeout(() => {
                    setResults(data);
                }, 500);
            }

        } catch {
            setStatus('idle');
            alert('Error analyzing media. Ensure backend is running.');
        }
    };

    return (
        <section id="analyzer" className="container mx-auto px-6 py-24">
            <div className="flex flex-col items-center gap-8">
                <div className="text-center space-y-4">
                    <h2 className="relative z-10 text-3xl font-bold text-white md:text-4xl font-display uppercase tracking-wide">
                        <span className="text-neon-primary">AI</span> Analysis Lab
                    </h2>
                    <p className="text-white max-w-lg mx-auto font-sans text-lg leading-relaxed mix-blend-plus-lighter">
                        Select your input method and let our neural networks analyze your biomechanics in real-time.
                    </p>
                </div>

                <div className="flex flex-col md:flex-row items-center gap-6 z-20">
                    <ModeSelector mode={mode} setMode={setMode} />
                </div>

                <div className="w-full max-w-5xl relative">
                    <BentoCard className="min-h-[600px] flex flex-col items-center justify-center p-8 md:p-12 transition-all duration-500">
                        <AnimatePresence mode="wait">
                            {status === 'complete' ? (
                                <motion.div
                                    key="results"
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -20 }}
                                    className="w-full"
                                >
                                    <ResultsView />
                                </motion.div>
                            ) : (
                                <motion.div
                                    key={mode}
                                    initial={{ opacity: 0, scale: 0.95 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.95 }}
                                    transition={{ duration: 0.3 }}
                                    className="w-full h-full flex items-center justify-center"
                                >
                                    {mode === 'image' && <DropZone mode="image" onFileSelect={handleFileSelect} />}
                                    {mode === 'video' && <DropZone mode="video" onFileSelect={handleFileSelect} />}
                                    {mode === 'live' && (
                                        <div className="flex flex-col gap-6 w-full">
                                            <WebcamStage />
                                            {resultData && <ResultsView />}
                                        </div>
                                    )}
                                </motion.div>
                            )}
                        </AnimatePresence>

                        {/* Processing Overlay */}
                        {status === 'processing' && (
                            <div className="absolute inset-0 z-50 bg-black/80 backdrop-blur-sm flex flex-col items-center justify-center rounded-2xl">
                                <div className="relative w-24 h-24 mb-6">
                                    <div className="absolute inset-0 border-4 border-neon-primary/30 rounded-full animate-ping" />
                                    <div className="absolute inset-0 border-4 border-neon-primary rounded-full border-t-transparent animate-spin" />
                                    <ScanLine className="absolute inset-0 m-auto w-8 h-8 text-white animate-pulse" />
                                </div>
                                <h3 className="text-xl font-bold text-white animate-pulse">Running Neural Analysis...</h3>
                                <p className="text-neon-secondary mt-2">Extracting 33 skeletal landmarks</p>
                            </div>
                        )}

                        {status === 'uploading' && (
                            <div className="absolute inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center rounded-2xl">
                                <h3 className="text-xl font-bold text-white animate-bounce">Uploading...</h3>
                            </div>
                        )}
                    </BentoCard>
                </div>
            </div>
        </section>
    );
}
