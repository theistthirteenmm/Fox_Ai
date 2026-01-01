"""
AI Connector for External APIs
"""
from typing import List, Dict, Optional
from backend.config.settings import settings

# Optional imports
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class AIConnector:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.gemini_model = None
        
        # Initialize clients if API keys and modules are available
        if OPENAI_AVAILABLE and settings.openai_api_key:
            self.openai_client = openai.OpenAI(api_key=settings.openai_api_key)
        
        if ANTHROPIC_AVAILABLE and settings.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        
        if GEMINI_AVAILABLE and settings.google_api_key:
            genai.configure(api_key=settings.google_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    def get_available_models(self) -> List[str]:
        """Get list of available external AI models"""
        models = []
        
        if self.openai_client:
            models.extend(['gpt-4', 'gpt-3.5-turbo'])
        
        if self.anthropic_client:
            models.extend(['claude-3-sonnet', 'claude-3-haiku'])
        
        if self.gemini_model:
            models.append('gemini-pro')
        
        return models
    
    def chat_with_openai(self, messages: List[Dict], model: str = "gpt-3.5-turbo") -> str:
        """Chat with OpenAI models"""
        if not self.openai_client:
            return "OpenAI API key not configured or module not installed"
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"
    
    def chat_with_claude(self, messages: List[Dict], model: str = "claude-3-haiku-20240307") -> str:
        """Chat with Anthropic Claude"""
        if not self.anthropic_client:
            return "Anthropic API key not configured or module not installed"
        
        try:
            # Convert messages to Claude format
            system_msg = ""
            user_messages = []
            
            for msg in messages:
                if msg['role'] == 'system':
                    system_msg = msg['content']
                else:
                    user_messages.append(msg)
            
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=1000,
                system=system_msg,
                messages=user_messages
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude Error: {str(e)}"
    
    def chat_with_gemini(self, messages: List[Dict]) -> str:
        """Chat with Google Gemini"""
        if not self.gemini_model:
            return "Google API key not configured or module not installed"
        
        try:
            # Convert messages to Gemini format
            prompt = ""
            for msg in messages:
                role = "Human" if msg['role'] == 'user' else "Assistant"
                prompt += f"{role}: {msg['content']}\n"
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"
    
    def compare_responses(self, messages: List[Dict]) -> Dict[str, str]:
        """Get responses from multiple AI models for comparison"""
        responses = {}
        
        if self.openai_client:
            responses['GPT-3.5'] = self.chat_with_openai(messages)
        
        if self.anthropic_client:
            responses['Claude'] = self.chat_with_claude(messages)
        
        if self.gemini_model:
            responses['Gemini'] = self.chat_with_gemini(messages)
        
        return responses
