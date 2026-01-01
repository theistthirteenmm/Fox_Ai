"""
📊 Mood Tracking - ردیابی حالت روحی
"""

import json
import os
from datetime import datetime

class MoodTracker:
    def __init__(self):
        self.mood_file = "data/profiles/حامد_mood.json"
        self.positive_words = [
            "خوب", "عالی", "خوشحال", "شاد", "راضی", "خندیدم", "لذت", 
            "موفق", "بهتر", "آرام", "راحت", "خوشگذران"
        ]
        self.negative_words = [
            "بد", "ناراحت", "خسته", "غمگین", "عصبانی", "استرس", "نگران",
            "افسرده", "بیحال", "کسل", "درد", "مشکل"
        ]
        self.mood_history = self.load_mood_history()
    
    def load_mood_history(self):
        """بارگذاری تاریخچه حالات"""
        if os.path.exists(self.mood_file):
            try:
                with open(self.mood_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"daily_moods": [], "overall_trend": "neutral"}
    
    def save_mood_history(self):
        """ذخیره تاریخچه حالات"""
        os.makedirs(os.path.dirname(self.mood_file), exist_ok=True)
        with open(self.mood_file, 'w', encoding='utf-8') as f:
            json.dump(self.mood_history, f, ensure_ascii=False, indent=2)
    
    def analyze_mood(self, message):
        """تحلیل حالت از پیام"""
        message_lower = message.lower()
        
        positive_score = sum(1 for word in self.positive_words if word in message_lower)
        negative_score = sum(1 for word in self.negative_words if word in message_lower)
        
        if positive_score > negative_score:
            mood = "positive"
        elif negative_score > positive_score:
            mood = "negative"
        else:
            mood = "neutral"
        
        # ذخیره در تاریخچه
        today = datetime.now().strftime("%Y-%m-%d")
        mood_entry = {
            "date": today,
            "time": datetime.now().strftime("%H:%M"),
            "mood": mood,
            "message": message[:50] + "..." if len(message) > 50 else message
        }
        
        self.mood_history["daily_moods"].append(mood_entry)
        
        # نگه داشتن فقط 30 روز اخیر
        if len(self.mood_history["daily_moods"]) > 30:
            self.mood_history["daily_moods"] = self.mood_history["daily_moods"][-30:]
        
        self.save_mood_history()
        return mood
    
    def get_mood_response(self, mood):
        """پاسخ بر اساس حالت"""
        responses = {
            "positive": [
                "خوشحالم که حالت خوبه! 😊",
                "عالیه! انرژی مثبتت رو حس می‌کنم",
                "آفرین! همینطور شاد باش"
            ],
            "negative": [
                "متأسفم که حالت خوب نیست 😔",
                "نگران نباش، همه چیز درست میشه",
                "اگه می‌خوای حرف بزنی، اینجام"
            ],
            "neutral": [
                "چطور می‌تونم کمکت کنم؟",
                "چه خبر؟ چیزی لازم داری؟",
                "همه چیز خوبه؟"
            ]
        }
        
        import random
        return random.choice(responses[mood])
    
    def get_mood_stats(self):
        """آمار حالات"""
        if not self.mood_history["daily_moods"]:
            return "هنوز حالتی ثبت نشده"
        
        moods = [entry["mood"] for entry in self.mood_history["daily_moods"]]
        positive_count = moods.count("positive")
        negative_count = moods.count("negative")
        neutral_count = moods.count("neutral")
        
        total = len(moods)
        return f"""📊 آمار حالات شما:
😊 مثبت: {positive_count} ({positive_count/total*100:.1f}%)
😔 منفی: {negative_count} ({negative_count/total*100:.1f}%)
😐 خنثی: {neutral_count} ({neutral_count/total*100:.1f}%)

📈 کل: {total} مورد"""

# Instance سراسری
mood_tracker = MoodTracker()
