import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Static export – Flask serves the built HTML/JS/CSS
  output: 'export',
  // Required for static export with next/image (if used later)
  images: { unoptimized: true },
  // Explicitly set Turbopack root to this directory (not the repo root)
  turbopack: {
    root: __dirname,
  },
};

export default nextConfig;
