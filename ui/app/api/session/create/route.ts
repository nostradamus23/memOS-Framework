import { sessionManager } from '@/app/services/sessionService';
import { NextResponse } from 'next/server';

export async function GET() {
  const sessionId = sessionManager.createSession();
  return NextResponse.json({ sessionId });
} 