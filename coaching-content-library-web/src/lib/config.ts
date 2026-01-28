function getEnvVar(key: string, defaultValue?: string): string {
  const value = import.meta.env[key] || defaultValue;
  if (!value) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  return value;
}

export const config = {
  apiUrl: getEnvVar('VITE_API_URL', 'http://localhost:8000'),
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD
} as const;
