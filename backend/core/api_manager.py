"""
API Manager - مدیریت API های مختلف هوش مصنوعی
"""
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import requests

@dataclass
class APIConfig:
    name: str
    api_key: str
    base_url: str
    model: str
    is_free: bool = False
    max_tokens: int = 1000
    temperature: float = 0.7

class APIManager:
    def __init__(self):
        self.config_file = "data/api_configs.json"
        self.apis = self.load_configs()
        
        # Free APIs که پیش‌فرض اضافه میشن
        self.add_free_apis()
    
    def load_configs(self) -> Dict[str, APIConfig]:
        """بارگذاری تنظیمات API ها"""
        if not os.path.exists(self.config_file):
            return {}
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {name: APIConfig(**config) for name, config in data.items()}
        except:
            return {}
    
    def save_configs(self):
        """ذخیره تنظیمات"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            data = {name: asdict(config) for name, config in self.apis.items()}
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def add_api(self, name: str, api_key: str, base_url: str, model: str, 
                is_free: bool = False, max_tokens: int = 1000, temperature: float = 0.7):
        """اضافه کردن API جدید"""
        config = APIConfig(
            name=name,
            api_key=api_key,
            base_url=base_url,
            model=model,
            is_free=is_free,
            max_tokens=max_tokens,
            temperature=temperature
        )
        self.apis[name] = config
        self.save_configs()
        return f"✅ API {name} اضافه شد"
    
    def remove_api(self, name: str):
        """حذف API"""
        if name in self.apis:
            del self.apis[name]
            self.save_configs()
            return f"🗑️ API {name} حذف شد"
        return f"❌ API {name} پیدا نشد"
    
    def list_apis(self) -> List[Dict]:
        """لیست API ها"""
        result = []
        for name, config in self.apis.items():
            status = "🟢 فعال" if self.test_api(name) else "🔴 غیرفعال"
            free_status = "🆓 رایگان" if config.is_free else "💰 پولی"
            result.append({
                "name": name,
                "model": config.model,
                "status": status,
                "type": free_status,
                "base_url": config.base_url
            })
        return result
    
    def test_api(self, name: str) -> bool:
        """تست API"""
        if name not in self.apis:
            return False
        
        config = self.apis[name]
        try:
            # تست ساده برای بررسی دسترسی
            headers = {"Authorization": f"Bearer {config.api_key}"}
            response = requests.get(f"{config.base_url}/models", headers=headers, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def chat_with_api(self, api_name: str, messages: List[Dict]) -> str:
        """چت با API مشخص"""
        if api_name not in self.apis:
            return f"❌ API {api_name} پیدا نشد"
        
        config = self.apis[api_name]
        
        try:
            # تنظیمات خاص برای API های مختلف
            if api_name == 'groq':
                headers = {
                    "Authorization": f"Bearer {config.api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": config.model,
                    "messages": messages,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature
                }
                
                response = requests.post(
                    f"{config.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
            elif api_name == 'huggingface':
                headers = {
                    "Authorization": f"Bearer {config.api_key}",
                    "Content-Type": "application/json"
                }
                
                # HuggingFace فرمت متفاوت داره
                user_message = messages[-1]['content'] if messages else ""
                data = {
                    "inputs": user_message,
                    "parameters": {
                        "max_new_tokens": config.max_tokens,
                        "temperature": config.temperature,
                        "return_full_text": False
                    }
                }
                
                # استفاده از URL مدل مستقیم
                model_url = f"https://api-inference.huggingface.co/models/{config.model}"
                response = requests.post(
                    model_url,
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
            else:
                # فرمت استاندارد OpenAI
                headers = {
                    "Authorization": f"Bearer {config.api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": config.model,
                    "messages": messages,
                    "max_tokens": config.max_tokens,
                    "temperature": config.temperature
                }
                
                response = requests.post(
                    f"{config.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                
                # پردازش پاسخ بر اساس نوع API
                if api_name == 'huggingface':
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get('generated_text', 'پاسخ دریافت نشد')
                    else:
                        return str(result)
                else:
                    # فرمت OpenAI
                    return result["choices"][0]["message"]["content"]
            else:
                return f"❌ خطا: {response.status_code} - {response.text[:200]}"
                
        except Exception as e:
            return f"❌ خطا در ارتباط: {str(e)}"
    
    def add_free_apis(self):
        """اضافه کردن API های رایگان"""
        free_apis = [
            {
                "name": "huggingface_hub",
                "api_key": "hf_your_token_here",
                "base_url": "https://api-inference.huggingface.co",
                "model": "gpt2",
                "is_free": True
            },
            {
                "name": "ollama_local",
                "api_key": "local",
                "base_url": "http://localhost:11434",
                "model": "qwen2:7b",
                "is_free": True
            },
            {
                "name": "groq_example",
                "api_key": "gsk_your_key_here",
                "base_url": "https://api.groq.com/openai/v1",
                "model": "llama3-8b-8192",
                "is_free": True
            }
        ]
        
        for api in free_apis:
            if api["name"] not in self.apis:
                self.add_api(**api)

# Global instance
api_manager = APIManager()
