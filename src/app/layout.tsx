import type { Metadata } from "next";
import localFont from "next/font/local";
import dynamic from "next/dynamic";
import "./globals.css";

const SmoothScroll = dynamic(() => import("@/components/ui/SmoothScroll"));

const ndot = localFont({
  src: "../public/fonts/Ndot-55.otf",
  variable: "--font-ndot",
  display: "swap",
});

const ntypeHeadline = localFont({
  src: "../public/fonts/NType82-Headline.otf",
  variable: "--font-ntype-headline",
  display: "swap",
  preload: false,
});

const ntypeRegular = localFont({
  src: "../public/fonts/NType82-Regular.otf",
  variable: "--font-ntype-regular",
  display: "swap",
  preload: false,
});

const letteraMono = localFont({
  src: "../public/fonts/LetteraMonoLL-Regular.otf",
  variable: "--font-lettera-mono",
  display: "swap",
  preload: false,
});

export const metadata: Metadata = {
  title: "FormCore AI",
  description: "Cinematic AI Exercise Form Analysis",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${ndot.variable} ${ntypeHeadline.variable} ${ntypeRegular.variable} ${letteraMono.variable} antialiased bg-background text-foreground font-sans`}
      >
        <SmoothScroll />
        {children}
      </body>
    </html>
  );
}
