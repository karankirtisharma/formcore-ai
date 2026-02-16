'use client';

import { BentoCard } from '@/components/ui/BentoCard';
import { useAnalyzerStore } from '@/store/useAnalyzerStore';
import { NeonButton } from '@/components/ui/NeonButton';
import { Terminal } from '@/components/ui/Terminal';
import { motion } from 'framer-motion';

import { memo } from 'react';

const MediaDisplay = memo(({ video_base64, image_base64 }: { video_base64?: string, image_base64?: string }) => (
    <BentoCard glow className="relative overflow-hidden flex items-center justify-center bg-black/50 border-neon-primary/20">
        {video_base64 ? (
            <>
                <video
                    src={`data:video/mp4;base64,${video_base64}`}
                    controls
                    autoPlay
                    loop
                    muted
                    className="w-full rounded-lg object-contain z-10"
                />
                <div className="absolute top-4 right-4 z-30 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full border border-white/10 text-xs text-neon-primary font-mono">
                    VIDEO_FEED :: TRACKED
                </div>
            </>
        ) : image_base64 ? (
            <>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                    src={`data:image/jpeg;base64,${image_base64}`}
                    alt="Pose Analysis Result"
                    className="w-full rounded-lg object-contain z-10"
                />
                <div className="absolute top-4 right-4 z-30 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full border border-white/10 text-xs text-neon-primary font-mono">
                    LIVE_FEED :: PROCESSED
                </div>
            </>
        ) : (
            <div className="text-text-secondary font-mono py-32">NO_SIGNAL</div>
        )}
    </BentoCard>
));
MediaDisplay.displayName = 'MediaDisplay';

export function ResultsView() {
    const { resultData, reset } = useAnalyzerStore();

    if (!resultData) return null;

    const { score, mistakes, image_base64, video_base64 } = resultData;

    // Generate terminal lines based on analysis
    const terminalLines = [
        { text: '> Initializing neural network...', delay: 0 },
        { text: '> Loading pose estimation model (BlazePose)...', delay: 200 },
        { text: '> Analyzing frame geometry...', delay: 400 },
        { text: `> Detected skeletal confidence: ${(score * 0.9 + 10).toFixed(1)}%`, color: 'text-success', delay: 800 },
        { text: '----------------------------------------', color: 'text-white/20', delay: 1000 },
        { text: `> BIOMECHANICAL ANALYSIS COMPLETE`, color: 'text-neon-primary', delay: 1200 },
        { text: `> FORM SCORE: ${score}/100`, color: score > 70 ? 'text-success' : 'text-error', delay: 1400 },
        ...mistakes.map((m, i) => ({
            text: `[CRITICAL] ${m}`,
            color: 'text-error',
            delay: 1600 + i * 400
        })),
        ...(mistakes.length === 0 ? [{ text: '> No critical faults detected.', color: 'text-success', delay: 1600 }] : []),
        { text: '> Session data archived.', color: 'text-text-secondary', delay: 2000 + mistakes.length * 400 }
    ];

    return (
        <div className="w-full max-w-6xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Visual Analysis Column */}
                <div className="lg:col-span-2 space-y-6">
                    <MediaDisplay video_base64={video_base64} image_base64={image_base64} />
                </div>

                {/* Data Column */}
                <div className="space-y-6 flex flex-col h-full">
                    {/* Score Card */}
                    <BentoCard className="flex-none bg-surface/80 backdrop-blur-sm">
                        <div className="flex items-center justify-between mb-2">
                            <h3 className="text-xs font-mono text-text-secondary uppercase tracking-widest">Efficiency Rating</h3>
                            <span className={score > 80 ? "text-success" : "text-error"}>●</span>
                        </div>
                        <div className="flex items-end gap-2">
                            <span className="text-6xl font-display font-black tracking-tighter text-white tabular-nums">{score}</span>
                            <span className="text-xl font-display font-medium text-text-secondary mb-2">/100</span>
                        </div>
                        <div className="w-full bg-white/5 h-1 mt-4 rounded-full overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${score}%` }}
                                transition={{ duration: 1.5, ease: "easeOut", delay: 0.5 }}
                                className={`h-full ${score > 80 ? 'bg-success' : 'bg-error'} shadow-[0_0_10px_currentColor]`}
                            />
                        </div>
                    </BentoCard>

                    {/* Terminal Log */}
                    <div className="grow min-h-[250px] flex flex-col">
                        <Terminal lines={terminalLines} className="h-full w-full shadow-2xl" title="NEURAL_ENGINE_V1" />
                    </div>

                    <NeonButton onClick={reset} variant="secondary" className="w-full mt-auto">
                        New Analysis
                    </NeonButton>
                </div>
            </div>
        </div>
    );
}
