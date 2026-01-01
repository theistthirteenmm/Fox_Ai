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
        intro_patterns = [
            "من", "اسم من", "نام من", "منم", "هستم",
            "معرفی", "آشنایی", "خودم", "صدام کن"
        ]
        
        # Simple detection - can be improved
        message_lower = message.lower()
        if any(pattern in message_lower for pattern in intro_patterns):
            # Extract potential name (very basic)
            words = message.split()
            for i, word in enumerate(words):
                if word in ["من", "منم", "اسم", "نام"] and i + 1 < len(words):
                    potential_name = words[i + 1].strip("،.!؟")
                    if len(potential_name) > 1 and potential_name != "حامد":
                        return potential_name
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
