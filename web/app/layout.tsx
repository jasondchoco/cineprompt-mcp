import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CinePrompt — Turn any film into an AI video blueprint",
  description:
    "Search any movie or TV show and get a cinematic reference pack, shot list, and AI video prompt — with built-in copyright safety.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col bg-zinc-950 text-zinc-100 antialiased">
        <nav className="border-b border-zinc-800 px-6 py-3 flex items-center gap-6">
          <a href="/" className="text-amber-400 font-bold tracking-tight text-lg">
            🎬 CinePrompt
          </a>
          <a href="/" className="text-sm text-zinc-400 hover:text-zinc-100 transition-colors">
            Search
          </a>
        </nav>
        <main className="flex-1">{children}</main>
        <footer className="border-t border-zinc-800 px-6 py-4 text-xs text-zinc-600 text-center">
          Data from TMDb · Prompts are original — no direct content copying
        </footer>
      </body>
    </html>
  );
}
