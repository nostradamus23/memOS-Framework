interface RateLimitStore {
  [key: string]: {
    count: number;
    timestamp: number;
  }
}

const store: RateLimitStore = {};

export async function rateLimit(ip: string) {
  const now = Date.now();
  const windowMs = 60 * 1000; // 1 minuto
  const limit = 10; // máximo de solicitudes por ventana

  // Limpiar entradas antiguas
  for (const key in store) {
    if (now - store[key].timestamp > windowMs) {
      delete store[key];
    }
  }

  // Verificar y actualizar el límite
  if (!store[ip]) {
    store[ip] = { count: 1, timestamp: now };
  } else if (now - store[ip].timestamp > windowMs) {
    store[ip] = { count: 1, timestamp: now };
  } else {
    store[ip].count++;
  }

  return {
    success: store[ip].count <= limit
  };
} 