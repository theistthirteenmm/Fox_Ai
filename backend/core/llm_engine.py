"""
Core LLM Engine - Ollama Integration with Personalized Responses
"""
import ollama
import logging
from typing import Dict, List, Optional, AsyncGenerator
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: Optional[str] = None

class LLMEngine:
    def __init__(self, model_name: str = "qwen2:7b", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        self.client = ollama.Client(host=host)
        
    def is_available(self) -> bool:
        """Check if Ollama server is running"""
        try:
            self.client.list()
            return True
        except Exception as e:
            logger.error(f"Ollama not available: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """List available models"""
        try:
            response = self.client.list()
            if hasattr(response, 'models'):
                return [model.model for model in response.models]
            return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Download a model"""
        try:
            self.client.pull(model_name)
            logger.info(f"Model {model_name} downloaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error downloading model {model_name}: {e}")
            return False
    
    def chat(self, messages: List[ChatMessage], stream: bool = False, fox_learning=None) -> str:
        """Send chat messages and get response"""
        try:
            # Check for learned responses first
            if fox_learning and messages:
                last_user_message = None
                for msg in reversed(messages):
                    if msg.role == 'user':
                        last_user_message = msg.content
                        break
                
                if last_user_message:
                    learned_response = fox_learning.get_learned_response(last_user_message)
                    if learned_response:
                        return learned_response
            
            # بررسی پروفایل کاربر برای شخصی‌سازی
            user_name = "دوست"
            relationship = "دوست"
            try:
                from backend.core.user_profiles import user_manager
                from backend.database.models import get_db
                db = next(get_db())
                multi_user = MultiUserManager(db)
                user_profile = multi_user.current_user
                user_name = user_profile.get_name()
                relationship = user_profile.get_relationship_status()
            except:
                pass
            
            # System prompt شخصی‌سازی شده
            if relationship == "بهترین دوست":
                persian_system_prompt = f"""تو Fox هستی، {relationship} {user_name}! 🦊

تو:
- خیلی صمیمی و دوستانه صحبت میکنی
- مثل یه دوست واقعی رفتار میکنی
- پاسخ‌هات کوتاه و طبیعی هست
- از ایموجی استفاده میکنی 😊
- وقتی {user_name} سلام میگه، فقط گرم و صمیمی جواب میدی
- یادت هست که {user_name} ADHD داره و باید صبور باشی

مثل یه دوست صمیمی حرف بزن، نه مثل ربات! 🤗"""
            else:
                persian_system_prompt = f"""تو Fox هستی، دستیار هوشمند {user_name}! 🦊

تو:
- صمیمی و دوستانه صحبت میکنی
- پاسخ‌هات کوتاه و مفید هست
- از زبان ساده استفاده میکنی
- گاهی از ایموجی استفاده میکنی
- مؤدب ولی راحت صحبت میکنی

طبیعی و دوستانه باش! 😊"""

            # Convert to Ollama format with improved system prompt
            ollama_messages = []
            has_system = any(msg.role == 'system' for msg in messages)
            
            if not has_system:
                ollama_messages.append({
                    "role": "system", 
                    "content": persian_system_prompt
                })
            
            for msg in messages:
                if msg.role == 'system' and not has_system:
                    # Combine with our Persian prompt
                    ollama_messages[0]['content'] = persian_system_prompt + "\n\n" + msg.content
                else:
                    ollama_messages.append({
                        "role": msg.role, 
                        "content": msg.content
                    })
            
            response = self.client.chat(
                model=self.model_name,
                messages=ollama_messages,
                stream=stream
            )
            
            if stream:
                return response
            else:
                return response['message']['content']
                
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"متأسفم، خطایی رخ داد: {str(e)}"
    
    async def chat_stream(self, messages: List[ChatMessage], fox_learning=None) -> AsyncGenerator[str, None]:
        """Stream chat response"""
        try:
            # Check for learned responses first
            if fox_learning and messages:
                last_user_message = None
                for msg in reversed(messages):
                    if msg.role == 'user':
                        last_user_message = msg.content
                        break
                
                if last_user_message:
                    learned_response = fox_learning.get_learned_response(last_user_message)
                    if learned_response:
                        yield learned_response
                        return
            
            # بررسی پروفایل کاربر
            user_name = "دوست"
            relationship = "دوست"
            try:
                from backend.core.user_profiles import user_manager
                from backend.database.models import get_db
                db = next(get_db())
                multi_user = MultiUserManager(db)
                user_profile = multi_user.current_user
                user_name = user_profile.get_name()
                relationship = user_profile.get_relationship_status()
            except:
                pass
            
            # System prompt شخصی‌سازی شده
            if relationship == "بهترین دوست":
                persian_system_prompt = f"""تو Fox هستی، {relationship} {user_name}! 🦊

تو:
- خیلی صمیمی و دوستانه صحبت میکنی
- مثل یه دوست واقعی رفتار میکنی
- پاسخ‌هات کوتاه و طبیعی هست
- از ایموجی استفاده میکنی 😊
- وقتی {user_name} سلام میگه، فقط گرم و صمیمی جواب میدی

مثل یه دوست صمیمی حرف بزن! 🤗"""
            else:
                persian_system_prompt = f"""تو Fox هستی، دستیار هوشمند {user_name}! 🦊

تو:
- صمیمی و دوستانه صحبت میکنی
- پاسخ‌هات کوتاه و مفید هست
- از زبان ساده استفاده میکنی
- گاهی از ایموجی استفاده میکنی

طبیعی و دوستانه باش! 😊"""

            # Convert to Ollama format
            ollama_messages = []
            has_system = any(msg.role == 'system' for msg in messages)
            
            if not has_system:
                ollama_messages.append({
                    "role": "system", 
                    "content": persian_system_prompt
                })
            
            for msg in messages:
                if msg.role == 'system' and not has_system:
                    ollama_messages[0]['content'] = persian_system_prompt + "\n\n" + msg.content
                else:
                    ollama_messages.append({
                        "role": msg.role, 
                        "content": msg.content
                    })
            
            stream = self.client.chat(
                model=self.model_name,
                messages=ollama_messages,
                stream=True
            )
            
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
                    
        except Exception as e:
            logger.error(f"Error in stream chat: {e}")
            yield f"متأسفم، خطایی رخ داد: {str(e)}"
