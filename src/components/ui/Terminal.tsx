'use client';

import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { TerminalSquare, X, Minus, Square } from 'lucide-react';

interface TerminalLine {
    text: string;
    color?: string;
    delay?: number;
}

interface TerminalProps {
    lines: TerminalLine[];
    className?: string;
    title?: string;
}

export function Terminal({ lines, className, title = 'FormCore Analysis Engine' }: TerminalProps) {
    const [visibleLines, setVisibleLines] = useState<number>(0);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (visibleLines < lines.length) {
            const timeout = setTimeout(() => {
                setVisibleLines((prev) => prev + 1);
            }, lines[visibleLines].delay || 500);
            return () => clearTimeout(timeout);
        }
    }, [visibleLines, lines]);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [visibleLines]);

    return (
        <div className={cn('w-full rounded-xl overflow-hidden border border-white/10 bg-[#0F0F16] shadow-2xl font-mono text-sm tracking-tight', className)}>
            {/* Title Bar */}
            <div className="flex items-center justify-between px-4 py-2 bg-white/5 border-b border-white/5">
                <div className="flex items-center gap-2 text-text-secondary">
                    <TerminalSquare className="w-4 h-4" />
                    <span className="text-xs font-bold uppercase tracking-wider font-ndot">{title}</span>
                </div>
                <div className="flex items-center gap-2 text-text-secondary/50">
                    <Minus className="w-3 h-3 hover:text-white cursor-pointer" />
                    <Square className="w-3 h-3 hover:text-white cursor-pointer" />
                    <X className="w-3 h-3 hover:text-error cursor-pointer" />
                </div>
            </div>

            {/* Content */}
            <div ref={scrollRef} className="p-4 h-64 overflow-y-auto space-y-2 custom-scrollbar">
                {lines.slice(0, visibleLines).map((line, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="flex items-start gap-2"
                    >
                        <span className="text-white/30 select-none">❯</span>
                        <span className={cn('wrap-break-word', line.color || 'text-text-primary')}>
                            {line.text}
                        </span>
                    </motion.div>
                ))}
                <motion.div
                    animate={{ opacity: [0, 1, 0] }}
                    transition={{ repeat: Infinity, duration: 0.8 }}
                    className="w-2 h-4 bg-neon-primary inline-block ml-2 align-middle"
                />
            </div>
        </div>
    );
}
