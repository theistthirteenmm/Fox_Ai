#!/bin/bash

# Fox Remote CLI Access Script

SERVER_IP="localhost"  # تغییر بده به IP سرور
SERVER_PORT="8080"

echo "🦊 Fox Remote CLI Access"
echo "======================="

# Check if server is reachable
if ! curl -s "http://$SERVER_IP:$SERVER_PORT/health" > /dev/null; then
    echo "❌ Cannot connect to Fox server at $SERVER_IP:$SERVER_PORT"
    echo "Make sure the server is running: python start_web.py"
    exit 1
fi

echo "✅ Connected to Fox server"
echo "🌐 Web Interface: http://$SERVER_IP:$SERVER_PORT"
echo "🖥️ Web Terminal: http://$SERVER_IP:$SERVER_PORT/terminal"
echo ""

# Option 1: SSH (if available)
if command -v ssh &> /dev/null; then
    echo "Option 1: SSH Access"
    echo "ssh hamed@$SERVER_IP"
    echo "cd /home/hamed/personal-ai && source venv/bin/activate && python cli/main.py"
    echo ""
fi

# Option 2: Web Terminal
echo "Option 2: Web Terminal (Recommended)"
echo "Open: http://$SERVER_IP:$SERVER_PORT/terminal"
echo ""

# Option 3: API Access
echo "Option 3: API Testing"
echo "curl 'http://$SERVER_IP:$SERVER_PORT/api/web-search?q=test'"
echo ""

read -p "Press Enter to open web terminal in browser (if available)..."

# Try to open browser
if command -v xdg-open &> /dev/null; then
    xdg-open "http://$SERVER_IP:$SERVER_PORT/terminal"
elif command -v open &> /dev/null; then
    open "http://$SERVER_IP:$SERVER_PORT/terminal"
else
    echo "Please open: http://$SERVER_IP:$SERVER_PORT/terminal"
fi
