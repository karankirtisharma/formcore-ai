'use client';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';
import { Image, Video, Camera } from 'lucide-react';

interface ModeSelectorProps {
    mode: 'image' | 'video' | 'live';
    setMode: (mode: 'image' | 'video' | 'live') => void;
}

export function ModeSelector({ mode, setMode }: ModeSelectorProps) {
    const modes = [
        { id: 'image', label: 'Image', icon: Image },
        { id: 'video', label: 'Video', icon: Video },
        { id: 'live', label: 'Live Cam', icon: Camera },
    ] as const;

    return (
        <div className="flex p-1 bg-surface-highlight/50 backdrop-blur-md rounded-full border border-white/5">
            {modes.map((m) => {
                const isActive = mode === m.id;
                const Icon = m.icon;

                return (
                    <button
                        key={m.id}
                        onClick={() => setMode(m.id)}
                        className={cn(
                            "relative flex items-center gap-2 px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 z-10",
                            isActive ? "text-white" : "text-text-secondary hover:text-white"
                        )}
                    >
                        {isActive && (
                            <motion.div
                                layoutId="activeMode"
                                className="absolute inset-0 bg-neon-primary rounded-full -z-10"
                                transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                            />
                        )}
                        <Icon className="w-4 h-4" />
                        {m.label}
                    </button>
                );
            })}
        </div>
    );
}
