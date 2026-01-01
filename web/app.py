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
from web.terminal import add_terminal_support
from backend.core.personality import PersonalitySystem
from backend.core.user_profile import UserProfile
from backend.core.fox_learning import FoxLearningSystem

app = FastAPI(title="Fox - Personal AI Assistant")

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
personality = PersonalitySystem()

# Initialize user profile and learning system
from backend.database.models import get_db
db_session = next(get_db())
user_profile = UserProfile(db_session)
fox_learning = FoxLearningSystem(user_profile)

async def handle_web_command(command: str, websocket: WebSocket) -> str:
    """Handle web chat commands"""
    parts = command.strip().split()
    cmd = parts[0][1:].lower()  # Remove /
    
    if cmd == 'help':
        return """دستورات موجود:
• /help - نمایش راهنما
• /teach <کلید> <پاسخ> - آموزش پاسخ خاص  
• /learn <موضوع> <حقیقت> - آموزش دانش جدید
• /learned - نمایش آمار یادگیری
• /mood - نمایش وضعیت احساسی
• /web <سوال> - جستجو در اینترنت"""
    
    elif cmd == 'teach':
        if len(parts) >= 2:
            rest = command[6:].strip()
            if ' ' in rest:
                trigger, response = rest.split(' ', 1)
                return fox_learning.teach_response(trigger, response)
        return "استفاده: /teach <کلید> <پاسخ>"
    
    elif cmd == 'learn':
        if len(parts) >= 2:
            rest = command[6:].strip()
            if ' ' in rest:
                topic, fact = rest.split(' ', 1)
                return fox_learning.teach_fact(topic, fact)
        return "استفاده: /learn <موضوع> <حقیقت>"
    
    elif cmd == 'learned':
        stats = fox_learning.get_learning_stats()
        return f"""📚 آمار یادگیری Fox:
• پاسخهای آموزش داده شده: {stats['custom_responses']}
• حقایق یادگیری شده: {stats['learned_facts']}
• اطلاعات فرهنگی: {stats['cultural_knowledge']}"""
    
    elif cmd == 'mood':
        return f"وضعیت احساسی Fox: {personality.get_current_mood()}"
    
    elif cmd == 'web':
        if len(parts) > 1:
            query = ' '.join(parts[1:])
            results = internet.search_web(query, 3)
            if results:
                return f"نتایج جستجو برای '{query}':\n" + "\n".join(results[:2])
        return "استفاده: /web <سوال جستجو>"
    
    return f"دستور '{cmd}' شناخته نشد. /help را امتحان کنید."

# Add terminal support
add_terminal_support(app)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/terminal", response_class=HTMLResponse)
async def terminal_page(request: Request):
    return templates.TemplateResponse("terminal.html", {"request": request})

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
            
            # Analyze user input for emotional context
            personality.analyze_user_input(user_message)
            
            # Send typing indicator
            await websocket.send_text(json.dumps({
                "type": "typing",
                "message": "در حال تایپ..."
            }))
            
            try:
                # Check for commands
                if user_message.startswith('/'):
                    command_response = await handle_web_command(user_message, websocket)
                    if command_response:
                        await websocket.send_text(json.dumps({
                            "type": "message",
                            "message": command_response
                        }))
                        continue
            
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
                
                # Add personality prompt
                personality_prompt = personality.get_personality_prompt()
                from backend.core.llm_engine import ChatMessage
                context_messages.insert(0, ChatMessage("system", personality_prompt))
                
                # Get AI response
                response = llm.chat(context_messages, fox_learning=fox_learning)
                
                # Apply personality styling
                styled_response = personality.generate_response_style(response)
                
                # Add AI response to conversation
                conversation_manager.add_message("assistant", styled_response)
                
                # Send response to client
                await websocket.send_text(json.dumps({
                    "type": "message",
                    "message": styled_response,
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

@app.get("/api/mood")
async def get_mood():
    """Get current emotional state"""
    try:
        emotions = personality.get_emotion_state()
        dominant = personality.get_dominant_emotion()
        return {
            "emotions": emotions,
            "dominant": dominant,
            "greeting": personality.get_greeting()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mood")
async def set_mood(emotion: str, value: float):
    """Set specific emotion"""
    try:
        result = personality.set_emotion(emotion, value)
        return {"message": result, "emotions": personality.get_emotion_state()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
