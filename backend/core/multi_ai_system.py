"""
🤖 Multi-AI System - مشورت با چند AI
"""

from backend.core.ai_providers import ai_manager
import json
import os

class MultiAISystem:
    def __init__(self):
        self.enabled = False
        self.config_file = "data/multi_ai_enabled.json"
        self.min_responses = 1  # حداقل تعداد پاسخ برای مقایسه
        self.load_status()
    
    def load_status(self):
        """بارگذاری وضعیت"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.enabled = data.get("enabled", False)
            except:
                self.enabled = False
                
    def save_status(self):
        """ذخیره وضعیت"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump({"enabled": self.enabled}, f)
    
    def enable(self):
        """فعال کردن Multi-AI"""
        self.enabled = True
        self.save_status()
        available = len(ai_manager.get_available_providers())
        return f"✅ Multi-AI فعال شد! {available} AI در دسترس"
    
    def disable(self):
        """غیرفعال کردن Multi-AI"""
        self.enabled = False
        self.save_status()
        return "❌ Multi-AI غیرفعال شد! فقط از Fox محلی استفاده میکنم"
    
    def is_enabled(self):
        """بررسی فعال بودن"""
        return self.enabled
    
    def get_status(self):
        """وضعیت Multi-AI"""
        status = "🟢 فعال" if self.enabled else "🔴 غیرفعال"
        providers = ai_manager.get_available_providers()
        provider_names = [p.name for p in providers]
        return f"🤖 Multi-AI: {status}\n📡 AI های موجود: {', '.join(provider_names)}"
    
    def get_best_response(self, prompt):
        """دریافت بهترین پاسخ از چند AI"""
        if not self.enabled:
            return None
        
        # دریافت پاسخ از همه AI ها
        responses = ai_manager.get_responses(prompt)
        
        if len(responses) < self.min_responses:
            return None
        
        # انتخاب بهترین پاسخ
        best_response = None
        best_score = 0
        
        for provider_name, response in responses.items():
            if response and len(response.strip()) > 10:
                # امتیازدهی ساده
                score = len(response)
                # ترجیح متن فارسی
                persian_chars = sum(1 for c in response if '\u0600' <= c <= '\u06FF')
                score += persian_chars * 2
                
                if score > best_score:
                    best_score = score
                    best_response = f"{response}\n\n💡 *از {provider_name}*"
        
        return best_response

# Instance سراسری
multi_ai_system = MultiAISystem()
