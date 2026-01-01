#!/bin/bash

echo "🦊 Fox AI - Standalone Desktop App"
echo "=================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python first."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "📦 Setting up Fox AI..."

# Install Python dependencies if needed
if [ ! -d "../venv" ]; then
    echo "🐍 Setting up Python environment..."
    cd ..
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd electron
else
    echo "✅ Python environment ready"
fi

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
else
    echo "✅ Node.js dependencies ready"
fi

echo "🚀 Starting Fox AI Desktop App..."
echo "The app will start its own web server automatically."
echo ""

# Start the Electron app (it will start the web server internally)
npm start
