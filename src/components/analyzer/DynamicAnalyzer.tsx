'use client';
import dynamic from 'next/dynamic';

export const DynamicAnalyzer = dynamic(
  () => import('./AnalyzerContainer').then(mod => mod.AnalyzerContainer),
  {
    loading: () => (
      <div className="w-full max-w-6xl mx-auto px-6 py-24 flex items-center justify-center">
        <div className="text-text-secondary font-mono text-sm animate-pulse">Loading analyzer...</div>
      </div>
    ),
    ssr: false
  }
);
