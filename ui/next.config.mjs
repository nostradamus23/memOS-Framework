/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
      remotePatterns: [
        {
          protocol: 'https',
          hostname: '**',
        },
        {
          protocol: 'http',
          hostname: '**',
        },
      ],
      dangerouslyAllowSVG: true,
      domains: ['localhost'],
    },
    typescript: {
      ignoreBuildErrors: true, // Solo para desarrollo, eliminar en producción
    },
    eslint: {
      ignoreDuringBuilds: true, // Solo para desarrollo, eliminar en producción
    },
  }

export default nextConfig;
