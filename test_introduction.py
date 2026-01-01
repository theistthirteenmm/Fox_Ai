#!/usr/bin/env python3
"""
Test Introduction System
"""
import sys
import os
sys.path.append('.')

from backend.core.user_profile import UserProfile
from backend.core.introduction import FoxIntroduction
from backend.core.memory import MemoryManager

def test_introduction():
    print("🦊 Testing Fox Introduction System")
    
    # Remove existing profile
    if os.path.exists("data/user_profile.json"):
        os.remove("data/user_profile.json")
    
    # Initialize
    memory = MemoryManager()
    profile = UserProfile(memory.db)
    intro = FoxIntroduction(profile)
    
    print(f"First time user: {profile.is_first_time()}")
    
    # Start introduction
    print("\n" + "="*50)
    message = intro.start_introduction()
    print("Fox:", message)
    
    # Simulate conversation
    responses = [
        "سلام",      # greeting response
        "حامد",      # name response  
        "برنامه‌نویسی، موسیقی",  # interests response
        "کنجکاو و شوخ‌طبع"      # personality response
    ]
    
    for response in responses:
        print(f"\nUser: {response}")
        fox_response = intro.process_response(response)
        print(f"Fox: {fox_response}")
        
        if intro.is_introduction_complete():
            print("\n🎉 Introduction completed!")
            break
    
    # Check profile
    print(f"\nProfile after introduction:")
    print(f"Name: {profile.get_name()}")
    print(f"Interests: {profile.profile['interests']}")
    print(f"Traits: {profile.profile['personality_traits']}")
    print(f"Relationship level: {profile.get_relationship_status()}")

if __name__ == "__main__":
    test_introduction()
