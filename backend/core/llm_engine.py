"""
Core LLM Engine - Ollama Integration
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
    
    def chat(self, messages: List[ChatMessage], stream: bool = False) -> str:
        """Send chat messages and get response"""
        try:
            # Convert to Ollama format
            ollama_messages = [
                {"role": msg.role, "content": msg.content} 
                for msg in messages
            ]
            
            response = self.client.chat(
                model=self.model_name,
                messages=ollama_messages,
                stream=stream
            )
            
            if stream:
                return response  # Return generator for streaming
            else:
                return response['message']['content']
                
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"خطا در ارتباط با مدل: {str(e)}"
    
    async def chat_stream(self, messages: List[ChatMessage]) -> AsyncGenerator[str, None]:
        """Stream chat response"""
        try:
            ollama_messages = [
                {"role": msg.role, "content": msg.content} 
                for msg in messages
            ]
            
            stream = self.client.chat(
                model=self.model_name,
                messages=ollama_messages,
                stream=True
            )
            
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
                    
        except Exception as e:
            logger.error(f"Stream chat error: {e}")
            yield f"خطا در ارتباط: {str(e)}"
