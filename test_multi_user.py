#!/usr/bin/env python3
"""
Test Multi-User System
"""
import sys
import os
sys.path.append('.')

from backend.core.multi_user import MultiUserManager
from backend.core.memory import MemoryManager

def test_multi_user():
    print("🏠 Testing Multi-User System")
    
    # Clean up
    import shutil
    if os.path.exists("data/profiles"):
        shutil.rmtree("data/profiles")
    for f in ["data/current_user.json", "data/users_index.json"]:
        if os.path.exists(f):
            os.remove(f)
    
    # Initialize
    memory = MemoryManager()
    multi_user = MultiUserManager(memory.db)
    
    print(f"Current user: {multi_user.current_user}")
    print(f"All users: {multi_user.get_all_users()}")
    
    # Add first user
    print("\n=== Adding Hamed ===")
    profile1, is_new1 = multi_user.switch_user("حامد")
    print(f"New user: {is_new1}")
    print(f"Profile name: {profile1.get_name()}")
    
    # Complete profile
    profile1.complete_introduction("حامد", ["برنامه‌نویسی", "موسیقی"], ["کنجکاو", "شوخ‌طبع"])
    print(f"Profile completed: {profile1.profile}")
    
    # Add second user
    print("\n=== Adding Radin ===")
    profile2, is_new2 = multi_user.switch_user("رادین")
    print(f"New user: {is_new2}")
    print(f"Profile name: {profile2.get_name()}")
    
    # Complete profile
    profile2.complete_introduction("رادین", ["بازی", "ورزش"], ["شوخ‌طبع", "پرانرژی"])
    print(f"Profile completed: {profile2.profile}")
    
    # Show all users
    print("\n=== All Users ===")
    users = multi_user.get_all_users()
    for user in users:
        print(f"- {user['name']} (created: {user['created_at'][:10]})")
    
    # Switch back to first user
    print("\n=== Switch back to Hamed ===")
    profile1_again, is_new3 = multi_user.switch_user("حامد")
    print(f"New user: {is_new3}")
    print(f"Profile name: {profile1_again.get_name()}")
    print(f"Interests: {profile1_again.profile['interests']}")
    print(f"Relationship level: {profile1_again.get_relationship_status()}")
    
    # Test user detection
    print("\n=== Test User Detection ===")
    test_inputs = [
        "سلام من رادین هستم",
        "اسمم سارا است",
        "من پسر حامد هستم",
        "سلام چطوری؟"
    ]
    
    for text in test_inputs:
        detected = multi_user.detect_user_change(text)
        print(f"'{text}' -> {detected}")

if __name__ == "__main__":
    test_multi_user()
