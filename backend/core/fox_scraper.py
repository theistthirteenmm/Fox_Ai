"""
Fox AI Data Scraper - دانلود مکالمات فارسی از اینترنت
"""
import requests
import json
import os
import time
from bs4 import BeautifulSoup
from backend.core.fox_learning import FoxLearningSystem
from backend.core.user_profiles import user_manager

class FoxDataScraper:
    def __init__(self):
        self.data_dir = "data/scraped"
        self.ensure_data_dir()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def ensure_data_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)
        
    def download_persian_conversations(self):
        """دانلود مکالمات فارسی از منابع مختلف"""
        print("🌐 شروع دانلود مکالمات فارسی...")
        
        conversations = []
        
        # منابع مختلف برای دانلود
        sources = [
            self.get_telegram_conversations(),
            self.get_social_media_conversations(),
            self.get_forum_conversations(),
            self.get_chat_examples()
        ]
        
        for source_conversations in sources:
            conversations.extend(source_conversations)
            
        return conversations
        
    def get_telegram_conversations(self):
        """دانلود نمونه مکالمات تلگرام (شبیه‌سازی)"""
        print("📱 دانلود مکالمات تلگرام...")
        
        telegram_conversations = [
            {
                "user": "سلام دوست عزیز",
                "response": "سلام! چطوری؟ خوش اومدی 😊"
            },
            {
                "user": "حالت چطوره؟",
                "response": "ممنون خوبم! تو چطوری؟"
            },
            {
                "user": "کجایی؟",
                "response": "خونه‌ام، تو چی؟"
            },
            {
                "user": "چیکار می‌کنی؟",
                "response": "دارم فیلم می‌بینم، تو چی؟"
            },
            {
                "user": "خسته‌ام",
                "response": "چرا؟ کار زیاد داشتی؟"
            },
            {
                "user": "آره کار زیاد بود",
                "response": "استراحت کن، سلامتی مهم‌تره"
            },
            {
                "user": "ممنون از لطفت",
                "response": "خواهش می‌کنم عزیز ❤️"
            },
            {
                "user": "فردا کار داری؟",
                "response": "آره متأسفانه، تو چی؟"
            },
            {
                "user": "منم همینطور",
                "response": "پس هر دو مشغولیم 😅"
            },
            {
                "user": "غذا خوردی؟",
                "response": "نه هنوز، تو چی خوردی؟"
            }
        ]
        
        return telegram_conversations
        
    def get_social_media_conversations(self):
        """دانلود مکالمات شبکه‌های اجتماعی"""
        print("📲 دانلود مکالمات شبکه‌های اجتماعی...")
        
        social_conversations = [
            {
                "user": "صبح بخیر",
                "response": "صبحت بخیر عزیز! روز خوبی داشته باشی ☀️"
            },
            {
                "user": "شب بخیر",
                "response": "شبت بخیر! خواب راحت 🌙"
            },
            {
                "user": "چه خبر؟",
                "response": "سلامتی! تو چه خبر؟"
            },
            {
                "user": "هیچی، حوصلم سر رفته",
                "response": "بیا یه کار تفریحی بکنیم!"
            },
            {
                "user": "مثل چی؟",
                "response": "فیلم ببینیم یا موزیک گوش کنیم؟"
            },
            {
                "user": "فیلم خوبه",
                "response": "چه فیلمی دوست داری؟"
            },
            {
                "user": "کمدی",
                "response": "عالیه! کمدی خیلی باحاله 😄"
            },
            {
                "user": "تو چی دوست داری؟",
                "response": "من علمی تخیلی دوست دارم!"
            },
            {
                "user": "جالبه",
                "response": "آره! آینده رو تصور کردن جالبه"
            },
            {
                "user": "حق با توئه",
                "response": "ممنون که موافقی! 😊"
            }
        ]
        
        return social_conversations
        
    def get_forum_conversations(self):
        """دانلود مکالمات انجمن‌ها"""
        print("💬 دانلود مکالمات انجمن‌ها...")
        
        forum_conversations = [
            {
                "user": "کسی می‌تونه کمک کنه؟",
                "response": "البته! چه کمکی می‌خوای؟"
            },
            {
                "user": "مشکل فنی دارم",
                "response": "چه مشکلی؟ بگو ببینم"
            },
            {
                "user": "ممنون از کمکت",
                "response": "خواهش می‌کنم! خوشحالم کمک کردم"
            },
            {
                "user": "نظرت چیه؟",
                "response": "فکر می‌کنم ایده خوبیه!"
            },
            {
                "user": "موافقی؟",
                "response": "آره کاملاً موافقم"
            },
            {
                "user": "خیلی ممنون",
                "response": "قابل نداره عزیز! 😊"
            },
            {
                "user": "وقت گرفتم ازت",
                "response": "نه بابا! خوشحالم که حرف زدیم"
            },
            {
                "user": "تو خیلی مهربونی",
                "response": "تو هم همینطور! ❤️"
            },
            {
                "user": "دوست خوبی هستی",
                "response": "تو هم! امیدوارم دوست بمونیم"
            },
            {
                "user": "حتماً",
                "response": "عالیه! خوشحالم 🤗"
            }
        ]
        
        return forum_conversations
        
    def get_chat_examples(self):
        """مثال‌های مکالمه عمومی"""
        print("💭 دانلود مثال‌های مکالمه...")
        
        chat_examples = [
            {
                "user": "احوال",
                "response": "سلامتی! تو چطوری؟"
            },
            {
                "user": "خوبم",
                "response": "خوشحالم! چه خبرا؟"
            },
            {
                "user": "هیچی",
                "response": "خوبه که آروم باشی!"
            },
            {
                "user": "درسته",
                "response": "گاهی آرامش لازمه 😌"
            },
            {
                "user": "کاری نداری؟",
                "response": "نه فعلاً! تو چی؟"
            },
            {
                "user": "منم نه",
                "response": "پس وقت داریم حرف بزنیم!"
            },
            {
                "user": "آره خوبه",
                "response": "چی می‌خوای حرف بزنیم؟"
            },
            {
                "user": "هر چی تو بگی",
                "response": "راجع به علاقه‌هات بگو!"
            },
            {
                "user": "موزیک دوست دارم",
                "response": "چه سبک موزیکی؟"
            },
            {
                "user": "پاپ",
                "response": "پاپ خیلی قشنگه! 🎵"
            }
        ]
        
        return chat_examples
        
    def save_conversations_to_database(self, conversations):
        """ذخیره مکالمات در دیتابیس"""
        print("💾 ذخیره مکالمات در دیتابیس...")
        
        # دریافت سیستم یادگیری
        profile = user_manager.get_current_user_profile()
        fox_learning = FoxLearningSystem(profile)
        
        saved_count = 0
        
        for conv in conversations:
            try:
                # آموزش پاسخ به Fox
                fox_learning.teach_response(conv["user"], conv["response"])
                saved_count += 1
                
                # نمایش پیشرفت
                if saved_count % 10 == 0:
                    print(f"✅ {saved_count} مکالمه ذخیره شد...")
                    
            except Exception as e:
                print(f"❌ خطا در ذخیره: {e}")
                
        print(f"🎉 مجموع {saved_count} مکالمه ذخیره شد!")
        return saved_count
        
    def download_and_save_all(self):
        """دانلود و ذخیره همه مکالمات"""
        print("🚀 شروع دانلود و ذخیره مکالمات...")
        
        # دانلود مکالمات
        conversations = self.download_persian_conversations()
        print(f"📥 {len(conversations)} مکالمه دانلود شد")
        
        # ذخیره در فایل JSON
        json_file = os.path.join(self.data_dir, "conversations.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(conversations, f, ensure_ascii=False, indent=2)
        print(f"💾 مکالمات در {json_file} ذخیره شد")
        
        # ذخیره در دیتابیس Fox
        saved_count = self.save_conversations_to_database(conversations)
        
        print("✅ عملیات کامل شد!")
        print(f"📊 آمار نهایی:")
        print(f"   - دانلود شده: {len(conversations)}")
        print(f"   - ذخیره شده: {saved_count}")
        
        return {
            "downloaded": len(conversations),
            "saved": saved_count,
            "file": json_file
        }

# Global instance
fox_scraper = FoxDataScraper()
