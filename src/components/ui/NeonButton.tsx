'use client';
import { cn } from '@/lib/utils';
import { motion, HTMLMotionProps } from 'framer-motion';

interface NeonButtonProps extends HTMLMotionProps<"button"> {
    variant?: 'primary' | 'secondary' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    glow?: boolean;
}

export function NeonButton({
    className,
    variant = 'primary',
    size = 'md',
    glow = true,
    children,
    ...props
}: NeonButtonProps) {
    const variants = {
        primary: "bg-neon-primary text-white hover:bg-neon-primary/90 border-transparent",
        secondary: "bg-surface-highlight text-white border-white/10 hover:bg-white/10",
        danger: "bg-error/10 text-error border-error/20 hover:bg-error/20"
    };

    const sizes = {
        sm: "h-8 px-4 text-xs",
        md: "h-10 px-6 text-sm",
        lg: "h-12 px-8 text-base"
    };

    return (
        <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={cn(
                "relative inline-flex items-center justify-center rounded-full font-ndot font-bold uppercase tracking-wider transition-all duration-300",
                "border backdrop-blur-sm",
                variants[variant],
                sizes[size],
                glow && variant === 'primary' && "shadow-[0_0_15px_rgba(124,58,237,0.5)] hover:shadow-[0_0_25px_rgba(124,58,237,0.7)]",
                className
            )}
            {...props}
        >
            {children}
        </motion.button>
    );
}
