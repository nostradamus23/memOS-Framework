import * as fs from 'fs';
import * as path from 'path';

const IMAGE_DIR = path.join(__dirname, '../../images');

// Asegurarse de que la carpeta images existe
if (!fs.existsSync(IMAGE_DIR)) {
  fs.mkdirSync(IMAGE_DIR, { recursive: true });
}

export function encodeImage(imageName: string): string {
  const imagePath = path.join(IMAGE_DIR, imageName);
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');
  const mimeType = getMimeType(imagePath);
  return `data:${mimeType};base64,${base64Image}`;
}

function getMimeType(filePath: string): string {
  const extension = filePath.split('.').pop()?.toLowerCase();
  switch (extension) {
    case 'jpg':
    case 'jpeg':
      return 'image/jpeg';
    case 'png':
      return 'image/png';
    case 'gif':
      return 'image/gif';
    default:
      return 'image/jpeg';
  }
}

export function getAvailableImages(): string[] {
  return fs.readdirSync(IMAGE_DIR);
} 