import { CONFIG } from './config/config';
import { CharacterChat } from './models/CharacterChat';
import * as readline from 'readline';
import { getAvailableImages } from './utils/imageUtils';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = (query: string): Promise<string> => {
  return new Promise((resolve) => {
    rl.question(query, resolve);
  });
};

async function main() {
  try {
    const chat = new CharacterChat(CONFIG.OPENAI_API_KEY);
    
    console.log('Welcome to Crypto Meme Chat! 🚀\n');
    const memeName = await question('Enter your crypto meme name: ');
    
    // Mostrar imágenes disponibles
    const images = getAvailableImages();
    console.log('\nAvailable images in /images folder:');
    images.forEach((img, index) => {
      console.log(`${index + 1}. ${img}`);
    });
    
    const imageIndex = parseInt(await question('\nSelect image number: ')) - 1;
    if (imageIndex < 0 || imageIndex >= images.length) {
      throw new Error('Invalid image selection');
    }
    
    const selectedImage = images[imageIndex];
    console.log('\nAnalyzing meme character...');
    const description = await chat.inicializarConImagen(selectedImage, memeName);
    console.log('\nMeme Character Description:', description);

    const topic = await question('\nEnter a topic for the conversation: ');
    console.log('\nGenerating conversation...\n');
    
    const previousMessages: string[] = [];
    
    // Generate 3 exchanges (6 messages total)
    for (let i = 0; i < 3; i++) {
      // Hacky's turn
      console.log("Hacky is thinking...");
      const hackyMessage = await chat.generateSingleMessage(true, topic, previousMessages);
      console.log(`\nHacky: ${hackyMessage}\n`);
      previousMessages.push(`Hacky: ${hackyMessage}`);
      
      await new Promise(resolve => setTimeout(resolve, 1000)); // Pequeña pausa
      
      // Meme character's turn
      console.log(`${memeName} is thinking...`);
      const memeMessage = await chat.generateSingleMessage(false, topic, previousMessages);
      console.log(`\n${memeName}: ${memeMessage}\n`);
      previousMessages.push(`${memeName}: ${memeMessage}`);
      
      await new Promise(resolve => setTimeout(resolve, 1000)); // Pequeña pausa
    }
    
    rl.close();

  } catch (error: any) {
    console.error('Application error:', error.message);
    if (error.cause) {
      console.error('Error cause:', error.cause);
    }
    rl.close();
    process.exit(1);
  }
}

main();