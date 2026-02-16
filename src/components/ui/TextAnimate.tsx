'use client';

import { motion, Variants } from 'framer-motion';

interface TextAnimateProps {
    text: string;
    type?: 'fadeIn' | 'popIn' | 'shiftIn' | 'rollIn' | 'whipIn' | 'calmIn' | 'neonPulse';
    delay?: number;
    duration?: number;
    className?: string;
    as?: React.ElementType;
}

export const TextAnimate = ({
    text,
    type = 'whipIn',
    delay = 0,
    duration = 0.05,
    className,
    as: Component = 'div',
}: TextAnimateProps) => {
    const letters = Array.from(text);

    const container: Variants = {
        hidden: { opacity: 0 },
        visible: (i: number = 1) => ({
            opacity: 1,
            transition: { staggerChildren: duration, delayChildren: i * delay },
        }),
    };

    const child: Variants = {
        visible: {
            opacity: 1,
            y: 0,
            x: 0,
            scale: 1,
            rotate: 0,
            filter: 'blur(0px)',
            transition: {
                type: 'spring' as const,
                damping: 12,
                stiffness: 100,
            },
        },
        hidden: {
            opacity: 0,
            y: type === 'shiftIn' ? 20 : type === 'popIn' ? -20 : 0,
            x: type === 'whipIn' ? -20 : 0,
            scale: type === 'popIn' ? 0.5 : 1,
            rotate: type === 'rollIn' ? -45 : 0,
            filter: type === 'calmIn' ? 'blur(10px)' : 'blur(0px)',
        },
        neonPulse: {
            opacity: [1, 0.5, 1],
            textShadow: [
                '0 0 5px var(--neon-primary)',
                '0 0 10px var(--neon-primary)',
                '0 0 5px var(--neon-primary)',
            ],
            transition: {
                duration: 1.5,
                repeat: Infinity,
                ease: 'easeInOut',
            },
        }
    };

    if (type === 'neonPulse') {
        return (
            <Component className={className}>
                <motion.span
                    animate="neonPulse"
                    variants={child}
                >
                    {text}
                </motion.span>
            </Component>
        )
    }

    return (
        <Component className={className}>
            <motion.div
                style={{ display: 'flex', flexWrap: 'wrap' }}
                variants={container}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
            >
                {letters.map((letter, index) => (
                    <motion.span key={index} variants={child}>
                        {letter === ' ' ? '\u00A0' : letter}
                    </motion.span>
                ))}
            </motion.div>
        </Component>
    );
};
