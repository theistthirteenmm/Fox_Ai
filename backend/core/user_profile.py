"""
Fox AI - User Profile & Relationship System
شخصی‌سازی و سیستم رابطه کاربری
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from backend.database.models import Memory

class UserProfile:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.profile_file = "data/user_profile.json"
        self.profile = self.load_profile()
        
    def load_profile(self) -> Dict:
        """بارگذاری پروفایل کاربر"""
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "is_first_time": True,
            "name": "",
            "interests": [],
            "personality_traits": [],
            "relationship_level": 0,  # 0=stranger, 10=best friend
            "favorite_topics": [],
            "communication_style": "friendly",
            "created_at": datetime.now().isoformat(),
            "last_interaction": None,
            "interaction_count": 0,
            "memories": []
        }
    
    def save_profile(self):
        """ذخیره پروفایل"""
        os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)
    
    def is_first_time(self) -> bool:
        """آیا اولین بار است؟"""
        return self.profile.get("is_first_time", True)
    
    def complete_introduction(self, name: str, interests: List[str], traits: List[str]):
        """تکمیل معرفی اولیه"""
        self.profile.update({
            "is_first_time": False,
            "name": name,
            "interests": interests,
            "personality_traits": traits,
            "relationship_level": 1
        })
        self.save_profile()
    
    def get_name(self) -> str:
        """دریافت نام کاربر"""
        return self.profile.get("name", "دوست")
    
    def add_interest(self, interest: str):
        """اضافه کردن علاقه جدید"""
        if interest not in self.profile["interests"]:
            self.profile["interests"].append(interest)
            self.save_profile()
    
    def update_relationship_level(self, change: int = 1):
        """بروزرسانی سطح رابطه"""
        self.profile["relationship_level"] = min(10, max(0, 
            self.profile["relationship_level"] + change))
        self.save_profile()
    
    def record_interaction(self):
        """ثبت تعامل جدید"""
        self.profile["last_interaction"] = datetime.now().isoformat()
        self.profile["interaction_count"] += 1
        self.save_profile()
    
    def get_relationship_status(self) -> str:
        """دریافت وضعیت رابطه"""
        level = self.profile["relationship_level"]
        if level == 0: return "غریبه"
        elif level <= 2: return "آشنا"
        elif level <= 4: return "دوست"
        elif level <= 6: return "دوست خوب"
        elif level <= 8: return "دوست نزدیک"
        else: return "بهترین دوست"
    
    def should_be_proactive(self) -> bool:
        """آیا باید فعال باشد؟"""
        return self.profile["relationship_level"] >= 3
    
    def get_conversation_starters(self) -> List[str]:
        """پیشنهادات شروع مکالمه"""
        name = self.get_name()
        interests = self.profile["interests"]
        
        starters = [
            f"سلام {name}! چطوری؟ چه خبر؟",
            f"{name} عزیز، امروز چیکار می‌کنی؟",
            "حوصلت سر نمیره؟ بیا یه چیز جالب یاد بگیریم!",
        ]
        
        if interests:
            interest = interests[0] if interests else "برنامه‌نویسی"
            starters.append(f"راستی {name}، چیز جدیدی راجع به {interest} یاد گرفتی؟")
        
        return starters

class FoxPersonality:
    def __init__(self, user_profile: UserProfile):
        self.user = user_profile
        
    def get_greeting_style(self) -> str:
        """سبک سلام بر اساس رابطه"""
        level = self.user.profile["relationship_level"]
        name = self.user.get_name()
        
        if level == 0:
            return "سلام! من Fox هستم 🦊"
        elif level <= 2:
            return f"سلام {name}! 🦊"
        elif level <= 5:
            return f"سلام {name} عزیز! چطوری؟ 🦊✨"
        else:
            return f"سلاااام {name} جونم! 🦊💕 دلم برات تنگ شده بود!"
    
    def get_response_style(self) -> Dict[str, any]:
        """سبک پاسخ بر اساس رابطه"""
        level = self.user.profile["relationship_level"]
        
        if level <= 2:
            return {
                "formality": "polite",
                "emoji_frequency": "low",
                "curiosity": "medium",
                "proactiveness": "low"
            }
        elif level <= 5:
            return {
                "formality": "friendly",
                "emoji_frequency": "medium", 
                "curiosity": "high",
                "proactiveness": "medium"
            }
        else:
            return {
                "formality": "intimate",
                "emoji_frequency": "high",
                "curiosity": "very_high", 
                "proactiveness": "high"
            }
    
    def should_ask_question(self) -> bool:
        """آیا باید سوال بپرسد؟"""
        return self.user.profile["relationship_level"] >= 2
    
    def get_random_question(self) -> str:
        """سوال تصادفی برای ادامه مکالمه"""
        questions = [
            "راستی، امروز چیکار کردی؟",
            "چیز جدیدی یاد گرفتی؟",
            "حالت چطوره؟",
            "چیزی هست که بخوای راجعش صحبت کنیم؟",
            "پروژه جدیدی داری؟",
            "چه چیزی الان ذهنت رو درگیر کرده؟"
        ]
        
        import random
        return random.choice(questions)
