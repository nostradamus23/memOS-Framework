export const OPENAI_CONFIG = {
  MODEL: process.env.MODEL || "gpt-4o-mini",
  API_KEY: process.env.OPENAI_API_KEY,
  MAX_TOKENS: 150,
  TEMPERATURE: 0.9,
};

export const RATE_LIMIT = {
  WINDOW_MS: 60 * 1000, // 1 minuto
  MAX_REQUESTS: 10,
};

export const DEFAULT_ERROR_MESSAGES = {
  INVALID_SESSION: 'Sesión inválida',
  MISSING_FIELDS: 'Faltan campos requeridos',
  OPENAI_ERROR: 'Error en la respuesta de OpenAI',
  RATE_LIMIT: 'Demasiadas solicitudes. Por favor, espera un momento.',
}; 