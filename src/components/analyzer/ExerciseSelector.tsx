'use client';

import { useEffect } from 'react';
import { API_BASE_URL } from '@/lib/api';
import { useAnalyzerStore } from '@/store/useAnalyzerStore';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";

// Fallback list in case backend is unreachable
const FALLBACK_EXERCISES = ["squat", "pushup", "deadlift"];

interface ExerciseSelectorProps {
    exercise: string;
    setExercise: (val: string) => void;
    disabled?: boolean;
}

export function ExerciseSelector({ exercise, setExercise, disabled }: ExerciseSelectorProps) {
    const { exercises, setExercises } = useAnalyzerStore();

    useEffect(() => {
        let cancelled = false;
        fetch(`${API_BASE_URL}/exercises`)
            .then(res => res.json())
            .then(data => {
                if (!cancelled && data.exercises?.length) {
                    setExercises(data.exercises);
                }
            })
            .catch(() => {
                if (!cancelled) setExercises(FALLBACK_EXERCISES);
            });
        return () => { cancelled = true; };
    }, [setExercises]);

    const list = exercises.length ? exercises : FALLBACK_EXERCISES;

    const formatLabel = (s: string) =>
        s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

    return (
        <div className="z-20 w-full max-w-xs">
            <Select value={exercise} onValueChange={setExercise} disabled={disabled}>
                <SelectTrigger className="w-full bg-surface-highlight/50 backdrop-blur-md border border-white/10 text-white rounded-full h-12 px-6">
                    <SelectValue placeholder="Select Exercise" />
                </SelectTrigger>
                <SelectContent className="bg-black/90 border-neon-primary/20 backdrop-blur-xl text-white max-h-64 overflow-y-auto">
                    {list.map(ex => (
                        <SelectItem key={ex} value={ex}>{formatLabel(ex)}</SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </div>
    );
}
