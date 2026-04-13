import { DynamicAnalyzer } from '@/components/analyzer/DynamicAnalyzer';
import { GlowingEffect } from '@/components/ui/GlowingEffect';
import { Navbar } from '@/components/layout/Navbar';
import { Hero } from '@/components/layout/Hero';
import { Features } from '@/components/sections/Features';
import { Footer } from '@/components/layout/Footer';

export default function Home() {
  return (
    <main className="min-h-screen relative overflow-hidden bg-background text-foreground">
      {/* Background Ambience */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <video
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 w-full h-full object-cover opacity-20 mix-blend-screen"
        >
          <source src="/backgrounds/GOJO.mp4" type="video/mp4" />
        </video>
        <div className="absolute inset-0 bg-background/80 backdrop-blur-[2px]" />

        <GlowingEffect
          blur={120}
          inactiveZone={0.1}
          proximity={1000}
          spread={100}
          borderWidth={0}
          movementDuration={4}
          disabled={false}
          className="opacity-20"
        />
      </div>

      <Navbar />
      <Hero />
      <Features />
      <DynamicAnalyzer />
      <Footer />
    </main>
  );
}
