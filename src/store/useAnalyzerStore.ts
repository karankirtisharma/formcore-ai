import { create } from 'zustand';

export interface AnalysisResult {
    score: number;
    mistakes: string[];
    image_base64?: string;
    video_base64?: string;
}

interface AnalyzerState {
    mode: 'image' | 'video' | 'live';
    status: 'idle' | 'uploading' | 'processing' | 'complete';
    resultData: AnalysisResult | null;
    exercise: string;
    exercises: string[];

    setMode: (mode: 'image' | 'video' | 'live') => void;
    setStatus: (status: 'idle' | 'uploading' | 'processing' | 'complete') => void;
    setExercise: (exercise: string) => void;
    setExercises: (exercises: string[]) => void;
    startProcessing: () => void;
    setResults: (data: AnalysisResult) => void;
    reset: () => void;
}

export const useAnalyzerStore = create<AnalyzerState>((set) => ({
    mode: 'image',
    status: 'idle',
    resultData: null,
    exercise: 'squat',
    exercises: [],

    setMode: (mode) => set({ mode, status: 'idle', resultData: null }),
    setStatus: (status) => set({ status }),
    setExercise: (exercise) => set({ exercise }),
    setExercises: (exercises) => set({ exercises }),
    startProcessing: () => set({ status: 'processing' }),
    setResults: (data) => set({ resultData: data, status: 'complete' }),
    reset: () => set({ status: 'idle', resultData: null }),
}));
