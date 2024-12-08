require('dotenv').config();

const requiredEnvVars = [
  'OPENAI_API_KEY',
];

const defaultValues = {
  MODEL: 'gpt-4o-mini',
  NODE_ENV: 'development',
  RATE_LIMIT_WINDOW_MS: '60000',
  RATE_LIMIT_MAX_REQUESTS: '10'
};

function verifyEnv() {
  // Establecer valores por defecto si no existen
  Object.entries(defaultValues).forEach(([key, value]) => {
    if (!process.env[key]) {
      process.env[key] = value;
      console.log(`\x1b[33m%s\x1b[0m`, `Warning: Using default value for ${key}: ${value}`);
    }
  });

  const missingVars = requiredEnvVars.filter(envVar => !process.env[envVar]);
  
  if (missingVars.length > 0) {
    console.error('\x1b[31m%s\x1b[0m', 'Error: Missing required environment variables:');
    missingVars.forEach(envVar => {
      console.error(`  - ${envVar}`);
    });
    console.log('\nPlease add these variables to your environment or .env file');
    process.exit(1);
  }
  
  console.log('\x1b[32m%s\x1b[0m', '✓ All required environment variables are set');
}

verifyEnv(); 