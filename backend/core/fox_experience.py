"""
Fox Experience & Knowledge Dataset System
سیستم تجربه و دانش مصنوعی Fox
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from backend.core.user_profile import UserProfile
from backend.core.fox_dataset import PERSIAN_CONVERSATIONS, KNOWLEDGE_BASE, PERSONALITY_RESPONSES, get_response_for_input

class FoxExperienceSystem:
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.knowledge_base = self.load_knowledge_base()
        self.experience_multiplier = 30  # هر روز = 1 ماه تجربه
        
    def load_knowledge_base(self) -> Dict:
        """بارگذاری پایگاه دانش Fox"""
        # شروع با دیتاست آماده
        base_knowledge = {
            "conversations": PERSIAN_CONVERSATIONS.copy(),
            "personality_responses": PERSONALITY_RESPONSES.copy(),
            "knowledge_base": KNOWLEDGE_BASE.copy(),
            "learned_patterns": [
                # الگوهای یادگیری پایه
                "همیشه مؤدب و احترام‌آمیز باش",
                "به سوالات واضح و مفید جواب بده", 
                "اگر نمی‌دونی، صادقانه بگو",
                "از کاربر یاد بگیر و بهتر شو",
                "احساسات کاربر رو درک کن",
                "کمک‌کننده و مفید باش",
                "با زبان ساده و قابل فهم صحبت کن"
            ]
        }
        
        # اضافه کردن دانش تخصصی بر اساس سطح تجربه
        experience_level = self.get_base_experience_level()
        
        if experience_level >= 100:  # مبتدی
            base_knowledge["learned_patterns"].extend([
                "سوالات پیگیری بپرس",
                "جزئیات بیشتر ارائه بده",
                "مثال‌های عملی بزن"
            ])
        
        if experience_level >= 500:  # متوسط
            base_knowledge["learned_patterns"].extend([
                "ارتباط بین موضوعات برقرار کن",
                "پیشنهادات شخصی‌سازی شده بده",
                "از تجربیات قبلی استفاده کن"
            ])
        
        if experience_level >= 1000:  # پیشرفته
            base_knowledge["learned_patterns"].extend([
                "تحلیل عمیق‌تر ارائه بده",
                "راه‌حل‌های خلاقانه پیشنهاد کن",
                "الگوهای پیچیده تشخیص بده"
            ])
        
        return base_knowledge
    
    def get_base_experience_level(self) -> int:
        """دریافت سطح تجربه پایه"""
        return self.user_profile.profile.get('interaction_count', 0)
    
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
