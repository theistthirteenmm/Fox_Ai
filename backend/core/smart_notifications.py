"""
🔔 Smart Notifications - اعلان‌های هوشمند Fox
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import asyncio
from dataclasses import dataclass

@dataclass
class Notification:
    id: str
    title: str
    message: str
    type: str  # reminder, suggestion, follow_up, achievement
    priority: int  # 1=low, 2=medium, 3=high
    scheduled_time: str
    created_time: str
    is_read: bool = False
    is_sent: bool = False
    user_id: str = "default"

class SmartNotifications:
    def __init__(self):
        self.notifications_file = "data/notifications/notifications.json"
        self.settings_file = "data/notifications/settings.json"
        self.load_data()
        
    def load_data(self):
        """بارگذاری اعلان‌ها و تنظیمات"""
        # بارگذاری اعلان‌ها
        if os.path.exists(self.notifications_file):
            with open(self.notifications_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.notifications = [Notification(**notif) for notif in data]
        else:
            self.notifications = []
            
        # بارگذاری تنظیمات
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                "enabled": True,
                "quiet_hours": {"start": "22:00", "end": "08:00"},
                "notification_types": {
                    "reminders": True,
                    "suggestions": True,
                    "follow_ups": True,
                    "achievements": True
                },
                "frequency": {
                    "daily_summary": True,
                    "weekly_insights": True,
                    "learning_reminders": True
                }
            }
    
    def save_data(self):
        """ذخیره اعلان‌ها و تنظیمات"""
        os.makedirs(os.path.dirname(self.notifications_file), exist_ok=True)
        
        # ذخیره اعلان‌ها
        notifications_data = [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "type": n.type,
                "priority": n.priority,
                "scheduled_time": n.scheduled_time,
                "created_time": n.created_time,
                "is_read": n.is_read,
                "is_sent": n.is_sent,
                "user_id": n.user_id
            }
            for n in self.notifications
        ]
        
        with open(self.notifications_file, 'w', encoding='utf-8') as f:
            json.dump(notifications_data, f, ensure_ascii=False, indent=2)
            
        # ذخیره تنظیمات
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)
    
    def create_notification(self, title: str, message: str, notif_type: str, 
                          priority: int = 2, schedule_after_minutes: int = 0) -> str:
        """ایجاد اعلان جدید"""
        notification_id = f"notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        scheduled_time = datetime.now() + timedelta(minutes=schedule_after_minutes)
        
        notification = Notification(
            id=notification_id,
            title=title,
            message=message,
            type=notif_type,
            priority=priority,
            scheduled_time=scheduled_time.isoformat(),
            created_time=datetime.now().isoformat()
        )
        
        self.notifications.append(notification)
        self.save_data()
        
        return notification_id
    
    def create_follow_up(self, original_question: str, context: Dict = None):
        """ایجاد follow-up بر اساس سوال قبلی"""
        follow_ups = [
            f"آیا پاسخ من در مورد '{original_question[:50]}...' کاملاً واضح بود؟",
            f"سوال دیگه‌ای در مورد '{original_question[:30]}...' داری؟",
            f"آیا می‌خوای بیشتر در مورد این موضوع صحبت کنیم؟",
            f"چطور می‌تونم بهتر کمکت کنم؟"
        ]
        
        import random
        message = random.choice(follow_ups)
        
        self.create_notification(
            title="🤔 سوال تکمیلی",
            message=message,
            notif_type="follow_up",
            priority=1,
            schedule_after_minutes=30  # 30 دقیقه بعد
        )
    
    def create_learning_reminder(self, topic: str):
        """یادآوری یادگیری"""
        reminders = [
            f"بیا یه چیز جدید در مورد {topic} یاد بگیریم!",
            f"وقتشه که دانش {topic}ت رو تقویت کنی",
            f"چه نظری داری یه تمرین {topic} انجام بدیم؟"
        ]
        
        import random
        message = random.choice(reminders)
        
        self.create_notification(
            title="📚 یادآوری یادگیری",
            message=message,
            notif_type="reminder",
            priority=2,
            schedule_after_minutes=60  # 1 ساعت بعد
        )
    
    def create_daily_summary(self, stats: Dict):
        """خلاصه روزانه"""
        conversations = stats.get('conversations_today', 0)
        topics = stats.get('topics_discussed', [])
        
        if conversations > 0:
            message = f"امروز {conversations} مکالمه داشتیم"
            if topics:
                message += f" و در مورد {', '.join(topics[:3])} صحبت کردیم"
            message += ". فردا هم منتظرتم! 🦊"
            
            # برنامه‌ریزی برای فردا صبح
            tomorrow_morning = datetime.now().replace(hour=9, minute=0, second=0) + timedelta(days=1)
            
            notification = Notification(
                id=f"daily_{datetime.now().strftime('%Y%m%d')}",
                title="📊 خلاصه امروز",
                message=message,
                type="summary",
                priority=2,
                scheduled_time=tomorrow_morning.isoformat(),
                created_time=datetime.now().isoformat()
            )
            
            self.notifications.append(notification)
            self.save_data()
    
    def create_achievement_notification(self, achievement: str, description: str):
        """اعلان دستاورد"""
        self.create_notification(
            title=f"🏆 دستاورد جدید: {achievement}",
            message=description,
            notif_type="achievement",
            priority=3,
            schedule_after_minutes=0  # فوری
        )
    
    def get_pending_notifications(self) -> List[Notification]:
        """دریافت اعلان‌های در انتظار"""
        now = datetime.now()
        pending = []
        
        for notification in self.notifications:
            if (not notification.is_sent and 
                datetime.fromisoformat(notification.scheduled_time) <= now and
                self.should_send_notification(notification)):
                pending.append(notification)
                
        return pending
    
    def should_send_notification(self, notification: Notification) -> bool:
        """بررسی اینکه آیا اعلان باید ارسال شود"""
        if not self.settings["enabled"]:
            return False
            
        if not self.settings["notification_types"].get(notification.type, True):
            return False
            
        # بررسی ساعات سکوت
        now = datetime.now()
        quiet_start = datetime.strptime(self.settings["quiet_hours"]["start"], "%H:%M").time()
        quiet_end = datetime.strptime(self.settings["quiet_hours"]["end"], "%H:%M").time()
        
        current_time = now.time()
        
        if quiet_start > quiet_end:  # شب تا صبح
            if current_time >= quiet_start or current_time <= quiet_end:
                return False
        else:  # روز عادی
            if quiet_start <= current_time <= quiet_end:
                return False
                
        return True
    
    def mark_as_sent(self, notification_id: str):
        """علامت‌گذاری به عنوان ارسال شده"""
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.is_sent = True
                break
        self.save_data()
    
    def mark_as_read(self, notification_id: str):
        """علامت‌گذاری به عنوان خوانده شده"""
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.is_read = True
                break
        self.save_data()
    
    def get_unread_notifications(self) -> List[Notification]:
        """دریافت اعلان‌های خوانده نشده"""
        return [n for n in self.notifications if n.is_sent and not n.is_read]
    
    def cleanup_old_notifications(self, days: int = 30):
        """پاک‌سازی اعلان‌های قدیمی"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        self.notifications = [
            n for n in self.notifications 
            if datetime.fromisoformat(n.created_time) > cutoff_date
        ]
        
        self.save_data()
    
    def update_settings(self, new_settings: Dict):
        """آپدیت تنظیمات"""
        self.settings.update(new_settings)
        self.save_data()
    
    def get_notification_stats(self) -> Dict:
        """آمار اعلان‌ها"""
        total = len(self.notifications)
        sent = len([n for n in self.notifications if n.is_sent])
        read = len([n for n in self.notifications if n.is_read])
        pending = len(self.get_pending_notifications())
        
        return {
            "total": total,
            "sent": sent,
            "read": read,
            "pending": pending,
            "read_rate": (read / sent * 100) if sent > 0 else 0
        }

# نمونه استفاده
smart_notifications = SmartNotifications()
