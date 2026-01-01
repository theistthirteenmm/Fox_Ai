#!/bin/bash

# Personal AI Assistant - Quick Setup Script

echo "🤖 Personal AI Assistant - Quick Setup"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "⚙️ Creating environment file..."
    cp .env.example .env
    echo "✅ Created .env file. You can modify it if needed."
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/{database,logs,models}

# Start Ollama container
echo "🐳 Starting Ollama container..."
docker run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama ollama/ollama

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Download Persian model
echo "📥 Downloading Persian AI model (this may take a few minutes)..."
docker exec ollama ollama pull qwen2:7b

# Run tests
echo "🧪 Running tests..."
./test.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 Quick start:"
echo "  CLI: python cli/main.py"
echo "  Web: python start_web.py"
echo ""
echo "📚 For more information, see README.md"
