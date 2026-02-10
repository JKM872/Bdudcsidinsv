import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Output standalone build for optimal Vercel deployment
  output: 'standalone',
  // Rewrite API calls to Flask backend
  async rewrites() {
    const apiUrl = process.env.API_URL || 'http://localhost:5000'
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ]
  },
};

export default nextConfig;
