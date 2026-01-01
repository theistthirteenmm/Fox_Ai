#!/bin/bash
# Test script for Personal AI

echo "🚀 Testing Personal AI Assistant..."

cd /home/hamed/personal-ai
source venv/bin/activate

echo "✅ Testing CLI functionality..."
echo -e "/models\n/quit" | timeout 5 python cli/main.py > /tmp/test_cli.txt 2>&1

if grep -q "qwen2:7b" /tmp/test_cli.txt; then
    echo "✅ CLI works"
else
    echo "❌ CLI failed"
fi

echo "✅ Testing Memory System..."
timeout 5 python -c "
from backend.core.memory import MemoryManager
from backend.core.conversation import ConversationManager

# Test memory system
conv = ConversationManager()
session_id = conv.start_new_session()
conv.add_message('user', 'تست حافظه')
conv.add_message('assistant', 'حافظه کار می‌کند')

memories = conv.memory.get_memories()
conversations = conv.get_conversations_list()

if len(conversations) > 0:
    print('✅ Memory system works')
else:
    print('❌ Memory system failed')
" 2>/dev/null

echo "✅ Testing Internet Access..."
timeout 10 python -c "
from backend.core.internet import InternetAccess

internet = InternetAccess()
results = internet.search_web('test', 1)
weather = internet.get_weather('Tehran')

if len(results) > 0 and weather['city'] == 'Tehran':
    print('✅ Internet access works')
else:
    print('❌ Internet access failed')
" 2>/dev/null

echo "✅ Testing Web API..."
timeout 5 python -c "
import requests
import time
from web.app import app
import uvicorn
import threading

def start_server():
    uvicorn.run(app, host='127.0.0.1', port=8081, log_level='error')

# Start server in background
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(2)

try:
    response = requests.get('http://127.0.0.1:8081/health', timeout=3)
    if response.status_code == 200:
        print('✅ Web API works')
    else:
        print('❌ Web API failed')
except:
    print('❌ Web API connection failed')
" 2>/dev/null

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Available interfaces:"
echo "🖥️  CLI: python cli/main.py"
echo "🌐 Web: python start_web.py (then open http://localhost:8080)"
echo ""
echo "🧠 Memory Features:"
echo "📚 /history - View conversation history"
echo "🔍 /search <text> - Search conversations"
echo "💾 /memory - View stored memories"
echo ""
echo "🌐 Internet Features:"
echo "🔍 /web <query> - Web search"
echo "📰 /news [topic] - Latest news"
echo "🌤️ /weather [city] - Weather info"
echo "📄 /url <address> - Get webpage content"
echo "🤖 /compare <question> - Compare AI responses"
echo ""
echo "🔧 Management:"
echo "📊 Health: curl http://localhost:8080/health"
echo "🔍 Web Search API: curl 'http://localhost:8080/api/web-search?q=test'"
echo "📰 News API: curl 'http://localhost:8080/api/news?topic=Iran'"
echo "🐳 Ollama: docker ps | grep ollama"
