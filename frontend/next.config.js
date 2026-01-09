/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    MATRIX_SERVER: process.env.MATRIX_SERVER || 'http://localhost:8008',
    AI_BACKEND: process.env.AI_BACKEND || 'http://localhost:8000',
  },
}

module.exports = nextConfig
