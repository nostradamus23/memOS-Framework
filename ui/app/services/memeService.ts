interface CharacterAnalysis {
  name: string;
  appearanceTraits: string[];
  possibleJokes: string[];
  personality: string;
}

export class MemeService {
    private descripcionPersonaje: CharacterAnalysis | null = null;
    private descripcionTexto: string = '';
    private memeName: string = '';
    private imageUrl: string = '';
  
    async analizarImagen(formData: FormData): Promise<{ analysis: CharacterAnalysis }> {
      try {
        const response = await fetch('/api/meme/analyze', {
          method: 'POST',
          body: formData
        });
  
        const data = await response.json();
        if (!data.success) {
          throw new Error(data.error);
        }
  
        this.descripcionPersonaje = data.analysis;
        this.descripcionTexto = this.convertToTextDescription(data.analysis);
        this.memeName = data.analysis.name;
  
        const file = formData.get('file') as File;
        this.imageUrl = URL.createObjectURL(file);
  
        return { analysis: data.analysis };
      } catch (error) {
        console.error('Error analyzing image:', error);
        throw error;
      }
    }
  
    private convertToTextDescription(analysis: CharacterAnalysis): string {
      return `Name: ${analysis.name}
      
Physical Appearance:
${analysis.appearanceTraits.map(trait => `- ${trait}`).join('\n')}

Possible Jokes:
${analysis.possibleJokes.map(joke => `- ${joke}`).join('\n')}

Personality: ${analysis.personality}`;
    }
  
    async *generateConversation(topic: string): AsyncGenerator<{
      speaker: string;
      message: string;
      imageUrl?: string;
      isHacky?: boolean;
    }> {
      if (!this.descripcionPersonaje || !this.descripcionTexto) {
        throw new Error('Must analyze image first');
      }
  
      try {
        const response = await fetch('/api/meme/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            topic,
            description: this.descripcionTexto,
            memeName: this.memeName
          })
        });
  
        const reader = response.body?.getReader();
        if (!reader) throw new Error('No response body');
  
        const decoder = new TextDecoder();
        let buffer = '';
  
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
  
          buffer += decoder.decode(value);
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';
  
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(5));
                if (data.message) {
                  const isHackyMessage = data.message.startsWith('Hacky:');
                  yield {
                    speaker: isHackyMessage ? 'Hacky' : this.memeName,
                    message: isHackyMessage ? data.message.slice(6).trim() : data.message.slice(this.memeName.length + 1).trim(),
                    imageUrl: isHackyMessage ? '/images/hacky.jpeg' : this.imageUrl,
                    isHacky: isHackyMessage
                  };
                }
              } catch (e) {
                console.error('Error parsing JSON:', e);
              }
            }
          }
        }
      } catch (error) {
        console.error('Error generating conversation:', error);
        throw error;
      }
    }
  
    async sendDirectMessage(message: string): Promise<string> {
      if (!this.descripcionPersonaje || !this.descripcionTexto) {
        throw new Error('Must analyze image first');
      }
  
      try {
        const response = await fetch('/api/meme/direct-message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message,
            description: this.descripcionTexto,
            memeName: this.memeName
          })
        });
  
        const data = await response.json();
        if (!data.success) {
          throw new Error(data.error);
        }
  
        return data.message;
      } catch (error) {
        console.error('Error sending message:', error);
        throw error;
      }
    }
  
    async sendHackyMessage(message: string): Promise<string> {
      try {
        const response = await fetch('/api/meme/direct-message', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message,
            description: this.HACKY_DESCRIPTION,
            memeName: 'Hacky'
          })
        });
  
        const data = await response.json();
        if (!data.success) {
          throw new Error(data.error);
        }
  
        return data.message;
      } catch (error) {
        console.error('Error sending message to Hacky:', error);
        throw error;
      }
    }
  
    private readonly HACKY_DESCRIPTION = `Name: Hacky
      Physical Appearance:
      - Glowing neon-green matrix-style code running across face
      - Always wearing a black hoodie with crypto symbols
      - Digital glitch effects surrounding their form
      - Holographic keyboard floating in front of them`;
  
    initializeCharacter(analysis: CharacterAnalysis, imageUrl: string): void {
      this.descripcionPersonaje = analysis;
      this.descripcionTexto = this.convertToTextDescription(analysis);
      this.memeName = analysis.name;
      this.imageUrl = imageUrl;
    }
  }