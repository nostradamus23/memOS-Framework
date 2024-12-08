import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { rateLimit } from "@/app/services/rateLimit"

export async function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/api/')) {
    const ip = request.ip ?? '127.0.0.1';
    const { success } = await rateLimit(ip);
    
    if (!success) {
      return NextResponse.json(
        { error: 'Demasiadas solicitudes' },
        { status: 429 }
      );
    }
  }
  
  return NextResponse.next();
} 