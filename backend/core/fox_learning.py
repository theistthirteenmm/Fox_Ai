"""
Fox Learning & Teaching System
سیستم یادگیری و آموزش Fox
"""

import json
import os
from datetime import datetime
from typing import List, Dict
from backend.core.user_profile import UserProfile

class FoxLearningSystem:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        # Handle both dict and UserProfile object
        if isinstance(user_profile, dict):
            user_name = user_profile.get('name', 'حامد')
        else:
            user_name = user_profile.get_name()
        self.learning_file = f"data/profiles/{user_name}_learning.json"
        self.learned_data = self.load_learned_data()
    
    def load_learned_data(self) -> Dict:
        """بارگذاری اطلاعات یادگیری شده"""
        if os.path.exists(self.learning_file):
            with open(self.learning_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "custom_responses": {},
            "learned_facts": {},
            "cultural_knowledge": {},
            "personal_preferences": {},
            "daily_routines": {},
            "teaching_sessions": [],
            "learned_phrases": []
        }
    
    def save_learned_data(self):
        """ذخیره اطلاعات یادگیری"""
        os.makedirs(os.path.dirname(self.learning_file), exist_ok=True)
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.learned_data, f, ensure_ascii=False, indent=2)
    
    def teach_response(self, trigger: str, response: str):
        """آموزش پاسخ خاص"""
        self.learned_data["custom_responses"][trigger.lower()] = {
            "response": response,
            "taught_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        self.save_learned_data()
        return f"✅ یاد گرفتم! وقتی '{trigger}' گفتی، '{response}' جواب بدم"
    
    def teach_fact(self, topic: str, fact: str):
        """آموزش حقیقت جدید"""
        if topic not in self.learned_data["learned_facts"]:
            self.learned_data["learned_facts"][topic] = []
        
        self.learned_data["learned_facts"][topic].append({
            "fact": fact,
            "taught_at": datetime.now().isoformat()
        })
        self.save_learned_data()
        return f"✅ حقیقت جدید درباره '{topic}' یاد گرفتم!"
    
    def teach_culture(self, country: str, culture_info: str):
        """آموزش فرهنگ کشورها"""
        self.learned_data["cultural_knowledge"][country] = {
            "info": culture_info,
            "taught_at": datetime.now().isoformat()
        }
        self.save_learned_data()
        return f"✅ فرهنگ {country} رو یاد گرفتم!"
    
    def teach_routine(self, routine_name: str, description: str):
        """آموزش کارهای روزمره"""
        self.learned_data["daily_routines"][routine_name] = {
            "description": description,
            "taught_at": datetime.now().isoformat()
        }
        self.save_learned_data()
        return f"✅ روتین '{routine_name}' رو یاد گرفتم!"
    
    def teach_preference(self, category: str, preference: str):
        """آموزش ترجیحات شخصی"""
        self.learned_data["personal_preferences"][category] = {
            "preference": preference,
            "taught_at": datetime.now().isoformat()
        }
        self.save_learned_data()
        return f"✅ ترجیح شما در '{category}' رو یاد گرفتم!"
    
    def get_learned_response(self, user_input: str) -> str:
        """دریافت پاسخ یادگیری شده"""
        user_input_lower = user_input.lower()
        
        # جستجو در پاسخ‌های آموزش داده شده
        for trigger, data in self.learned_data["custom_responses"].items():
            if trigger in user_input_lower:
                # افزایش تعداد استفاده
                data["usage_count"] += 1
                self.save_learned_data()
                return data["response"]
        
        # جستجو در حقایق یادگیری شده
        for topic, facts in self.learned_data["learned_facts"].items():
            if topic in user_input_lower:
                if facts:
                    return f"راجع به {topic}: {facts[-1]['fact']}"
        
        # جستجو در اطلاعات فرهنگی
        for country, info in self.learned_data["cultural_knowledge"].items():
            if country in user_input_lower:
                return f"فرهنگ {country}: {info['info']}"
        
        return None
    
    def get_learning_stats(self) -> Dict:
        """آمار یادگیری"""
        return {
            "custom_responses": len(self.learned_data["custom_responses"]),
            "learned_facts": sum(len(facts) for facts in self.learned_data["learned_facts"].values()),
            "cultural_knowledge": len(self.learned_data["cultural_knowledge"]),
            "personal_preferences": len(self.learned_data["personal_preferences"]),
            "daily_routines": len(self.learned_data["daily_routines"]),
            "total_teachings": len(self.learned_data["teaching_sessions"])
        }
