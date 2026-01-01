"""
🤖 AI Providers - مدیریت API های مختلف هوش مصنوعی
"""

import requests
import json
from abc import ABC, abstractmethod

class AIProvider(ABC):
    """کلاس پایه برای همه AI providers"""
    
    def __init__(self, name, api_key=None):
        self.name = name
        self.api_key = api_key
        self.enabled = True
    
    @abstractmethod
    def generate_response(self, prompt):
        """تولید پاسخ از AI"""
        pass
    
    def is_available(self):
        """بررسی در دسترس بودن API"""
        return self.enabled

class OllamaProvider(AIProvider):
    """Ollama محلی"""
    
    def __init__(self):
        super().__init__("Ollama")
        self.base_url = "http://localhost:11434"
    
    def generate_response(self, prompt):
        try:
            response = requests.post(f"{self.base_url}/api/generate", 
                json={"model": "qwen2:7b", "prompt": prompt, "stream": False})
            return response.json().get("response", "")
        except:
            return None

class OpenAIProvider(AIProvider):
    """OpenAI GPT"""
    
    def __init__(self, api_key):
        super().__init__("OpenAI", api_key)
        self.base_url = "https://api.openai.com/v1"
    
    def generate_response(self, prompt):
        if not self.api_key:
            return None
        try:
            response = requests.post(f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]})
            return response.json()["choices"][0]["message"]["content"]
        except:
            return None

class ClaudeProvider(AIProvider):
    """Anthropic Claude"""
    
    def __init__(self, api_key):
        super().__init__("Claude", api_key)
        self.base_url = "https://api.anthropic.com/v1"
    
    def generate_response(self, prompt):
        if not self.api_key:
            return None
        try:
            response = requests.post(f"{self.base_url}/messages",
                headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01"},
                json={"model": "claude-3-sonnet-20240229", "max_tokens": 1000, 
                      "messages": [{"role": "user", "content": prompt}]})
            return response.json()["content"][0]["text"]
        except:
            return None

class GeminiProvider(AIProvider):
    """Google Gemini"""
    
    def __init__(self, api_key):
        super().__init__("Gemini", api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    def generate_response(self, prompt):
        if not self.api_key:
            return None
        try:
            response = requests.post(f"{self.base_url}/models/gemini-pro:generateContent",
                params={"key": self.api_key},
                json={"contents": [{"parts": [{"text": prompt}]}]})
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return None

class CustomProvider(AIProvider):
    """Custom AI Provider - برای API های دلخواه"""
    
    def __init__(self, name, api_key, base_url, headers=None, payload_template=None):
        super().__init__(name, api_key)
        self.base_url = base_url
        self.headers = headers or {}
        self.payload_template = payload_template or {}
    
    def generate_response(self, prompt):
        if not self.api_key or not self.base_url:
            return None
        try:
            headers = self.headers.copy()
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = self.payload_template.copy()
            payload["prompt"] = prompt
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            return response.json().get("response", response.text)
        except:
            return None

class AIProviderManager:
    """مدیر همه AI providers"""
    
    def __init__(self):
        self.providers = {}
        self.config_file = "backend/config/ai_providers.json"
        self.load_config()
    
    def load_config(self):
        """بارگذاری تنظیمات از فایل"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # اضافه کردن providers بر اساس config
            if config.get("ollama", {}).get("enabled", True):
                self.providers["ollama"] = OllamaProvider()
            
            if config.get("openai", {}).get("enabled", False):
                api_key = config["openai"].get("api_key")
                if api_key:
                    self.providers["openai"] = OpenAIProvider(api_key)
            
            if config.get("claude", {}).get("enabled", False):
                api_key = config["claude"].get("api_key")
                if api_key:
                    self.providers["claude"] = ClaudeProvider(api_key)
            
            if config.get("gemini", {}).get("enabled", False):
                api_key = config["gemini"].get("api_key")
                if api_key:
                    self.providers["gemini"] = GeminiProvider(api_key)
                    
        except FileNotFoundError:
            # فقط Ollama محلی
            self.providers["ollama"] = OllamaProvider()
    
    def get_available_providers(self):
        """لیست providers موجود"""
        return [p for p in self.providers.values() if p.is_available()]
    
    def get_provider(self, name):
        """دریافت provider خاص"""
        return self.providers.get(name.lower())
    
    def add_provider(self, provider):
        """اضافه کردن provider جدید"""
        self.providers[provider.name.lower()] = provider
    
    def get_responses(self, prompt):
        """دریافت پاسخ از همه providers"""
        responses = {}
        for name, provider in self.providers.items():
            if provider.is_available():
                response = provider.generate_response(prompt)
                if response:
                    responses[name] = response
        return responses

# Instance سراسری
ai_manager = AIProviderManager()
