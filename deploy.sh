#!/bin/bash
# Production deployment script for Fox AI

echo "🦊 Fox AI Production Deployment"
echo "================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Don't run as root for security"
    exit 1
fi

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+
echo "🐍 Installing Python..."
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install nodejs -y

# Install system dependencies
echo "🔧 Installing system dependencies..."
sudo apt install git curl wget build-essential -y

# Clone Fox AI
echo "📥 Cloning Fox AI..."
if [ ! -d "Fox_Ai" ]; then
    git clone https://github.com/theistthirteenmm/Fox_Ai.git
fi

cd Fox_Ai

# Setup Python environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Setup Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd electron/
npm install
cd ..

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/fox-ai.service > /dev/null <<EOF
[Unit]
Description=Fox AI Web Server
After=network.target

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

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable fox-ai
sudo systemctl start fox-ai

# Setup nginx (optional)
echo "🌐 Setting up Nginx reverse proxy..."
sudo apt install nginx -y

sudo tee /etc/nginx/sites-available/fox-ai > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;  # Change this
    
    location / {
        proxy_pass http://localhost:7070;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    location /ws {
        proxy_pass http://localhost:7070;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/fox-ai /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# Setup firewall
echo "🔥 Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

echo "✅ Fox AI deployed successfully!"
echo "🌐 Access via: http://your-server-ip"
echo "📊 Check status: sudo systemctl status fox-ai"
echo "📝 View logs: sudo journalctl -u fox-ai -f"
