'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, Activity } from 'lucide-react';
import { cn } from '@/lib/utils';
import { NeonButton } from '@/components/ui/NeonButton';

const navItems = [
    { name: 'Home', href: '/' },
    { name: 'Analysis', href: '#analyzer' },
    { name: 'Features', href: '#features' },
    { name: 'About', href: '#about' },
];

export function Navbar() {
    const [scrolled, setScrolled] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const pathname = usePathname();

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <header
            className={cn(
                'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
                scrolled
                    ? 'bg-background/80 backdrop-blur-md border-b border-white/5 py-3'
                    : 'bg-transparent py-5'
            )}
        >
            <div className="container mx-auto px-6 flex items-center justify-between">
                {/* Logo */}
                <Link href="/" className="flex items-center gap-2 group">
                    <div className="relative flex items-center justify-center w-8 h-8 rounded-lg bg-surface-highlight border border-white/10 group-hover:border-neon-primary/50 transition-colors">
                        <Activity className="w-5 h-5 text-neon-primary" />
                        <div className="absolute inset-0 bg-neon-primary/20 blur-lg opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                    <span className="font-ndot font-bold text-xl tracking-tight text-white">
                        FormCore<span className="text-neon-primary">.AI</span>
                    </span>
                </Link>

                {/* Desktop Nav */}
                <nav className="hidden md:flex items-center gap-8">
                    {navItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className="relative text-sm font-medium text-text-secondary hover:text-white transition-colors group font-ndot tracking-wider"
                        >
                            {item.name}
                            <span className="absolute -bottom-1 left-0 w-0 h-[2px] bg-neon-primary transition-all duration-300 group-hover:w-full box-shadow-[0_0_8px_var(--neon-primary)]" />
                            {pathname === item.href && (
                                <motion.span
                                    layoutId="navbar-indicator"
                                    className="absolute -bottom-1 left-0 w-full h-[2px] bg-neon-primary"
                                    transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                                />
                            )}
                        </Link>
                    ))}
                </nav>

                {/* CTA & Mobile Toggle */}
                <div className="flex items-center gap-4">
                    <NeonButton size="sm" className="hidden md:flex">
                        Get Started
                    </NeonButton>

                    <button
                        onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        className="md:hidden p-2 text-text-secondary hover:text-white transition-colors"
                    >
                        {mobileMenuOpen ? <X /> : <Menu />}
                    </button>
                </div>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {mobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="md:hidden bg-surface/95 backdrop-blur-xl border-b border-white/10 overflow-hidden"
                    >
                        <div className="container mx-auto px-6 py-6 flex flex-col gap-4">
                            {navItems.map((item) => (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    onClick={() => setMobileMenuOpen(false)}
                                    className="text-lg font-medium text-text-secondary hover:text-white transition-colors p-2 hover:bg-white/5 rounded-lg font-ndot tracking-wider"
                                >
                                    {item.name}
                                </Link>
                            ))}
                            <NeonButton className="w-full mt-2">Get Started</NeonButton>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </header>
    );
}
