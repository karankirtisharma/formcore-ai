import { cn } from '@/lib/utils';

interface GridOverlayProps {
    className?: string;
}

export function GridOverlay({ className }: GridOverlayProps) {
    return (
        <div className={cn("absolute inset-0 pointer-events-none overflow-hidden", className)}>
            {/* Horizontal lines */}
            <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px)] bg-size-[40px_40px]" />
            {/* Vertical lines */}
            <div className="absolute inset-0 bg-[linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-size-[40px_40px]" />

            {/* Radial fade */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_800px_at_50%_50%,transparent,var(--background))]" />
        </div>
    );
}
