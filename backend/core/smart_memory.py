"""
🧠 Smart Context Memory - حافظه هوشمند Fox
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re
from collections import defaultdict

class SmartMemory:
    def __init__(self):
        self.memory_file = "data/context/smart_memory.json"
        self.patterns_file = "data/context/user_patterns.json"
        self.load_memory()
        
    def load_memory(self):
        """بارگذاری حافظه هوشمند"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                self.memory = json.load(f)
        else:
            self.memory = {
                "conversations": [],
                "topics": {},
                "keywords": {},
                "user_preferences": {},
                "context_links": []
            }
            
        if os.path.exists(self.patterns_file):
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                self.patterns = json.load(f)
        else:
            self.patterns = {
                "frequent_topics": {},
                "time_patterns": {},
                "mood_patterns": {},
                "question_types": {}
            }
    
    def save_memory(self):
        """ذخیره حافظه"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
            
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, ensure_ascii=False, indent=2)
    
    def add_conversation(self, user_input: str, ai_response: str, context: Dict = None):
        """اضافه کردن مکالمه جدید"""
        timestamp = datetime.now().isoformat()
        
        # استخراج کلمات کلیدی
        keywords = self.extract_keywords(user_input)
        topic = self.detect_topic(user_input)
        
        conversation = {
            "timestamp": timestamp,
            "user_input": user_input,
            "ai_response": ai_response,
            "keywords": keywords,
            "topic": topic,
            "context": context or {}
        }
        
        self.memory["conversations"].append(conversation)
        
        # آپدیت آمار موضوعات
        if topic:
            self.memory["topics"][topic] = self.memory["topics"].get(topic, 0) + 1
            
        # آپدیت کلمات کلیدی
        for keyword in keywords:
            self.memory["keywords"][keyword] = self.memory["keywords"].get(keyword, 0) + 1
            
        # تحلیل الگوها
        self.analyze_patterns(user_input, timestamp)
        
        # نگهداری فقط 1000 مکالمه اخیر
        if len(self.memory["conversations"]) > 1000:
            self.memory["conversations"] = self.memory["conversations"][-1000:]
            
        self.save_memory()
    
    def extract_keywords(self, text: str) -> List[str]:
        """استخراج کلمات کلیدی"""
        # حذف کلمات رایج
        stop_words = {'که', 'در', 'از', 'به', 'با', 'را', 'و', 'یا', 'این', 'آن', 'چه', 'چی', 'کی', 'کجا'}
        
        # استخراج کلمات
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if len(w) > 2 and w not in stop_words]
        
        return keywords[:10]  # حداکثر 10 کلمه
    
    def detect_topic(self, text: str) -> str:
        """تشخیص موضوع"""
        topics = {
            'برنامه‌نویسی': ['کد', 'برنامه', 'پایتون', 'جاوا', 'اسکریپت', 'api', 'database'],
            'تکنولوژی': ['کامپیوتر', 'موبایل', 'اینترنت', 'سایت', 'اپلیکیشن'],
            'علم': ['ریاضی', 'فیزیک', 'شیمی', 'زیست', 'علمی'],
            'زندگی': ['کار', 'خانواده', 'دوست', 'زندگی', 'روزانه'],
            'سرگرمی': ['فیلم', 'موزیک', 'بازی', 'کتاب', 'ورزش']
        }
        
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
                
        return 'عمومی'
    
    def analyze_patterns(self, user_input: str, timestamp: str):
        """تحلیل الگوهای کاربر"""
        hour = datetime.fromisoformat(timestamp).hour
        
        # الگوی زمانی
        time_slot = f"{hour:02d}:00"
        self.patterns["time_patterns"][time_slot] = self.patterns["time_patterns"].get(time_slot, 0) + 1
        
        # نوع سوال
        if '؟' in user_input:
            question_type = 'سوال'
        elif any(word in user_input.lower() for word in ['لطفا', 'میشه', 'کمک']):
            question_type = 'درخواست'
        else:
            question_type = 'گفتگو'
            
        self.patterns["question_types"][question_type] = self.patterns["question_types"].get(question_type, 0) + 1
    
    def get_relevant_context(self, current_input: str, limit: int = 5) -> List[Dict]:
        """یافتن مکالمات مرتبط"""
        current_keywords = set(self.extract_keywords(current_input))
        current_topic = self.detect_topic(current_input)
        
        relevant_conversations = []
        
        for conv in reversed(self.memory["conversations"][-100:]):  # 100 مکالمه اخیر
            score = 0
            
            # امتیاز بر اساس کلمات مشترک
            common_keywords = set(conv["keywords"]) & current_keywords
            score += len(common_keywords) * 2
            
            # امتیاز بر اساس موضوع مشترک
            if conv["topic"] == current_topic:
                score += 3
                
            # امتیاز بر اساس زمان (مکالمات اخیر بیشتر)
            days_ago = (datetime.now() - datetime.fromisoformat(conv["timestamp"])).days
            if days_ago < 7:
                score += 2
            elif days_ago < 30:
                score += 1
                
            if score > 0:
                relevant_conversations.append({
                    "conversation": conv,
                    "score": score
                })
        
        # مرتب‌سازی بر اساس امتیاز
        relevant_conversations.sort(key=lambda x: x["score"], reverse=True)
        
        return [item["conversation"] for item in relevant_conversations[:limit]]
    
    def get_user_insights(self) -> Dict:
        """تحلیل رفتار کاربر"""
        total_conversations = len(self.memory["conversations"])
        
        if total_conversations == 0:
            return {"message": "هنوز مکالمه‌ای ثبت نشده"}
        
        # محبوب‌ترین موضوعات
        top_topics = sorted(self.memory["topics"].items(), key=lambda x: x[1], reverse=True)[:5]
        
        # فعال‌ترین ساعات
        top_hours = sorted(self.patterns["time_patterns"].items(), key=lambda x: x[1], reverse=True)[:3]
        
        # آخرین فعالیت
        last_conversation = self.memory["conversations"][-1]["timestamp"]
        last_date = datetime.fromisoformat(last_conversation).strftime("%Y/%m/%d %H:%M")
        
        return {
            "total_conversations": total_conversations,
            "favorite_topics": top_topics,
            "active_hours": top_hours,
            "last_activity": last_date,
            "question_types": dict(self.patterns["question_types"])
        }
    
    def suggest_topics(self) -> List[str]:
        """پیشنهاد موضوعات بر اساس تاریخچه"""
        suggestions = []
        
        # بر اساس موضوعات محبوب
        top_topics = sorted(self.memory["topics"].items(), key=lambda x: x[1], reverse=True)[:3]
        
        topic_suggestions = {
            'برنامه‌نویسی': ['آیا سوال جدیدی در مورد کدنویسی داری؟', 'بیا یه پروژه جدید شروع کنیم!'],
            'تکنولوژی': ['چه خبر از دنیای تکنولوژی؟', 'آخرین اخبار تک رو می‌خوای؟'],
            'علم': ['بیا یه موضوع علمی جالب بحث کنیم', 'سوال علمی جدید داری؟'],
            'زندگی': ['چطور می‌تونم تو زندگی روزانه‌ت کمکت کنم؟', 'چه برنامه‌ای برای امروز داری؟'],
            'سرگرمی': ['فیلم یا کتاب جدیدی پیشنهاد بدم؟', 'بیا یه بحث سرگرم‌کننده داشته باشیم']
        }
        
        for topic, count in top_topics:
            if topic in topic_suggestions:
                suggestions.extend(topic_suggestions[topic])
                
        return suggestions[:5]

# نمونه استفاده
smart_memory = SmartMemory()
