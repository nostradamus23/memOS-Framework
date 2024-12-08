import dotenv from 'dotenv';
dotenv.config();

export const CONFIG = {
  OPENAI_API_KEY: process.env.OPENAI_API_KEY || '',
};

if (!CONFIG.OPENAI_API_KEY) {
  throw new Error('OPENAI_API_KEY es requerida en el archivo .env');
}