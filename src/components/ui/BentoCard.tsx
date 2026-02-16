import { cn } from '@/lib/utils';
import { GlowingEffect } from './GlowingEffect';

interface BentoCardProps {
    children: React.ReactNode;
    className?: string;
    glow?: boolean;
}

export function BentoCard({ children, className, glow = false }: BentoCardProps) {
    return (
        <div
            className={cn(
                'group relative overflow-hidden rounded-xl border border-white/10 bg-surface px-8 py-6 shadow-2xl transition-all duration-300 hover:shadow-neon-primary/20',
                className
            )}
        >
            {glow && (
                <GlowingEffect
                    spread={40}
                    blur={0}
                    proximity={64}
                    inactiveZone={0.01}
                    borderWidth={3}
                    movementDuration={2}
                    disabled={false}
                />
            )}
            <div className="relative z-10">{children}</div>
        </div>
    );
}
