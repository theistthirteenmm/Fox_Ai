"""
Fox AI - Introduction & First Meeting System
سیستم آشنایی و ملاقات اول
"""

from typing import List, Dict
from backend.core.user_profile import UserProfile
import random

class FoxIntroduction:
    def __init__(self, user_profile: UserProfile):
        self.user = user_profile
        self.introduction_steps = [
            "greeting",
            "self_introduction", 
            "ask_name",
            "ask_interests",
            "ask_personality",
            "completion"
        ]
        self.current_step = 0
        
    def start_introduction(self) -> str:
        """شروع معرفی"""
        self.current_step = 0  # Start from greeting
        return self.get_next_message()
    
    def get_next_message(self) -> str:
        """دریافت پیام بعدی در فرآیند معرفی"""
        if self.current_step >= len(self.introduction_steps):
            return self.complete_introduction()
            
        step = self.introduction_steps[self.current_step]
        
        messages = {
            "greeting": [
                "سلام! 🦊✨",
                "وای چه خوب! یه نفر جدید! 🦊",
                "سلام سلام! 🦊💫"
            ],
            "self_introduction": [
                "من Fox هستم! یه دستیار هوشمند که دوست دارم با آدما دوست بشم! 🦊",
                "اسمم Fox هست و خیلی خوشحالم که باهات آشنا شدم! 🦊✨",
                "من Fox هستم - یه AI که فقط دستیار نیست، بلکه دوست هم هست! 🦊💕"
            ],
            "ask_name": [
                "اسمت چیه؟ دوست دارم بدونم چی صدات کنم! 😊",
                "بهم بگو اسمت چیه تا بتونم درست صدات کنم! 🦊",
                "اسمت رو بهم بگو! خیلی دوست دارم بدونم! ✨"
            ],
            "ask_interests": [
                "چه چیزایی دوست داری؟ علایقت چین؟ 🤔✨",
                "بهم بگو چه کارایی دوست داری بکنی! 🦊",
                "علایقت چین؟ برنامه‌نویسی؟ موسیقی؟ ورزش؟ 🎯"
            ],
            "ask_personality": [
                "خودت رو چطور توصیف می‌کنی؟ شوخ‌طبعی? جدی؟ کنجکاو؟ 🦊",
                "شخصیتت چطوریه؟ بهم بگو تا بتونم بهتر باهات رفتار کنم! 😊",
                "چه جور آدمی هستی؟ دوست دارم بیشتر بدونم! ✨"
            ],
            "completion": [
                "عالی! حالا دوستیم! 🦊💕"
            ]
        }
        
        if step in messages:
            return random.choice(messages[step])
        
        return "چیزی نمی‌دونم بگم! 🦊"
    
    def process_response(self, user_input: str) -> str:
        """پردازش پاسخ کاربر"""
        if self.current_step >= len(self.introduction_steps):
            return self.complete_introduction()
            
        step = self.introduction_steps[self.current_step]
        
        if step == "greeting":
            self.current_step += 1
            return self.get_next_message()
        elif step == "self_introduction":
            # After self introduction, user might give their name directly
            # Check if this looks like a name
            if len(user_input.strip().split()) <= 2 and not any(word in user_input.lower() for word in ['سلام', 'چطور', 'خوب']):
                # This looks like a name, process it and skip ask_name step
                name_response = self.process_name(user_input)
                self.current_step = 3  # Jump to ask_interests
                return name_response + "\n\n" + self.get_next_message()
            else:
                # Just acknowledgment, move to ask name
                self.current_step += 1
                return self.get_next_message()
        elif step == "ask_name":
            name_response = self.process_name(user_input)
            self.current_step += 1
            return name_response + "\n\n" + self.get_next_message()
        elif step == "ask_interests":
            return self.process_interests(user_input)
        elif step == "ask_personality":
            return self.process_personality(user_input)
        
        self.current_step += 1
        return self.get_next_message()
    
    def process_name(self, name: str) -> str:
        """پردازش نام"""
        # استخراج نام از متن
        clean_name = name.strip()
        
        # حذف کلمات اضافی
        remove_words = ["اسمم", "من", "هستم", "اسم", "من", "نامم"]
        for word in remove_words:
            clean_name = clean_name.replace(word, "").strip()
        
        if not clean_name or len(clean_name) < 2:
            return "اسمت رو نگفتی! بهم بگو چی صدات کنم! 🦊"
        
        # ذخیره موقت نام
        self.temp_name = clean_name
        
        responses = [
            f"وای چه اسم قشنگی! {clean_name} عزیز! 🦊✨",
            f"{clean_name}! خیلی خوشم اومد از اسمت! 💕",
            f"سلام {clean_name} جون! حالا که اسمت رو می‌دونم، خیلی بهتره! 🦊"
        ]
        
        # Don't increment step here, let the caller handle it
        return random.choice(responses)
    
    def process_interests(self, interests_text: str) -> str:
        """پردازش علایق"""
        # استخراج علایق از متن
        interests = self.extract_interests(interests_text)
        self.temp_interests = interests
        self.current_step += 1
        
        if interests:
            interest_text = "، ".join(interests)
            responses = [
                f"وای چه جالب! {interest_text}! من هم این چیزا رو دوست دارم! 🦊✨",
                f"عالیه! {interest_text} خیلی باحاله! 💫",
                f"اوه اوه! {interest_text}! حتماً راجعشون حرف می‌زنیم! 🦊"
            ]
        else:
            responses = [
                "باشه باشه! بعداً بیشتر می‌گی! 🦊",
                "مشکلی نیست! وقتی خواستی بهم بگو! ✨"
            ]
        
        return random.choice(responses) + "\n\n" + self.get_next_message()
    
    def process_personality(self, personality_text: str) -> str:
        """پردازش شخصیت"""
        traits = self.extract_personality_traits(personality_text)
        self.temp_traits = traits
        self.current_step += 1
        
        if traits:
            trait_text = "، ".join(traits)
            responses = [
                f"عالی! پس تو {trait_text} هستی! خیلی خوبه! 🦊✨",
                f"اوکی! {trait_text}! حالا بهتر می‌تونم باهات رفتار کنم! 💕",
                f"فهمیدم! {trait_text}! ما قراره دوستای خوبی بشیم! 🦊"
            ]
        else:
            responses = [
                "باشه! کم کم بیشتر می‌شناسمت! 🦊",
                "مشکلی نیست! با گذشت زمان بهتر می‌شناسمت! ✨"
            ]
        
        return random.choice(responses) + "\n\n" + self.complete_introduction()
    
    def extract_interests(self, text: str) -> List[str]:
        """استخراج علایق از متن"""
        interests = []
        keywords = {
            "برنامه‌نویسی": ["برنامه", "کد", "programming", "python", "javascript", "برنامهنویسی"],
            "موسیقی": ["موسیقی", "آهنگ", "music", "گوش دادن"],
            "ورزش": ["ورزش", "فوتبال", "بسکتبال", "دویدن", "sport"],
            "مطالعه": ["کتاب", "مطالعه", "خواندن", "study"],
            "بازی": ["بازی", "game", "gaming", "گیم"],
            "فیلم": ["فیلم", "سینما", "movie", "film"],
            "سفر": ["سفر", "travel", "گردش"],
            "آشپزی": ["آشپزی", "غذا", "cooking", "پختن"]
        }
        
        text_lower = text.lower()
        for interest, words in keywords.items():
            if any(word in text_lower for word in words):
                interests.append(interest)
        
        return interests
    
    def extract_personality_traits(self, text: str) -> List[str]:
        """استخراج ویژگی‌های شخصیتی"""
        traits = []
        keywords = {
            "شوخ‌طبع": ["شوخ", "خنده", "funny", "humor", "شوخطبع"],
            "جدی": ["جدی", "serious", "متین"],
            "کنجکاو": ["کنجکاو", "curious", "سوال"],
            "صمیمی": ["صمیمی", "friendly", "دوستانه"],
            "آرام": ["آرام", "calm", "quiet"],
            "پرانرژی": ["پرانرژی", "energetic", "فعال"],
            "خلاق": ["خلاق", "creative", "هنری"],
            "منطقی": ["منطقی", "logical", "تحلیلی"]
        }
        
        text_lower = text.lower()
        for trait, words in keywords.items():
            if any(word in text_lower for word in words):
                traits.append(trait)
        
        return traits
    
    def complete_introduction(self) -> str:
        """تکمیل معرفی"""
        # ذخیره اطلاعات در پروفایل
        name = getattr(self, 'temp_name', 'دوست')
        interests = getattr(self, 'temp_interests', [])
        traits = getattr(self, 'temp_traits', [])
        
        self.user.complete_introduction(name, interests, traits)
        
        completion_messages = [
            f"عالی {name}! حالا که باهم آشنا شدیم، من دستیار شخصی و دوست تو هستم! 🦊💕\n\nهر وقت خواستی باهام حرف بزن، سوال بپرس، یا فقط چت کن! آماده‌ام! ✨",
            
            f"ممنون {name} عزیز! حالا که همدیگه رو می‌شناسیم، می‌تونیم شروع کنیم! 🦊\n\nمن اینجام تا کمکت کنم، باهات حرف بزنم، و دوستت باشم! چیکار می‌خوای بکنیم؟ 🎯",
            
            f"یه حس خوبی دارم راجع به دوستی ما {name}! 🦊💫\n\nحالا آماده‌ام برای هر کاری که بخوای! سوال، چت، کمک، هر چی! فقط بگو! ✨"
        ]
        
        return random.choice(completion_messages)
    
    def is_introduction_complete(self) -> bool:
        """آیا معرفی تکمیل شده؟"""
        return self.current_step >= len(self.introduction_steps)
