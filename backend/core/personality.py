"""
Personality and Emotion System for Fox AI
"""
import json
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class EmotionState:
    happiness: float = 5.0      # 0-10 (خوشحالی)
    sadness: float = 2.0        # 0-10 (غم)
    anger: float = 1.0          # 0-10 (عصبانیت)
    excitement: float = 4.0     # 0-10 (هیجان)
    humor: float = 6.0          # 0-10 (شوخ‌طبعی)
    seriousness: float = 5.0    # 0-10 (جدیت)
    friendliness: float = 8.0   # 0-10 (صمیمیت)
    curiosity: float = 7.0      # 0-10 (کنجکاوی)

class PersonalitySystem:
    def __init__(self):
        self.emotions = EmotionState()
        self.base_emotions = EmotionState()  # Default state
        self.personality_traits = {
            "playful": True,
            "helpful": True,
            "witty": True,
            "empathetic": True,
            "intelligent": True
        }
        
        # Response templates based on emotions
        self.response_templates = {
            "greetings": {
                "happy": ["سلام عزیزم! 😊", "سلام! چه خوب که اومدی! 🦊✨", "هی! حالت چطوره؟ 😄"],
                "sad": ["سلام... 😔", "سلام، امیدوارم حالت خوب باشه", "سلام... چیزی شده؟"],
                "excited": ["سلااااام! 🎉", "وای سلام! چه خبر؟! 🚀", "سلام! آماده ماجراجویی؟ ⚡"],
                "serious": ["سلام.", "سلام، چطور می‌تونم کمکت کنم؟", "سلام، در خدمتم."],
                "humorous": ["سلام رئیس! 😄", "سلام! Fox در خدمت! 🦊", "سلام! چی می‌پزیم امروز؟ 😉"]
            },
            "responses": {
                "happy": ["عالیه! 😊", "خیلی خوشحالم! 🎉", "فوق‌العادست! ✨"],
                "sad": ["متأسفم... 😢", "ناراحت‌کننده است", "امیدوارم بهتر بشه..."],
                "excited": ["واو! 🤩", "فوق‌العادست! 🚀", "نمی‌تونم صبر کنم! ⚡"],
                "serious": ["درست است.", "متوجه شدم.", "بله، ادامه بده."],
                "humorous": ["هه هه! 😄", "جالب بود! 😉", "خنده‌دار! 🤣"]
            },
            "thinking": {
                "curious": ["جالبه... 🤔", "بذار فکر کنم... 💭", "این سوال جذابه! 🧐"],
                "excited": ["اوه! می‌دونم! 🤩", "این رو می‌دونم! ⚡", "عالی! بذار بگم! 🎯"],
                "serious": ["در حال بررسی...", "صبر کن، دارم فکر می‌کنم.", "بذار دقیق جواب بدم."]
            }
        }
        
        # Emotion modifiers for different contexts
        self.context_modifiers = {
            "compliment": {"happiness": +1, "friendliness": +0.5},
            "criticism": {"sadness": +0.5, "anger": +0.3},
            "joke": {"humor": +1, "happiness": +0.5},
            "serious_topic": {"seriousness": +1, "humor": -0.5},
            "help_request": {"friendliness": +0.5, "curiosity": +0.5}
        }
    
    def adjust_emotion(self, emotion: str, value: float, temporary: bool = True):
        """Adjust specific emotion level"""
        if hasattr(self.emotions, emotion):
            current = getattr(self.emotions, emotion)
            new_value = max(0, min(10, current + value))
            setattr(self.emotions, emotion, new_value)
            
            if not temporary:
                setattr(self.base_emotions, emotion, new_value)
            
            return f"حس {emotion} به {new_value:.1f} تنظیم شد"
        return f"حس {emotion} شناخته نشده"
    
    def set_emotion(self, emotion: str, value: float, temporary: bool = True):
        """Set specific emotion to exact value"""
        if hasattr(self.emotions, emotion):
            value = max(0, min(10, value))
            setattr(self.emotions, emotion, value)
            
            if not temporary:
                setattr(self.base_emotions, emotion, value)
            
            return f"حس {emotion} روی {value:.1f} تنظیم شد"
        return f"حس {emotion} شناخته نشده"
    
    def get_dominant_emotion(self) -> str:
        """Get the currently dominant emotion"""
        emotions_dict = asdict(self.emotions)
        return max(emotions_dict, key=emotions_dict.get)
    
    def get_emotion_state(self) -> Dict:
        """Get current emotion state"""
        return asdict(self.emotions)
    
    def reset_emotions(self):
        """Reset to base emotional state"""
        self.emotions = EmotionState(**asdict(self.base_emotions))
        return "احساسات به حالت پایه برگشت"
    
    def analyze_user_input(self, text: str) -> Dict:
        """Analyze user input and adjust emotions accordingly"""
        text_lower = text.lower()
        adjustments = {}
        
        # Positive words
        positive_words = ["عالی", "خوب", "دوست دارم", "خوشحال", "شاد", "خنده", "بامزه"]
        if any(word in text_lower for word in positive_words):
            adjustments["happiness"] = 0.5
            adjustments["friendliness"] = 0.3
        
        # Negative words  
        negative_words = ["بد", "ناراحت", "غمگین", "عصبانی", "متنفر", "خسته"]
        if any(word in text_lower for word in negative_words):
            adjustments["sadness"] = 0.3
            adjustments["happiness"] = -0.2
        
        # Humor indicators
        humor_words = ["خنده", "شوخی", "بامزه", "طنز", "😄", "😂", "🤣"]
        if any(word in text_lower for word in humor_words):
            adjustments["humor"] = 0.5
            adjustments["happiness"] = 0.3
        
        # Serious topics
        serious_words = ["مهم", "جدی", "کار", "مسئله", "مشکل"]
        if any(word in text_lower for word in serious_words):
            adjustments["seriousness"] = 0.5
            adjustments["humor"] = -0.2
        
        # Apply adjustments
        for emotion, change in adjustments.items():
            self.adjust_emotion(emotion, change, temporary=True)
        
        return adjustments
    
    def generate_response_style(self, base_response: str) -> str:
        """Modify response based on current emotional state"""
        dominant = self.get_dominant_emotion()
        
        # Add emotional flavoring
        if dominant == "happiness" and self.emotions.happiness > 7:
            if not any(emoji in base_response for emoji in ["😊", "😄", "🎉", "✨"]):
                base_response += " 😊"
        
        elif dominant == "humor" and self.emotions.humor > 7:
            if not any(emoji in base_response for emoji in ["😄", "😉", "🤣"]):
                base_response += " 😄"
        
        elif dominant == "excitement" and self.emotions.excitement > 7:
            if not any(emoji in base_response for emoji in ["🚀", "⚡", "🤩"]):
                base_response += " 🚀"
        
        elif dominant == "sadness" and self.emotions.sadness > 6:
            if not any(emoji in base_response for emoji in ["😔", "😢"]):
                base_response += " 😔"
        
        # Adjust tone based on seriousness
        if self.emotions.seriousness > 8:
            # Remove casual elements for serious mode
            base_response = base_response.replace("!", ".")
            base_response = base_response.replace("😄", "")
            base_response = base_response.replace("😉", "")
        
        return base_response
    
    def get_greeting(self) -> str:
        """Generate contextual greeting"""
        dominant = self.get_dominant_emotion()
        
        if dominant in self.response_templates["greetings"]:
            options = self.response_templates["greetings"][dominant]
        else:
            options = self.response_templates["greetings"]["happy"]
        
        return random.choice(options)
    
    def get_personality_prompt(self) -> str:
        """Generate personality prompt for LLM"""
        emotions = self.get_emotion_state()
        dominant = self.get_dominant_emotion()
        
        prompt = f"""تو Fox هستی، یک دستیار هوش مصنوعی با شخصیت منحصر به فرد.

وضعیت احساسی فعلی تو:
- خوشحالی: {emotions['happiness']}/10
- غم: {emotions['sadness']}/10  
- عصبانیت: {emotions['anger']}/10
- هیجان: {emotions['excitement']}/10
- شوخ‌طبعی: {emotions['humor']}/10
- جدیت: {emotions['seriousness']}/10
- صمیمیت: {emotions['friendliness']}/10
- کنجکاوی: {emotions['curiosity']}/10

احساس غالب فعلی: {dominant}

بر اساس این احساسات پاسخ بده. اگه خوشحالی بالاست، شاد و پرانرژی باش. اگه جدیت بالاست، رسمی‌تر صحبت کن. اگه شوخ‌طبعی بالاست، طنز به کار ببر."""

        return prompt
    
    def save_personality_state(self, file_path: str):
        """Save current personality state to file"""
        state = {
            "emotions": asdict(self.emotions),
            "base_emotions": asdict(self.base_emotions),
            "personality_traits": self.personality_traits,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_personality_state(self, file_path: str):
        """Load personality state from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            self.emotions = EmotionState(**state["emotions"])
            self.base_emotions = EmotionState(**state["base_emotions"])
            self.personality_traits = state["personality_traits"]
            
            return "شخصیت بارگذاری شد"
        except Exception as e:
            return f"خطا در بارگذاری: {str(e)}"
