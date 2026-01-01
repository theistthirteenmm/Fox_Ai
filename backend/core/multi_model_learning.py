"""
Multi-Model Learning System - یادگیری از چند مدل
"""
from backend.core.api_manager import api_manager
from backend.core.llm_engine import LLMEngine, ChatMessage
import json
import asyncio

class MultiModelLearning:
    def __init__(self, fox_learning):
        self.fox_learning = fox_learning
        self.llm = LLMEngine()
    
    async def get_multi_model_response(self, question: str, models: list = None):
        """دریافت پاسخ از چند مدل و ترکیب آنها"""
        if not models:
            models = ['ollama', 'groq', 'huggingface']  # مدل‌های پیش‌فرض
        
        responses = {}
        
        # دریافت پاسخ از مدل محلی (Ollama)
        try:
            messages = [ChatMessage("user", question)]
            ollama_response = self.llm.chat(messages)
            responses['ollama'] = ollama_response
        except:
            responses['ollama'] = "خطا در دریافت پاسخ"
        
        # دریافت پاسخ از API های خارجی
        for model in models:
            if model != 'ollama' and model in api_manager.apis:
                try:
                    api_response = api_manager.chat_with_api(model, [{"role": "user", "content": question}])
                    responses[model] = api_response
                except:
                    responses[model] = "خطا در دریافت پاسخ"
        
        return responses
    
    def analyze_responses(self, responses: dict):
        """تحلیل و مقایسه پاسخ‌ها"""
        analysis = {
            "best_response": "",
            "common_points": [],
            "unique_insights": {},
            "quality_scores": {}
        }
        
        # پیدا کردن نکات مشترک
        all_responses = list(responses.values())
        
        # انتخاب بهترین پاسخ (ساده‌ترین: طولانی‌ترین پاسخ معقول)
        best_key = max(responses.keys(), key=lambda k: len(responses[k]) if len(responses[k]) < 1000 else 0)
        analysis["best_response"] = responses[best_key]
        
        # ذخیره برای یادگیری
        analysis["responses"] = responses
        
        return analysis
    
    def learn_from_multi_model(self, question: str, analysis: dict):
        """یادگیری از پاسخ‌های چندگانه"""
        # ذخیره بهترین پاسخ
        self.fox_learning.add_learned_response(question, analysis["best_response"])
        
        # ذخیره تحلیل برای بهبود آینده
        learning_data = {
            "question": question,
            "multi_responses": analysis["responses"],
            "selected_best": analysis["best_response"],
            "timestamp": str(datetime.now())
        }
        
        # ذخیره در فایل یادگیری
        self.save_learning_data(learning_data)
    
    def save_learning_data(self, data):
        """ذخیره داده‌های یادگیری"""
        import os
        learning_file = "data/multi_model_learning.json"
        
        if os.path.exists(learning_file):
            with open(learning_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        
        existing_data.append(data)
        
        # نگه داشتن فقط 100 مورد آخر
        if len(existing_data) > 100:
            existing_data = existing_data[-100:]
        
        os.makedirs(os.path.dirname(learning_file), exist_ok=True)
        with open(learning_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    def get_smart_response(self, question: str):
        """پاسخ هوشمند با استفاده از چند مدل"""
        # ابتدا چک کن آیا قبلاً یاد گرفته
        learned = self.fox_learning.get_learned_response(question)
        if learned:
            return f"🧠 (از یادگیری قبلی): {learned}"
        
        # اگر نه، از چند مدل بپرس
        responses = asyncio.run(self.get_multi_model_response(question))
        analysis = self.analyze_responses(responses)
        
        # یاد بگیر برای دفعه بعد
        self.learn_from_multi_model(question, analysis)
        
        return f"🤖 (ترکیب چند مدل): {analysis['best_response']}"

# Global instance
multi_model_learning = None
