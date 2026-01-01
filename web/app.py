"""
FastAPI Web Application with Internet Access
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
import json
import asyncio
from backend.core.llm_engine import LLMEngine
from backend.core.conversation import ConversationManager
from backend.core.internet import InternetAccess
from backend.core.ai_connector import AIConnector
from backend.config.settings import settings

app = FastAPI(title="Personal AI Assistant")

# Static files and templates
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Initialize components
llm = LLMEngine(
    model_name=settings.default_model,
    host=settings.ollama_host
)
conversation_manager = ConversationManager()
internet = InternetAccess()
ai_connector = AIConnector()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Start new conversation session
    session_id = conversation_manager.start_new_session()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            
            if not user_message.strip():
                continue
            
            # Add user message to conversation
            conversation_manager.add_message("user", user_message)
            
            # Send typing indicator
            await websocket.send_text(json.dumps({
                "type": "typing",
                "message": "در حال تایپ..."
            }))
            
            try:
                # Check if user is asking for web search
                if any(keyword in user_message.lower() for keyword in ['جستجو کن', 'search', 'اینترنت', 'آخرین اخبار', 'خبر', 'وضعیت آب و هوا']):
                    # Add web search results to context
                    web_results = internet.search_web(user_message, 3)
                    if web_results:
                        web_context = "نتایج جستجو در اینترنت:\n"
                        for result in web_results:
                            web_context += f"- {result['title']}: {result['content'][:200]}...\n"
                        
                        conversation_manager.add_message("system", web_context)
                
                # Get enhanced context with memories
                context_messages = conversation_manager.get_enhanced_context()
                
                # Get AI response
                response = llm.chat(context_messages)
                
                # Add AI response to conversation
                conversation_manager.add_message("assistant", response)
                
                # Send response to client
                await websocket.send_text(json.dumps({
                    "type": "message",
                    "message": response,
                    "sender": "assistant"
                }))
                
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"خطا: {str(e)}"
                }))
                
    except WebSocketDisconnect:
        pass

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ollama_available": llm.is_available(),
        "models": llm.list_models(),
        "external_models": ai_connector.get_available_models()
    }

@app.get("/api/conversations")
async def get_conversations():
    """Get list of recent conversations"""
    try:
        conversations = conversation_manager.get_conversations_list()
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/memory")
async def get_memory():
    """Get stored memories"""
    try:
        memories = conversation_manager.memory.get_memories()
        return {"memories": memories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_conversations(q: str):
    """Search in conversation history"""
    try:
        results = conversation_manager.search_history(q)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/web-search")
async def web_search(q: str, limit: int = 5):
    """Search the web"""
    try:
        results = internet.search_web(q, limit)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/news")
async def get_news(topic: str = "Iran", limit: int = 5):
    """Get latest news"""
    try:
        news = internet.get_news(topic, limit)
        return {"news": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather")
async def get_weather(city: str = "Tehran"):
    """Get weather information"""
    try:
        weather = internet.get_weather(city)
        return {"weather": weather}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/webpage")
async def get_webpage(url: str):
    """Get webpage content"""
    try:
        content = internet.get_webpage_content(url)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
