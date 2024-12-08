# MemOS AI Framework

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Node.js Version](https://img.shields.io/badge/node-18%2B-green)](https://nodejs.org/)

## 🚀 Overview

MemOS AI is a groundbreaking framework that transforms static memes into interactive digital entities. By leveraging advanced AI technologies, MemOS creates an operating system-like environment where memes become dynamic, interactive, and context-aware digital beings.

## 🌟 Key Features

- **Meme Consciousness Engine**: Transform static memes into self-aware digital entities
- **Interactive Meme Framework**: Enable dynamic interactions between users and meme entities
- **Context-Aware Processing**: Understand and adapt to user context and preferences
- **Emotional Intelligence**: Process and respond to emotional cues in communications
- **Multi-Modal Integration**: Support for various media types (images, text, audio, video)
- **Extensible Architecture**: Plugin system for custom features and integrations
- **Modern Web Interface**: Beautiful and intuitive user interface for interacting with the system


### 📷 Frontend Setup

Create a .env file with your OPENAI_API_KEY in the ui folder (we use OPENAI gpt-4o-mini model for the frontend example)

```bash
# Clone the repository
git clone https://github.com/nostradamus23/memos-Framework.git
cd memos-Framwork

# Install Node.js dependencies and start the development server
npm install
npm run dev
```

The web interface will be available at `http://localhost:3000` by default. When you open it in your browser, you'll see the MemOS Terminal Interface - an interactive chat-like interface where you can interact with meme entities and experience the AI-powered meme consciousness system. 

## 🚦 Quick Framework Start

```bash
# Clone the repository
git clone https://github.com/nostradamus23/memos-Framework.git
cd memos-Framwork

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

```python
from memos.core import MemOSEngine
from memos.entities import MemeEntity

# Initialize the MemOS engine
engine = MemOSEngine()

# Create a new meme entity
meme = MemeEntity.from_image("path/to/meme.jpg")

# Start interaction
engine.activate(meme)
```

## 📚 Documentation

Comprehensive documentation is available in the `/docs` directory:

- [Architecture Overview](docs/architecture.md)
- [Core Concepts](docs/core-concepts.md)
- [API Reference](docs/api-reference.md)
- [Development Guide](docs/development.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run all tests with coverage
pytest --cov=memos tests/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Special thanks to all contributors and the AI research community for inspiration and support.

## 📬 Contact

- Project Maintainer: MemosAI
- Email: Memosai@proton.me
- Twitter: [@memOSai_]

---

Made with ❤️ by the MemOS AI Team 