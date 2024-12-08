import { OpenAI } from 'openai';
import { NextResponse } from 'next/server';
import { sessionManager } from '@/app/services/sessionService';

const MODEL = "gpt-4o-mini";
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

export async function POST(req: Request) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File;
    const memeName = formData.get('memeName') as string;
    const sessionId = formData.get('sessionId') as string;

    if (!sessionId) {
      return NextResponse.json(
        { error: 'Se requiere sessionId' },
        { status: 400 }
      );
    }

    const session = sessionManager.getSession(sessionId);
    if (!session) {
      return NextResponse.json(
        { error: 'Sesión inválida' },
        { status: 401 }
      );
    }

    if (!file || !memeName) {
      return NextResponse.json(
        { error: 'Se requiere archivo y nombre del meme' },
        { status: 400 }
      );
    }

    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    const base64Image = buffer.toString('base64');
    const dataUrl = `data:${file.type};base64,${base64Image}`;

    const response = await openai.chat.completions.create({
      model: MODEL,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "text",
              text: `Analyze this crypto meme character named "${memeName}" and provide a JSON response with the following structure:
              {
                "name": "character name",
                "appearanceTraits": ["trait1", "trait2", "trait3", etc... (add as many as you think is ok)],
                "possibleJokes": ["joke1", "joke2", "joke3", etc... (add as many as you think is ok)],
                "personality": "brief personality description"
              }
              
              Focus on unique visual elements and crypto-related characteristics. ONLY answer with the json`
            },
            {
              type: "image_url",
              image_url: {
                url: dataUrl
              }
            }
          ],
        },
      ],
      max_tokens: 500,
      response_format: { type: "json_object" }
    });

    const analysisContent = response.choices[0]?.message?.content;
    if (!analysisContent) {
      throw new Error('No se recibió respuesta válida de OpenAI');
    }

    const analysis = JSON.parse(analysisContent);
    console.log('El analisis fue ', analysis)

    sessionManager.updateSession(sessionId, { analysis });
    return NextResponse.json({ success: true, analysis });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}