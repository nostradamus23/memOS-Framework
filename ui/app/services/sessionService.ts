import { v4 as uuidv4 } from 'uuid';

interface UserSession {
  id: string;
  lastActive: number;
  memeService?: any;
  analysis?: any;
}

class SessionManager {
  private sessions: Map<string, UserSession>;
  private readonly SESSION_TIMEOUT = 1000 * 60 * 30; // 30 minutos

  constructor() {
    this.sessions = new Map();
    this.startCleanupInterval();
  }

  createSession(): string {
    const sessionId = uuidv4();
    this.sessions.set(sessionId, {
      id: sessionId,
      lastActive: Date.now()
    });
    return sessionId;
  }

  getSession(sessionId: string): UserSession {
    let session = this.sessions.get(sessionId);
    if (!session) {
      // Si la sesión no existe, créala
      session = {
        id: sessionId,
        lastActive: Date.now()
      };
      this.sessions.set(sessionId, session);
    }
    return session;
  }

  updateSession(sessionId: string, data: Partial<UserSession>) {
    const session = this.sessions.get(sessionId);
    if (session) {
      this.sessions.set(sessionId, {
        ...session,
        ...data,
        lastActive: Date.now()
      });
    }
  }

  private startCleanupInterval() {
    setInterval(() => {
      const now = Date.now();
      for (const [sessionId, session] of Array.from(this.sessions)) {
        if (now - session.lastActive > this.SESSION_TIMEOUT) {
          this.sessions.delete(sessionId);
        }
      }
    }, 1000 * 60 * 5); // Limpieza cada 5 minutos
  }
}

export const sessionManager = new SessionManager();