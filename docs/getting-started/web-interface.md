# Web Interface Guide

The MemOS AI Web Interface provides a modern, intuitive way to interact with meme entities through a terminal-like chat interface.

## Getting Started

1. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/nostradamus23/memos-Framework.git
   cd memos-ai

   # Install dependencies
   npm install
   ```

2. **Starting the Interface**
   ```bash
   npm run dev
   ```
   The interface will be available at `http://localhost:3000`

## Features

- **Interactive Terminal**: A chat-like interface that mimics a terminal environment
- **Real-time Responses**: Instant interaction with meme entities
- **Context-Aware**: The interface maintains context throughout your conversation
- **Multi-Modal Support**: Handle various media types including images, text, and more
- **Modern Design**: Clean, intuitive UI with dark mode support

## Usage

1. **Starting a Conversation**
   - Open your browser and navigate to `http://localhost:3000`
   - The terminal interface will be ready for your input

2. **Basic Commands**
   - Type your messages naturally to interact with meme entities
   - Use special commands (documented in the interface) for advanced features

3. **Working with Media**
   - Drag and drop images directly into the interface
   - Use file upload buttons for media input
   - Copy-paste images directly into the chat

## Configuration

The web interface can be configured through environment variables:
- Create a `.env` file in the root directory
- Copy the contents from `.env.example`
- Update the values according to your needs

## Troubleshooting

Common issues and solutions:

1. **Port Already in Use**
   - The default port 3000 might be occupied
   - Change the port in your environment variables
   - Or stop the process using port 3000

2. **Dependencies Issues**
   - Run `npm install` again
   - Clear npm cache: `npm cache clean --force`
   - Delete `node_modules` and reinstall

## Next Steps

- Explore the [API Documentation](../api/rest.md) to understand the backend integration
- Check out [Advanced Features](../features/interaction.md) for more capabilities
- Visit our [Examples](../examples/basic/index.md) for common use cases 