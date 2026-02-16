import Link from 'next/link';

export function Footer() {
    return (
        <footer className="border-t border-white/5 bg-background py-12 relative overflow-hidden">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-1/2 h-px bg-linear-to-r from-transparent via-neon-primary/50 to-transparent" />

            <div className="container mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
                <div className="flex items-center gap-2">
                    <span className="font-display font-bold text-lg text-white">
                        FormCore<span className="text-neon-primary">.AI</span>
                    </span>
                    <span className="text-text-secondary/50 text-sm">© 2024 Neural Lab</span>
                </div>

                <div className="flex items-center gap-8 text-sm text-text-secondary">
                    <Link href="#" className="hover:text-neon-primary transition-colors">Privacy Protocol</Link>
                    <Link href="#" className="hover:text-neon-primary transition-colors">Terminals</Link>
                    <Link href="#" className="hover:text-neon-primary transition-colors">System Status</Link>
                </div>
            </div>
        </footer>
    );
}
