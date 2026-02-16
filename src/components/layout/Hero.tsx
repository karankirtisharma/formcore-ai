'use client';
import { NeonButton } from '@/components/ui/NeonButton';
import { GridOverlay } from '@/components/ui/GridOverlay';
import { TextAnimate } from '@/components/ui/TextAnimate';
import { Spotlight } from '@/components/ui/Spotlight';
import { ArrowRight, ScanLine } from 'lucide-react';
import { motion } from 'framer-motion';

export function Hero() {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
            <Spotlight className="-top-40 left-0 md:left-60 md:-top-20" fill="white" />
            <GridOverlay />

            {/* Background Glows */}
            <div className="absolute top-1/4 left-1/4 h-96 w-96 rounded-full bg-neon-primary/20 blur-[128px]" />
            <div className="absolute bottom-1/4 right-1/4 h-96 w-96 rounded-full bg-neon-secondary/20 blur-[128px]" />

            <div className="container relative z-10 mx-auto px-6 text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    className="mx-auto max-w-4xl"
                >
                    {/* Pill Badge */}
                    <div className="mx-auto mb-6 flex w-fit items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-1.5 backdrop-blur-sm">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-neon-primary opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-neon-primary"></span>
                        </span>
                        <TextAnimate text="AI-Powered Form Analysis" type="calmIn" className="text-xs font-medium text-neon-secondary font-ndot tracking-wider" as="span" />
                    </div>

                    <div className="mb-8 font-mono uppercase leading-none tracking-tight">
                        <div className="flex items-baseline justify-center gap-2 md:gap-4 text-white">
                            <h1 className="text-6xl md:text-8xl font-bold drop-shadow-2xl">MASTER</h1>
                            <span className="text-2xl md:text-4xl opacity-60 tracking-widest">YOUR</span>
                        </div>
                        <div className="flex items-baseline justify-center gap-2 md:gap-4 mt-1 md:mt-2">
                            <span className="text-2xl md:text-4xl opacity-60 tracking-widest text-white">BIO</span>
                            <span className="text-6xl md:text-8xl font-bold text-transparent bg-clip-text bg-linear-to-r from-neon-primary to-neon-secondary text-glow drop-shadow-2xl">
                                MECHANICS
                            </span>
                        </div>
                    </div>

                    <p className="mb-8 font-sans text-lg text-text-secondary md:text-xl max-w-2xl mx-auto leading-relaxed tracking-wide">
                        Real-time computer vision analysis for squats, pushups, and deadlifts.
                        Upload a video or use your webcam to get instant feedback on your form.
                    </p>

                    {/* CTAs */}
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <NeonButton size="lg" className="group font-sans tracking-wide" onClick={() => document.getElementById('analyzer')?.scrollIntoView({ behavior: 'smooth' })}>
                            Start Analysis
                            <ScanLine className="ml-2 h-4 w-4 transition-transform group-hover:scale-110" />
                        </NeonButton>
                        <NeonButton variant="secondary" size="lg">
                            View Demo
                            <ArrowRight className="ml-2 h-4 w-4" />
                        </NeonButton>
                    </div>
                </motion.div>
            </div>
        </section>
    );
}
