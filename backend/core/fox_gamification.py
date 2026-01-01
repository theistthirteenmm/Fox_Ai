"""
🎮 Fox Gamification - بازی‌سازی تعامل با Fox
"""

import json
import os
from datetime import datetime
import random

class FoxGamification:
    def __init__(self):
        self.game_file = "data/gamification/fox_game.json"
        self.load_game_data()
        
    def load_game_data(self):
        """بارگذاری داده‌های بازی"""
        if os.path.exists(self.game_file):
            try:
                with open(self.game_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.fox_level = data.get("fox_level", 1)
                    self.experience = data.get("experience", 0)
                    self.achievements = data.get("achievements", [])
                    self.stats = data.get("stats", {
                        "conversations": 0,
                        "questions_answered": 0,
                        "things_learned": 0,
                        "days_active": 0,
                        "friendship_points": 0
                    })
                    return
            except:
                pass
        
        # مقادیر پیش‌فرض
        self.fox_level = 1
        self.experience = 0
        self.achievements = []
        self.stats = {
            "conversations": 0,
            "questions_answered": 0,
            "things_learned": 0,
            "days_active": 0,
            "friendship_points": 0
        }
    
    def save_game_data(self):
        """ذخیره داده‌های بازی"""
        os.makedirs(os.path.dirname(self.game_file), exist_ok=True)
        
        data = {
            "fox_level": self.fox_level,
            "experience": self.experience,
            "achievements": self.achievements,
            "stats": self.stats,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.game_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def gain_experience(self, interaction_type, amount=None):
        """کسب تجربه"""
        exp_rewards = {
            "conversation": 5,
            "question": 10,
            "learning": 15,
            "teaching": 20,
            "daily_login": 25,
            "achievement": 50
        }
        
        exp_gained = amount or exp_rewards.get(interaction_type, 5)
        self.experience += exp_gained
        
        # بروزرسانی آمار
        if interaction_type == "conversation":
            self.stats["conversations"] += 1
        elif interaction_type == "question":
            self.stats["questions_answered"] += 1
        elif interaction_type == "learning":
            self.stats["things_learned"] += 1
        
        # بررسی level up
        level_up_message = self.check_level_up()
        
        # بررسی achievements جدید
        new_achievements = self.check_achievements()
        
        self.save_game_data()
        
        result = f"✨ +{exp_gained} XP ({interaction_type})"
        if level_up_message:
            result += f"\n{level_up_message}"
        if new_achievements:
            result += f"\n{new_achievements}"
        
        return result
    
    def check_level_up(self):
        """بررسی level up"""
        required_exp = self.fox_level * 100
        
        if self.experience >= required_exp:
            old_level = self.fox_level
            self.fox_level += 1
            self.experience -= required_exp
            
            # پاداش level up
            self.stats["friendship_points"] += 10
            
            level_messages = [
                f"🎉 Fox به سطح {self.fox_level} رسید!",
                f"🦊 Fox قوی‌تر شد! سطح {self.fox_level}",
                f"⭐ تبریک! Fox الان سطح {self.fox_level} است",
                f"🚀 Fox ارتقا یافت! سطح {self.fox_level}"
            ]
            
            return random.choice(level_messages)
        
        return None
    
    def check_achievements(self):
        """بررسی achievements جدید"""
        new_achievements = []
        
        # تعریف achievements
        achievements_list = [
            {"id": "first_chat", "name": "اولین مکالمه", "condition": lambda: self.stats["conversations"] >= 1},
            {"id": "chatty", "name": "پرحرف", "condition": lambda: self.stats["conversations"] >= 10},
            {"id": "social", "name": "اجتماعی", "condition": lambda: self.stats["conversations"] >= 50},
            {"id": "curious", "name": "کنجکاو", "condition": lambda: self.stats["questions_answered"] >= 20},
            {"id": "teacher", "name": "معلم", "condition": lambda: self.stats["things_learned"] >= 10},
            {"id": "friend", "name": "دوست", "condition": lambda: self.stats["friendship_points"] >= 50},
            {"id": "level_5", "name": "سطح 5", "condition": lambda: self.fox_level >= 5},
            {"id": "level_10", "name": "سطح 10", "condition": lambda: self.fox_level >= 10},
        ]
        
        for achievement in achievements_list:
            if achievement["id"] not in [a["id"] for a in self.achievements]:
                if achievement["condition"]():
                    new_achievement = {
                        "id": achievement["id"],
                        "name": achievement["name"],
                        "earned_date": datetime.now().isoformat()
                    }
                    self.achievements.append(new_achievement)
                    new_achievements.append(achievement["name"])
                    
                    # پاداش achievement
                    self.gain_experience("achievement", 50)
        
        if new_achievements:
            return f"🏆 Achievement جدید: {', '.join(new_achievements)}"
        
        return None
    
    def get_fox_status(self):
        """وضعیت Fox"""
        next_level_exp = self.fox_level * 100
        progress = (self.experience / next_level_exp) * 100
        
        # تعیین شخصیت Fox بر اساس سطح
        if self.fox_level < 5:
            personality = "🦊 Fox کوچولو"
        elif self.fox_level < 10:
            personality = "🦊 Fox باهوش"
        elif self.fox_level < 20:
            personality = "🦊 Fox حرفه‌ای"
        else:
            personality = "🦊 Fox استاد"
        
        return f"""🎮 وضعیت Fox:
{personality} - سطح {self.fox_level}
✨ تجربه: {self.experience}/{next_level_exp} ({progress:.1f}%)
🏆 Achievements: {len(self.achievements)}
💬 مکالمات: {self.stats['conversations']}
❓ سوالات پاسخ داده: {self.stats['questions_answered']}
📚 چیزهای یادگرفته: {self.stats['things_learned']}
❤️ امتیاز دوستی: {self.stats['friendship_points']}"""
    
    def get_daily_challenge(self):
        """چالش روزانه"""
        challenges = [
            "10 سوال از Fox بپرس",
            "5 چیز جدید به Fox یاد بده",
            "20 دقیقه با Fox حرف بزن",
            "از Fox درباره هوا بپرس",
            "به Fox درباره روزت بگو"
        ]
        
        return f"🎯 چالش امروز: {random.choice(challenges)}"
    
    def get_fox_mood(self):
        """حالت Fox بر اساس تعاملات"""
        if self.stats["friendship_points"] > 100:
            return "😍 Fox عاشقتونه!"
        elif self.stats["friendship_points"] > 50:
            return "😊 Fox خوشحاله"
        elif self.stats["friendship_points"] > 20:
            return "🙂 Fox راضیه"
        else:
            return "😐 Fox منتظر بیشتر حرف زدن"

# Instance سراسری
fox_game = FoxGamification()
