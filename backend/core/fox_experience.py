"""
Fox Experience & Knowledge Dataset System
سیستم تجربه و دانش مصنوعی Fox
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from backend.core.user_profile import UserProfile

class FoxExperienceSystem:
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.knowledge_base = self.load_knowledge_base()
        self.experience_multiplier = 30  # هر روز = 1 ماه تجربه
        
    def load_knowledge_base(self) -> Dict:
        """بارگذاری پایگاه دانش Fox"""
        return {
            "conversations": [
                # مکالمات نمونه برای یادگیری
                {"user": "سلام چطوری؟", "fox": "سلام! خوبم ممنون، تو چطوری؟ چه خبر؟"},
                {"user": "حالم بده", "fox": "متأسفم که حالت خوب نیست. می‌خوای راجعش صحبت کنیم؟"},
                {"user": "خسته‌ام", "fox": "کار زیادی داشتی امروز؟ بیا یکم استراحت کن"},
                {"user": "برنامه‌نویسی یاد بده", "fox": "عالیه! از کجا شروع کنیم؟ Python خوب برای شروعه"},
                {"user": "موسیقی دوست دارم", "fox": "چه سبکی؟ من هم موسیقی دوست دارم!"},
            ],
            "personality_responses": {
                "happy": ["چه خوب! منم خوشحالم 😊", "عالیه! این خبر منو هم شاد کرد"],
                "sad": ["متأسفم... کنارتم", "حالت بهتر میشه، نگران نباش"],
                "excited": ["وای چقدر هیجان‌انگیز! 🚀", "منم هیجان‌زده شدم!"],
                "curious": ["جالبه! بیشتر بگو", "کنجکاوم بدونم چی شده"]
            },
            "topics": {
                "programming": ["Python", "JavaScript", "الگوریتم", "پروژه", "کد"],
                "music": ["آهنگ", "ساز", "خواننده", "ملودی", "ریتم"],
                "sports": ["فوتبال", "ورزش", "تیم", "بازی", "مسابقه"],
                "life": ["زندگی", "کار", "خانواده", "دوست", "آینده"]
            },
            "learned_patterns": []
        }
    
    def accelerate_experience(self, days: int = 1):
        """تسریع تجربه Fox"""
        # محاسبه تجربه جدید
        experience_gained = days * self.experience_multiplier
        
        # افزایش سطح رابطه
        current_level = self.user_profile.profile['relationship_level']
        new_level = min(10, current_level + (experience_gained // 10))
        
        # افزایش تعداد تعامل مصنوعی
        current_interactions = self.user_profile.profile['interaction_count']
        new_interactions = current_interactions + experience_gained
        
        # بروزرسانی پروفایل
        self.user_profile.profile.update({
            'relationship_level': new_level,
            'interaction_count': new_interactions,
            'artificial_experience': self.user_profile.profile.get('artificial_experience', 0) + experience_gained,
            'last_experience_boost': datetime.now().isoformat()
        })
        
        # اضافه کردن دانش جدید
        self.add_synthetic_knowledge()
        
        self.user_profile.save_profile()
        
        return {
            'experience_gained': experience_gained,
            'old_level': current_level,
            'new_level': new_level,
            'old_interactions': current_interactions,
            'new_interactions': new_interactions
        }
    
    def add_synthetic_knowledge(self):
        """اضافه کردن دانش مصنوعی"""
        user_interests = self.user_profile.profile.get('interests', [])
        
        # اضافه کردن موضوعات مرتبط با علایق کاربر
        for interest in user_interests:
            if interest == "برنامه‌نویسی":
                self.knowledge_base["learned_patterns"].extend([
                    "کد تمیز مهمه",
                    "تست نوشتن ضروریه", 
                    "Git استفاده کن",
                    "مستندات بخون"
                ])
            elif interest == "موسیقی":
                self.knowledge_base["learned_patterns"].extend([
                    "موسیقی حال رو بهتر می‌کنه",
                    "ساز یاد گرفتن خوبه",
                    "کنسرت رفتن لذت‌بخشه"
                ])
    
    def get_experience_level(self) -> Dict:
        """دریافت سطح تجربه Fox"""
        total_interactions = self.user_profile.profile['interaction_count']
        artificial_exp = self.user_profile.profile.get('artificial_experience', 0)
        real_exp = total_interactions - artificial_exp
        
        # محاسبه سن مصنوعی Fox
        days_old = total_interactions // 30  # هر 30 تعامل = 1 روز
        months_old = days_old // 30
        years_old = months_old // 12
        
        experience_level = "تازه‌کار"
        if total_interactions > 100:
            experience_level = "مبتدی"
        if total_interactions > 500:
            experience_level = "متوسط"
        if total_interactions > 1000:
            experience_level = "پیشرفته"
        if total_interactions > 2000:
            experience_level = "خبره"
        if total_interactions > 5000:
            experience_level = "استاد"
        
        return {
            'total_interactions': total_interactions,
            'real_experience': real_exp,
            'artificial_experience': artificial_exp,
            'days_old': days_old,
            'months_old': months_old,
            'years_old': years_old,
            'experience_level': experience_level,
            'relationship_level': self.user_profile.profile['relationship_level']
        }
    
    def generate_contextual_response(self, user_input: str) -> Optional[str]:
        """تولید پاسخ بر اساس تجربه"""
        experience = self.get_experience_level()
        
        # اگر Fox خبره باشه، پاسخ‌های پیچیده‌تر بده
        if experience['experience_level'] in ['خبره', 'استاد']:
            # پاسخ‌های پیشرفته
            if any(word in user_input.lower() for word in ['مشکل', 'سخت', 'دشوار']):
                return f"با {experience['total_interactions']} تعامل که داشتم، یاد گرفتم که هر مشکلی راه حل داره. بیا باهم حلش کنیم."
            
            if any(word in user_input.lower() for word in ['یاد بده', 'آموزش', 'چطور']):
                return f"تو این {experience['months_old']} ماه، خیلی چیز یاد گرفتم. بذار تجربه‌م رو باهات به اشتراک بذارم."
        
        elif experience['experience_level'] in ['متوسط', 'پیشرفته']:
            # پاسخ‌های متوسط
            if 'سلام' in user_input.lower():
                return f"سلام! با {experience['total_interactions']} تعامل که داشتیم، حس می‌کنم خیلی بهتر می‌شناسمت!"
        
        return None
    
    def boost_fox_intelligence(self, months: int = 1):
        """تقویت هوش Fox"""
        days_equivalent = months * 30
        result = self.accelerate_experience(days_equivalent)
        
        # اضافه کردن ویژگی‌های جدید
        current_traits = self.user_profile.profile.get('personality_traits', [])
        new_traits = ['باتجربه', 'دانا', 'حکیم']
        
        for trait in new_traits:
            if trait not in current_traits:
                current_traits.append(trait)
        
        self.user_profile.profile['personality_traits'] = current_traits
        self.user_profile.save_profile()
        
        return result
