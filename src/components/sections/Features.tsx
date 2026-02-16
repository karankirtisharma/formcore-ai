'use client';

import { motion } from 'framer-motion';
import { BentoCard } from '@/components/ui/BentoCard';
import { TextAnimate } from '@/components/ui/TextAnimate';
import { ScanLine, Cpu, Zap, Lock } from 'lucide-react';

const features = [
    {
        title: 'Real-Time Analysis',
        description: 'Computer vision engine processes 60 frames per second for instant feedback.',
        icon: ScanLine,
        className: 'md:col-span-2',
        delay: 0.1,
    },
    {
        title: 'Neural Processing',
        description: 'Advanced algorithms map 33 diverse skeletal points.',
        icon: Cpu,
        className: 'md:col-span-1',
        delay: 0.2,
    },
    {
        title: 'Instant Feedback',
        description: 'Get corrections on your form typically within 200ms.',
        icon: Zap,
        className: 'md:col-span-1',
        delay: 0.3,
    },
    {
        title: 'Privacy First',
        description: 'All processing happens locally or on secure ephemeral instances.',
        icon: Lock,
        className: 'md:col-span-2',
        delay: 0.4,
    },
];

export function Features() {
    return (
        <section id="features" className="container mx-auto px-6 py-24">
            <div className="mb-16 text-center">
                <h2 className="text-3xl font-display font-bold text-white md:text-5xl mb-4">
                    <TextAnimate text="Advanced Biometrics" type="whipIn" />
                </h2>
                <p className="text-white max-w-2xl mx-auto font-sans text-lg leading-relaxed mix-blend-plus-lighter">
                    Our proprietary neural engine breaks down complex movements into actionable data points.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
                {features.map((feature, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: feature.delay, duration: 0.5 }}
                        className={feature.className}
                    >
                        <BentoCard glow className="h-full flex flex-col justify-between group hover:border-neon-primary/50 transition-colors duration-500">
                            <div className="mb-4 p-3 w-fit rounded-lg bg-surface-highlight border border-white/5 group-hover:scale-110 transition-transform duration-300">
                                <feature.icon className="w-6 h-6 text-neon-primary" />
                            </div>

                            <div>
                                <h3 className="text-xl font-display font-bold uppercase tracking-wide text-white mb-2 group-hover:text-neon-primary transition-colors">
                                    {feature.title}
                                </h3>
                                <p className="font-sans text-text-secondary text-sm leading-relaxed tracking-wide">
                                    {feature.description}
                                </p>
                            </div>
                        </BentoCard>
                    </motion.div>
                ))}
            </div>
        </section>
    );
}
