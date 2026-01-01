"""
🕐 Time-Based Responses - پاسخ بر اساس زمان
"""

from datetime import datetime
import random

class TimeBasedResponses:
    def __init__(self):
        self.time_greetings = {
            "morning": ["صبح بخیر حامد! ☀️", "صبح به خیر! امروز چه برنامه‌ای داری؟", "سلام! صبح زیبایی است"],
            "afternoon": ["ظهر بخیر! 🌤️", "سلام! ناهار خوردی؟", "ظهرتون بخیر! چطور میگذره؟"],
            "evening": ["عصر بخیر! 🌅", "سلام! روز خوبی بود؟", "عصرتون بخیر! خسته نباشی"],
            "night": ["شب بخیر! 🌙", "سلام! دیر وقت کار می‌کنی؟", "شب بخیر! زود بخواب"]
        }
        
        self.time_suggestions = {
            "morning": ["وقت صبحانه است!", "قهوه بخور تا بیدار شی", "ورزش صبحگاهی خوبه"],
            "afternoon": ["وقت ناهاره!", "یکم استراحت کن", "آب بخور"],
            "evening": ["وقت شامه!", "فیلم ببین", "کتاب بخون"],
            "night": ["وقت خوابه!", "گوشی رو کنار بذار", "فردا زود بیدار شو"]
        }
    
    def get_time_period(self):
        """تشخیص زمان روز"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    def get_time_greeting(self):
        """سلام بر اساس زمان"""
        period = self.get_time_period()
        return random.choice(self.time_greetings[period])
    
    def get_time_suggestion(self):
        """پیشنهاد بر اساس زمان"""
        period = self.get_time_period()
        return random.choice(self.time_suggestions[period])
    
    def should_suggest_break(self):
        """آیا وقت استراحت است؟"""
        now = datetime.now()
        # هر 2 ساعت یکبار پیشنهاد استراحت
        return now.minute == 0 and now.hour % 2 == 0

# Instance سراسری
time_responses = TimeBasedResponses()
