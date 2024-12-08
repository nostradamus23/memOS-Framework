import { ChatCompletionMessageParam } from 'openai/resources/chat/completions';
import { OpenAiService } from '../services/openAiService';

export class CharacterChat {
  private descripcionPersonaje: string = '';
  private memeName: string = '';
  private openAiService: OpenAiService;

  constructor(apiKey: string) {
    this.openAiService = new OpenAiService(apiKey);
  }

  async inicializarConImagen(imageName: string, memeName: string): Promise<string> {
    try {
      this.memeName = memeName;
      this.descripcionPersonaje = await this.openAiService.analizarImagen(imageName, memeName);
      return this.descripcionPersonaje;
    } catch (error) {
      console.error('Error initializing chat:', error);
      throw error;
    }
  }

  async generateSingleMessage(isHacky: boolean, topic: string, previousMessages: string[]): Promise<string> {
    if (!this.descripcionPersonaje) {
      throw new Error('Must initialize chat with an image first');
    }

    try {
      return await this.openAiService.generateSingleMessage(
        isHacky,
        this.descripcionPersonaje,
        this.memeName,
        topic,
        previousMessages
      );
    } catch (error) {
      console.error('Error generating message:', error);
      throw error;
    }
  }
}