#!/bin/bash
# Fox AI Complete Setup with LLM Models

echo "🦊 Fox AI Complete Installation"
echo "==============================="

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install python3 python3-pip python3-venv nodejs npm curl -y

# Setup Python environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Ollama
echo "🤖 Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh

# Wait for Ollama to start
echo "⏳ Starting Ollama service..."
sudo systemctl start ollama
sleep 5

# Download recommended model
echo "📥 Downloading AI model (this may take a while)..."
echo "Choose model size:"
echo "1) llama3.2:3b (2GB) - Fast, good for basic tasks"
echo "2) qwen2:7b (4GB) - Better quality, more capable"
echo "3) llama3.2:8b (5GB) - High quality, slower"

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        ollama pull llama3.2:3b
        MODEL="llama3.2:3b"
        ;;
    2)
        ollama pull qwen2:7b
        MODEL="qwen2:7b"
        ;;
    3)
        ollama pull llama3.2:8b
        MODEL="llama3.2:8b"
        ;;
    *)
        echo "Invalid choice, using default llama3.2:3b"
        ollama pull llama3.2:3b
        MODEL="llama3.2:3b"
        ;;
esac

# Update Fox AI config
echo "⚙️ Configuring Fox AI..."
sed -i "s/qwen2:7b/$MODEL/g" backend/config/settings.py

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd electron/
npm install
cd ..

# Create systemd service
echo "🔧 Creating system service..."
sudo tee /etc/systemd/system/fox-ai.service > /dev/null <<EOF
[Unit]
Description=Fox AI Web Server
After=network.target ollama.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
Environment=WEB_PORT=7070
ExecStart=$(pwd)/venv/bin/python start_web.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable fox-ai
sudo systemctl start fox-ai

echo "✅ Fox AI installation complete!"
echo "🌐 Access: http://localhost:7070"
echo "🖥️ Desktop: ./start_fox_desktop.sh"
echo "📊 Status: sudo systemctl status fox-ai"
echo "📝 Logs: sudo journalctl -u fox-ai -f"
echo ""
echo "🤖 Model installed: $MODEL"
echo "💾 Model size: $(ollama list | grep $MODEL | awk '{print $2}')"
