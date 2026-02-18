import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  // Static export – Flask serves the built HTML/JS/CSS
  output: 'export',
  // Required for static export with next/image (if used later)
  images: { unoptimized: true },
  // Explicitly set Turbopack root to this directory (not the repo root)
  // Prevents "module not found" when Vercel removes root package-lock.json
  turbopack: {
    root: path.resolve(__dirname),
  },
};

export default nextConfig;
