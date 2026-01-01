#!/bin/bash

echo "🦊 Fox AI Desktop App Builder"
echo "=============================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "📦 Installing dependencies..."
cd electron
npm install

echo "🚀 Starting Fox AI Desktop App..."
echo "Make sure the web server is running on http://localhost:8080"
echo ""

# Check if web server is running
if curl -s http://localhost:8080 > /dev/null; then
    echo "✅ Web server is running"
    echo "🖥️  Starting Electron app..."
    npm start
else
    echo "❌ Web server is not running on http://localhost:8080"
    echo "Please start the web server first:"
    echo "cd /home/hamed/personal-ai"
    echo "source venv/bin/activate"
    echo "python start_web.py"
    exit 1
fi
