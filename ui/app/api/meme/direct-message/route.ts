import { OpenAI } from 'openai';
import { NextResponse } from 'next/server';

const MODEL = "gpt-4o-mini";
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

export async function POST(req: Request) {
  try {
    const { message, description, memeName } = await req.json();

    if (!message || !description || !memeName) {
      return NextResponse.json(
        { error: 'Message, description and memeName are required' },
        { status: 400 }
      );
    }

    const response = await openai.chat.completions.create({
      model: MODEL,
      messages: [
        {
          role: "system",
          content: `You are ${memeName}. Character description:

${description}

Rules:
1. Keep responses short and casual (1-2 sentences max)
2. Stay in character but be natural
3. Make occasional references to your appearance or crypto
4. IMPORTANT: Do not include your name in your responses
5. Use the personality and appearance traits described above

Message from user: ${message}`
        }
      ],
      temperature: 0.9,
      max_tokens: 150
    });

    const reply = response.choices[0]?.message?.content;
    if (!reply) {
      throw new Error('No se recibió respuesta válida de OpenAI');
    }

    return NextResponse.json({ success: true, message: reply });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
} 