'use client';
import { useState } from 'react';
import { Upload, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

interface DropZoneProps {
    mode: 'image' | 'video';
    onFileSelect: (file: File) => void;
}

export function DropZone({ mode, onFileSelect }: DropZoneProps) {
    const [isDragging, setIsDragging] = useState(false);

    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            validateAndUpload(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            validateAndUpload(e.target.files[0]);
        }
    };

    const validateAndUpload = (file: File) => {
        if (mode === 'image' && !file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }
        if (mode === 'video' && !file.type.startsWith('video/')) {
            alert('Please upload a video file');
            return;
        }
        onFileSelect(file);
    };

    const accept = mode === 'image' ? 'image/*' : 'video/*';

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-xl mx-auto"
        >
            <div
                className={cn(
                    "relative group cursor-pointer flex flex-col items-center justify-center w-full h-72 rounded-2xl border-2 border-dashed transition-all duration-500 overflow-hidden",
                    isDragging
                        ? "border-neon-primary bg-neon-primary/10 shadow-[0_0_50px_rgba(124,58,237,0.3)] scale-[1.02]"
                        : "border-white/10 bg-surface/30 hover:bg-surface/50 hover:border-neon-primary/50 hover:shadow-[0_0_30px_rgba(124,58,237,0.1)]"
                )}
                onDragOver={(e) => { e.preventDefault(); e.stopPropagation(); setIsDragging(true); }}
                onDragLeave={(e) => { e.preventDefault(); e.stopPropagation(); setIsDragging(false); }}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    accept={accept}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-50"
                    onChange={handleChange}
                />

                {/* Animated Background Mesh */}
                <div className="absolute inset-0 opacity-20 pointer-events-none">
                    <div className="absolute inset-0 bg-linear-to-b from-transparent to-background/50" />
                    <div className="absolute bottom-0 left-0 right-0 h-32 bg-linear-to-t from-neon-primary/10 to-transparent" />
                </div>

                <div className="relative z-10 flex flex-col items-center justify-center p-6 text-center">
                    <motion.div
                        animate={isDragging ? { scale: 1.1, rotate: [0, 5, -5, 0] } : { scale: 1, rotate: 0 }}
                        transition={{ duration: 0.4 }}
                        className={cn(
                            "mb-6 p-5 rounded-full border transition-all duration-300",
                            isDragging
                                ? "bg-neon-primary text-white border-neon-primary shadow-[0_0_20px_var(--neon-primary)]"
                                : "bg-surface-highlight border-white/5 text-neon-primary group-hover:scale-110 group-hover:border-neon-primary/50"
                        )}
                    >
                        {isDragging ? <Sparkles className="w-10 h-10" /> : <Upload className="w-10 h-10" />}
                    </motion.div>

                    <h3 className="mb-2 text-2xl font-display font-medium text-white group-hover:text-neon-primary transition-colors">
                        {isDragging ? "Drop it here!" : "Upload Media"}
                    </h3>

                    <p className="text-text-secondary max-w-[200px] leading-relaxed">
                        {mode === 'image' ? 'Drag & drop your pose image or click to browse' : 'Upload a video for frame-by-frame analysis'}
                    </p>

                    {/* Badge */}
                    <div className="mt-6 flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/5 text-xs text-text-secondary">
                        <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
                        {mode === 'image' ? 'JPG, PNG, WEBP' : 'MP4, MOV, WEBM'}
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
