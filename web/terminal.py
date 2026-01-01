"""
Web Terminal for Remote CLI Access
"""
from fastapi import WebSocket, WebSocketDisconnect
import subprocess
import asyncio
import json
import os
import sys

class WebTerminal:
    def __init__(self, app):
        self.app = app
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.websocket("/terminal")
        async def terminal_websocket(websocket: WebSocket):
            await websocket.accept()
            
            try:
                # Start CLI process
                process = await asyncio.create_subprocess_exec(
                    sys.executable, "cli/main.py",
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd="/home/hamed/personal-ai"
                )
                
                # Handle input from web
                async def handle_input():
                    try:
                        while True:
                            data = await websocket.receive_text()
                            message = json.loads(data)
                            
                            if message.get("type") == "input":
                                command = message.get("data", "") + "\n"
                                process.stdin.write(command.encode())
                                await process.stdin.drain()
                    except:
                        pass
                
                # Handle output to web
                async def handle_output():
                    try:
                        while True:
                            output = await process.stdout.read(1024)
                            if output:
                                await websocket.send_text(json.dumps({
                                    "type": "output",
                                    "data": output.decode('utf-8', errors='ignore')
                                }))
                            else:
                                break
                    except:
                        pass
                
                # Run both handlers
                await asyncio.gather(
                    handle_input(),
                    handle_output()
                )
                
            except WebSocketDisconnect:
                if process:
                    process.terminate()
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "data": f"Error: {str(e)}"
                }))

# Add to main app
def add_terminal_support(app):
    WebTerminal(app)
