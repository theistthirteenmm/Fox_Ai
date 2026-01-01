#!/usr/bin/env python3
"""
Personal AI Assistant - Web Server Launcher
"""
import uvicorn
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web.app import app
from backend.config.settings import settings

if __name__ == "__main__":
    print("🚀 Starting Personal AI Web Interface...")
    print(f"📍 Server will be available at: http://localhost:{settings.web_port}")
    print("🔗 Open this URL in your browser to start chatting!")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        app,
        host=settings.web_host,
        port=settings.web_port,
        log_level="info"
    )
