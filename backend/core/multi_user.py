"""
Multi-User Profile Management System
سیستم مدیریت چند کاربره
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from backend.core.user_profile import UserProfile
from backend.core.introduction import FoxIntroduction

class MultiUserManager:
    def __init__(self, db_session):
        self.db = db_session
        self.profiles_dir = "data/profiles"
        self.current_user_file = "data/current_user.json"
        self.users_index_file = "data/users_index.json"
        
        # Create directories
        os.makedirs(self.profiles_dir, exist_ok=True)
        
        self.current_user = None
        self.load_current_user()
    
    def get_users_index(self) -> Dict:
        """دریافت فهرست کاربران"""
        if os.path.exists(self.users_index_file):
            with open(self.users_index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": [], "last_user": None}
    
    def save_users_index(self, index: Dict):
        """ذخیره فهرست کاربران"""
        with open(self.users_index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    def detect_user_change(self, user_input: str) -> Optional[str]:
        """تشخیص تغییر کاربر از متن"""
        # کلمات کلیدی برای تغییر کاربر
        switch_patterns = [
            "من", "اسمم", "نامم", "هستم",
            "پسر", "دختر", "همسر", "مادر", "پدر",
            "رادین", "سارا", "علی", "فاطمه"  # نام‌های رایج
        ]
        
        # اگر کاربر خودش معرفی کرد
        if any(pattern in user_input for pattern in ["من", "اسمم", "نامم"]):
            # استخراج نام از متن
            words = user_input.split()
            for i, word in enumerate(words):
                if word in ["من", "اسمم", "نامم"] and i + 1 < len(words):
                    potential_name = words[i + 1].strip("،.")
                    if len(potential_name) > 1:
                        return potential_name
        
        # اگر کاربر رابطه‌اش رو گفت
        if "پسر" in user_input and self.current_user:
            return f"پسر {self.current_user.get_name()}"
        elif "همسر" in user_input and self.current_user:
            return f"همسر {self.current_user.get_name()}"
        
        return None
    
    def is_writing_style_different(self, text: str) -> bool:
        """تشخیص تغییر سبک نوشتار (ساده)"""
        if not self.current_user:
            return False
        
        # بررسی‌های ساده برای تشخیص کاربر جدید
        current_traits = self.current_user.profile.get('personality_traits', [])
        
        # اگر متن خیلی رسمی باشه ولی کاربر فعلی غیررسمی باشه
        formal_words = ["شما", "جناب", "سرکار", "محترم"]
        informal_words = ["تو", "داداش", "رفیق", "یارو"]
        
        is_formal = any(word in text for word in formal_words)
        is_informal = any(word in text for word in informal_words)
        
        if "صمیمی" in current_traits and is_formal:
            return True
        elif "جدی" in current_traits and is_informal:
            return True
        
        return False
    
    def get_user_profile(self, user_name: str) -> UserProfile:
        """دریافت پروفایل کاربر"""
        profile_file = os.path.join(self.profiles_dir, f"{user_name}.json")
        
        # Create temporary profile file for this user
        temp_profile = UserProfile(self.db)
        temp_profile.profile_file = profile_file
        temp_profile.profile = temp_profile.load_profile()
        
        return temp_profile
    
    def switch_user(self, user_name: str) -> tuple[UserProfile, bool]:
        """تغییر کاربر فعال"""
        # بررسی اینکه کاربر وجود داره یا نه
        index = self.get_users_index()
        is_new_user = user_name not in [u['name'] for u in index['users']]
        
        if is_new_user:
            # اضافه کردن کاربر جدید به فهرست
            index['users'].append({
                'name': user_name,
                'created_at': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat()
            })
        else:
            # بروزرسانی آخرین بازدید
            for user in index['users']:
                if user['name'] == user_name:
                    user['last_seen'] = datetime.now().isoformat()
        
        index['last_user'] = user_name
        self.save_users_index(index)
        
        # تغییر کاربر فعال
        self.current_user = self.get_user_profile(user_name)
        
        # ذخیره کاربر فعال
        with open(self.current_user_file, 'w', encoding='utf-8') as f:
            json.dump({'current_user': user_name}, f, ensure_ascii=False)
        
        return self.current_user, is_new_user
    
    def load_current_user(self):
        """بارگذاری کاربر فعال"""
        if os.path.exists(self.current_user_file):
            with open(self.current_user_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                user_name = data.get('current_user')
                if user_name:
                    self.current_user = self.get_user_profile(user_name)
        
        # اگر کاربری نبود، از فهرست آخرین کاربر رو بگیر
        if not self.current_user:
            index = self.get_users_index()
            if index['last_user']:
                self.current_user = self.get_user_profile(index['last_user'])
    
    def get_all_users(self) -> List[Dict]:
        """دریافت همه کاربران"""
        return self.get_users_index()['users']
    
    def suggest_user_switch(self, user_input: str) -> Optional[str]:
        """پیشنهاد تغییر کاربر"""
        # تشخیص نام جدید
        potential_name = self.detect_user_change(user_input)
        if potential_name and (not self.current_user or potential_name != self.current_user.get_name()):
            return potential_name
        
        # تشخیص تغییر سبک
        if self.is_writing_style_different(user_input):
            return "کاربر_جدید"
        
        return None
    
    def get_switch_message(self, suggested_name: str) -> str:
        """پیام تغییر کاربر"""
        if suggested_name == "کاربر_جدید":
            return """
🤔 احساس می‌کنم با شخص جدیدی صحبت می‌کنم!

آیا شما همان کاربر قبلی هستید یا شخص جدیدی؟
اگر شخص جدیدی هستید، لطفاً اسمتان را بگویید تا بتوانم شما را بشناسم! 🦊
"""
        else:
            current_name = self.current_user.get_name() if self.current_user else "کاربر قبلی"
            return f"""
🤔 سلام! آیا شما {suggested_name} هستید؟

من الان با {current_name} صحبت می‌کردم. اگر شما شخص جدیدی هستید، خوشحال می‌شوم که آشناتان کنم! 🦊

برای تأیید فقط بگویید "بله" یا اسم خودتان را بگویید.
"""
