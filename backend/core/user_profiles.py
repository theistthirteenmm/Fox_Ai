"""
Multi-User Profile System for Fox AI
"""
import json
import os
from datetime import datetime
from typing import Dict, Optional, List

class UserProfileManager:
    def __init__(self, data_dir: str = "data/profiles"):
        self.data_dir = data_dir
        self.ensure_data_dir()
        self.current_user = "حامد"  # Default main user
        self.main_user = "حامد"
        
    def ensure_data_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)
        
    def get_user_file(self, username: str) -> str:
        return os.path.join(self.data_dir, f"{username}_profile.json")
        
    def create_user_profile(self, username: str, relationship_to_hamed: str = "دوست") -> Dict:
        """Create new user profile"""
        profile = {
            "name": username,
            "relationship_to_hamed": relationship_to_hamed,
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "preferences": {
                "personality_style": "دوستانه",
                "response_length": "متوسط",
                "use_emoji": True,
                "formality_level": "غیررسمی"
            },
            "characteristics": {
                "interests": [],
                "personality_traits": [],
                "communication_style": "طبیعی"
            },
            "conversation_stats": {
                "total_messages": 0,
                "favorite_topics": [],
                "common_phrases": []
            },
            "learning_data": {
                "custom_responses": {},
                "learned_facts": {},
                "personal_info": {}
            }
        }
        
        # Save profile
        with open(self.get_user_file(username), 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
            
        return profile
        
    def get_user_profile(self, username: str) -> Optional[Dict]:
        """Get user profile"""
        file_path = self.get_user_file(username)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
        
    def update_user_profile(self, username: str, updates: Dict):
        """Update user profile"""
        profile = self.get_user_profile(username)
        if profile:
            profile.update(updates)
            profile["last_active"] = datetime.now().isoformat()
            
            with open(self.get_user_file(username), 'w', encoding='utf-8') as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
                
    def detect_new_user(self, message: str) -> Optional[str]:
        """Detect if someone is introducing themselves"""
        message_lower = message.lower().strip()
        
        # الگوهای دقیق معرفی
        if "اسم من" in message_lower:
            # "اسم من علی هست" -> علی
            parts = message_lower.split("اسم من")
            if len(parts) > 1:
                name_part = parts[1].strip()
                words = name_part.split()
                if words and words[0] not in ["هست", "است", "میشه", "کی", "چی"]:
                    return words[0].strip("،.!؟")
                    
        elif "نام من" in message_lower:
            # "نام من سارا است" -> سارا  
            parts = message_lower.split("نام من")
            if len(parts) > 1:
                name_part = parts[1].strip()
                words = name_part.split()
                if words and words[0] not in ["هست", "است", "میشه", "کی", "چی"]:
                    return words[0].strip("،.!؟")
                    
        elif "هستم" in message_lower and "من" in message_lower:
            # "من رضا هستم" -> رضا
            # پیدا کردن کلمه بین "من" و "هستم"
            words = message_lower.split()
            try:
                man_index = words.index("من")
                hastam_index = words.index("هستم")
                if hastam_index > man_index + 1:
                    # کلمه بین "من" و "هستم"
                    name = words[man_index + 1]
                    if name not in ["یه", "یک", "کی", "چی", "خیلی"]:
                        return name.strip("،.!؟")
            except ValueError:
                pass
                    
        elif "صدام کن" in message_lower:
            # "صدام کن مهدی" -> مهدی
            parts = message_lower.split("صدام کن")
            if len(parts) > 1:
                name_part = parts[1].strip()
                if name_part and name_part not in ["من", "منو"]:
                    return name_part.strip("،.!؟")
        
        return None
        
    def switch_user(self, username: str):
        """Switch current user"""
        self.current_user = username
        
    def get_current_user_profile(self) -> Dict:
        """Get current user's profile"""
        profile = self.get_user_profile(self.current_user)
        if not profile:
            # Create profile for main user if doesn't exist
            if self.current_user == self.main_user:
                profile = self.create_user_profile(self.main_user, "کاربر اصلی")
            else:
                profile = self.create_user_profile(self.current_user)
        return profile
        
    def get_all_users(self) -> List[str]:
        """Get list of all users"""
        users = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('_profile.json'):
                username = filename.replace('_profile.json', '')
                users.append(username)
        return users
        
    def get_relationship_context(self, username: str) -> str:
        """Get relationship context for AI responses"""
        profile = self.get_user_profile(username)
        if not profile:
            return "دوست جدید"
            
        relationship = profile.get("relationship_to_hamed", "دوست")
        
        if username == self.main_user:
            return "کاربر اصلی حامد"
        else:
            return f"{relationship} حامد"
            
    def ask_for_relationship(self, username: str) -> str:
        """Generate question to ask about relationship with Hamed"""
        return f"سلام {username}! خوشحالم که آشناتون شدم 😊\nبرای اینکه بهتر باهاتون ارتباط برقرار کنم، می‌تونید بگید نسبتتون با حامد چیه؟ (مثلاً: دوست، همکار، خانواده، ...)"
        
    def update_conversation_stats(self, username: str, message: str):
        """Update conversation statistics"""
        profile = self.get_user_profile(username)
        if profile:
            stats = profile.get("conversation_stats", {})
            stats["total_messages"] = stats.get("total_messages", 0) + 1
            stats["last_message_time"] = datetime.now().isoformat()
            
            # Update profile
            profile["conversation_stats"] = stats
            self.update_user_profile(username, profile)

# Global instance
user_manager = UserProfileManager()
