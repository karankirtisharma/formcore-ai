declare module 'lenis' {
    export default class Lenis {
        constructor(options?: Record<string, unknown>);
        raf(time: number): void;
        destroy(): void;
        on(event: string, callback: (args: Record<string, unknown>) => void): void;
    }
}
