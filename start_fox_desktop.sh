#!/bin/bash

echo "🦊 Starting Fox AI Desktop Application"
echo "====================================="

# Check if web server is running
if ! curl -s http://localhost:8080 > /dev/null; then
    echo "🚀 Starting Fox AI web server..."
    cd /home/hamed/personal-ai
    source venv/bin/activate
    nohup python start_web.py > web.log 2>&1 &
    
    echo "⏳ Waiting for server to start..."
    sleep 5
    
    if curl -s http://localhost:8080 > /dev/null; then
        echo "✅ Web server started successfully"
    else
        echo "❌ Failed to start web server"
        exit 1
    fi
else
    echo "✅ Web server is already running"
fi

# Start Electron app
echo "🖥️  Launching Fox AI Desktop App..."
cd /home/hamed/personal-ai/electron

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the app
npm start
