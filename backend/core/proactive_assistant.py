"""
🔔 Proactive Assistant - دستیار پیشگام
"""

import json
import os
from datetime import datetime, timedelta
import random

class ProactiveAssistant:
    def __init__(self):
        self.suggestions_file = "data/proactive/suggestions.json"
        self.reminders_file = "data/proactive/reminders.json"
        self.load_data()
        
    def load_data(self):
        """بارگذاری داده‌ها"""
        self.suggestions = self.load_json(self.suggestions_file, {"last_suggestions": []})
        self.reminders = self.load_json(self.reminders_file, {"reminders": []})
    
    def load_json(self, file_path, default):
        """بارگذاری فایل JSON"""
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return default
    
    def save_data(self):
        """ذخیره داده‌ها"""
        os.makedirs(os.path.dirname(self.suggestions_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.reminders_file), exist_ok=True)
        
        with open(self.suggestions_file, 'w', encoding='utf-8') as f:
            json.dump(self.suggestions, f, ensure_ascii=False, indent=2)
        
        with open(self.reminders_file, 'w', encoding='utf-8') as f:
            json.dump(self.reminders, f, ensure_ascii=False, indent=2)
    
    def get_time_based_suggestions(self):
        """پیشنهادات بر اساس زمان"""
        hour = datetime.now().hour
        
        morning_suggestions = [
            "☕ وقت قهوه صبحگاهی! انرژی بگیر",
            "🌅 صبح بخیر! برنامه امروزت چیه؟",
            "💪 ورزش صبحگاهی خوبه، حداقل کشش",
            "📰 اخبار امروز رو چک کردی؟"
        ]
        
        afternoon_suggestions = [
            "🍽️ وقت ناهاره! چی می‌خوری؟",
            "💧 آب بخور، بدنت نیاز داره",
            "👀 چشماتو استراحت بده، از صفحه دور شو",
            "🚶 یکم قدم بزن، خون به جریان بیفته"
        ]
        
        evening_suggestions = [
            "🍽️ شام چی داری؟ سبک بخور",
            "📚 وقت مطالعه یا فیلم دیدن",
            "👨‍👩‍👧‍👦 با خانواده وقت بگذرون",
            "📝 برنامه فردا رو بچین"
        ]
        
        night_suggestions = [
            "😴 وقت خوابه! گوشی رو کنار بذار",
            "🧘 یکم مدیتیشن یا آرامش",
            "📖 کتاب بخون تا خوابت ببره",
            "🌙 شب بخیر! فردا روز بهتری خواهد بود"
        ]
        
        if 6 <= hour < 12:
            return random.choice(morning_suggestions)
        elif 12 <= hour < 17:
            return random.choice(afternoon_suggestions)
        elif 17 <= hour < 21:
            return random.choice(evening_suggestions)
        else:
            return random.choice(night_suggestions)
    
    def get_health_suggestions(self):
        """پیشنهادات سلامتی"""
        health_tips = [
            "💧 آب بخور! حداقل 8 لیوان در روز",
            "👀 قانون 20-20-20: هر 20 دقیقه، 20 ثانیه به 20 متری نگاه کن",
            "🧘 نفس عمیق بکش، استرس رو کم کن",
            "🚶 حداقل 30 دقیقه در روز راه برو",
            "😴 7-8 ساعت بخواب، مغزت نیاز داره",
            "🥗 میوه و سبزی بخور، ویتامین بگیر"
        ]
        return random.choice(health_tips)
    
    def get_productivity_suggestions(self):
        """پیشنهادات بهره‌وری"""
        productivity_tips = [
            "📝 لیست کارهای امروز رو بنویس",
            "⏰ تکنیک پومودورو امتحان کن: 25 دقیقه کار، 5 دقیقه استراحت",
            "🎯 روی مهم‌ترین کار تمرکز کن",
            "📱 اعلان‌های غیرضروری رو خاموش کن",
            "🧹 میز کارت رو مرتب کن، ذهنت هم مرتب میشه",
            "📚 چیز جدیدی یاد بگیر، مغزت رو فعال نگه دار"
        ]
        return random.choice(productivity_tips)
    
    def add_reminder(self, text, remind_time):
        """اضافه کردن یادآوری"""
        reminder = {
            "id": len(self.reminders["reminders"]) + 1,
            "text": text,
            "remind_time": remind_time,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        
        self.reminders["reminders"].append(reminder)
        self.save_data()
        return f"✅ یادآوری اضافه شد: {text}"
    
    def check_reminders(self):
        """بررسی یادآوری‌ها"""
        now = datetime.now()
        active_reminders = []
        
        for reminder in self.reminders["reminders"]:
            if not reminder["completed"]:
                remind_time = datetime.fromisoformat(reminder["remind_time"])
                if now >= remind_time:
                    active_reminders.append(reminder)
        
        return active_reminders
    
    def get_random_suggestion(self):
        """پیشنهاد تصادفی"""
        suggestion_types = [
            self.get_time_based_suggestions,
            self.get_health_suggestions,
            self.get_productivity_suggestions
        ]
        
        suggestion_func = random.choice(suggestion_types)
        return suggestion_func()
    
    def should_give_suggestion(self):
        """آیا وقت پیشنهاد است؟"""
        # هر 30 دقیقه یک پیشنهاد
        now = datetime.now()
        last_suggestion = self.suggestions.get("last_suggestion_time")
        
        if not last_suggestion:
            return True
        
        last_time = datetime.fromisoformat(last_suggestion)
        return (now - last_time).total_seconds() > 1800  # 30 minutes
    
    def give_suggestion(self):
        """ارائه پیشنهاد"""
        if self.should_give_suggestion():
            suggestion = self.get_random_suggestion()
            
            # ذخیره زمان آخرین پیشنهاد
            self.suggestions["last_suggestion_time"] = datetime.now().isoformat()
            self.suggestions["last_suggestions"].append({
                "text": suggestion,
                "time": datetime.now().isoformat()
            })
            
            # نگه داشتن فقط 10 پیشنهاد اخیر
            if len(self.suggestions["last_suggestions"]) > 10:
                self.suggestions["last_suggestions"] = self.suggestions["last_suggestions"][-10:]
            
            self.save_data()
            return f"💡 {suggestion}"
        
        return None

# Instance سراسری
proactive_assistant = ProactiveAssistant()
