"""
📊 Analytics Dashboard - داشبورد تحلیلی Fox
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict, Counter
import calendar

class AnalyticsDashboard:
    def __init__(self):
        self.analytics_file = "data/analytics/dashboard_data.json"
        self.load_analytics()
        
    def load_analytics(self):
        """بارگذاری داده‌های تحلیلی"""
        if os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'r', encoding='utf-8') as f:
                self.analytics = json.load(f)
        else:
            self.analytics = {
                "daily_stats": {},
                "weekly_stats": {},
                "monthly_stats": {},
                "user_behavior": {},
                "performance_metrics": {},
                "learning_progress": {}
            }
    
    def save_analytics(self):
        """ذخیره داده‌های تحلیلی"""
        os.makedirs(os.path.dirname(self.analytics_file), exist_ok=True)
        with open(self.analytics_file, 'w', encoding='utf-8') as f:
            json.dump(self.analytics, f, ensure_ascii=False, indent=2)
    
    def record_conversation(self, user_input: str, ai_response: str, 
                          response_time: float, topic: str = None):
        """ثبت مکالمه برای تحلیل"""
        today = datetime.now().strftime("%Y-%m-%d")
        hour = datetime.now().hour
        
        # آمار روزانه
        if today not in self.analytics["daily_stats"]:
            self.analytics["daily_stats"][today] = {
                "conversations": 0,
                "total_response_time": 0,
                "topics": {},
                "hourly_distribution": {},
                "user_satisfaction": [],
                "word_count": {"user": 0, "ai": 0}
            }
        
        daily = self.analytics["daily_stats"][today]
        daily["conversations"] += 1
        daily["total_response_time"] += response_time
        daily["hourly_distribution"][str(hour)] = daily["hourly_distribution"].get(str(hour), 0) + 1
        daily["word_count"]["user"] += len(user_input.split())
        daily["word_count"]["ai"] += len(ai_response.split())
        
        if topic:
            daily["topics"][topic] = daily["topics"].get(topic, 0) + 1
        
        # آمار هفتگی
        week_key = datetime.now().strftime("%Y-W%U")
        if week_key not in self.analytics["weekly_stats"]:
            self.analytics["weekly_stats"][week_key] = {
                "conversations": 0,
                "avg_response_time": 0,
                "top_topics": {},
                "active_days": set()
            }
        
        weekly = self.analytics["weekly_stats"][week_key]
        weekly["conversations"] += 1
        weekly["active_days"] = list(set(weekly.get("active_days", [])) | {today})
        
        if topic:
            weekly["top_topics"][topic] = weekly["top_topics"].get(topic, 0) + 1
        
        # آمار ماهانه
        month_key = datetime.now().strftime("%Y-%m")
        if month_key not in self.analytics["monthly_stats"]:
            self.analytics["monthly_stats"][month_key] = {
                "conversations": 0,
                "total_days_active": 0,
                "learning_sessions": 0,
                "achievements_unlocked": 0
            }
        
        monthly = self.analytics["monthly_stats"][month_key]
        monthly["conversations"] += 1
        
        self.save_analytics()
    
    def record_learning_session(self, topic: str, success: bool, duration: int):
        """ثبت جلسه یادگیری"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if "learning_progress" not in self.analytics:
            self.analytics["learning_progress"] = {}
            
        if today not in self.analytics["learning_progress"]:
            self.analytics["learning_progress"][today] = {
                "sessions": [],
                "total_duration": 0,
                "success_rate": 0
            }
        
        session = {
            "topic": topic,
            "success": success,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        
        self.analytics["learning_progress"][today]["sessions"].append(session)
        self.analytics["learning_progress"][today]["total_duration"] += duration
        
        # محاسبه نرخ موفقیت
        sessions = self.analytics["learning_progress"][today]["sessions"]
        success_count = sum(1 for s in sessions if s["success"])
        self.analytics["learning_progress"][today]["success_rate"] = success_count / len(sessions) * 100
        
        self.save_analytics()
    
    def get_dashboard_data(self, period: str = "week") -> Dict:
        """دریافت داده‌های داشبورد"""
        now = datetime.now()
        
        if period == "today":
            return self._get_today_stats()
        elif period == "week":
            return self._get_week_stats()
        elif period == "month":
            return self._get_month_stats()
        else:
            return self._get_overall_stats()
    
    def _get_today_stats(self) -> Dict:
        """آمار امروز"""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_data = self.analytics["daily_stats"].get(today, {})
        
        conversations = daily_data.get("conversations", 0)
        avg_response_time = 0
        if conversations > 0:
            avg_response_time = daily_data.get("total_response_time", 0) / conversations
        
        return {
            "period": "امروز",
            "conversations": conversations,
            "avg_response_time": round(avg_response_time, 2),
            "top_topics": dict(sorted(daily_data.get("topics", {}).items(), 
                                    key=lambda x: x[1], reverse=True)[:5]),
            "hourly_activity": daily_data.get("hourly_distribution", {}),
            "word_stats": daily_data.get("word_count", {"user": 0, "ai": 0})
        }
    
    def _get_week_stats(self) -> Dict:
        """آمار هفته"""
        # 7 روز گذشته
        week_data = {"conversations": 0, "topics": {}, "daily_breakdown": {}}
        
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            daily = self.analytics["daily_stats"].get(date, {})
            
            week_data["conversations"] += daily.get("conversations", 0)
            week_data["daily_breakdown"][date] = daily.get("conversations", 0)
            
            # ترکیب موضوعات
            for topic, count in daily.get("topics", {}).items():
                week_data["topics"][topic] = week_data["topics"].get(topic, 0) + count
        
        return {
            "period": "هفته گذشته",
            "conversations": week_data["conversations"],
            "avg_daily": round(week_data["conversations"] / 7, 1),
            "top_topics": dict(sorted(week_data["topics"].items(), 
                                    key=lambda x: x[1], reverse=True)[:5]),
            "daily_breakdown": week_data["daily_breakdown"],
            "trend": self._calculate_trend("week")
        }
    
    def _get_month_stats(self) -> Dict:
        """آمار ماه"""
        current_month = datetime.now().strftime("%Y-%m")
        month_data = {"conversations": 0, "topics": {}, "weekly_breakdown": {}}
        
        # 4 هفته گذشته
        for week in range(4):
            week_start = datetime.now() - timedelta(weeks=week)
            week_conversations = 0
            
            for day in range(7):
                date = (week_start - timedelta(days=day)).strftime("%Y-%m-%d")
                daily = self.analytics["daily_stats"].get(date, {})
                week_conversations += daily.get("conversations", 0)
                
                # ترکیب موضوعات
                for topic, count in daily.get("topics", {}).items():
                    month_data["topics"][topic] = month_data["topics"].get(topic, 0) + count
            
            month_data["conversations"] += week_conversations
            month_data["weekly_breakdown"][f"هفته {week+1}"] = week_conversations
        
        return {
            "period": "ماه گذشته",
            "conversations": month_data["conversations"],
            "avg_weekly": round(month_data["conversations"] / 4, 1),
            "top_topics": dict(sorted(month_data["topics"].items(), 
                                    key=lambda x: x[1], reverse=True)[:5]),
            "weekly_breakdown": month_data["weekly_breakdown"],
            "learning_progress": self._get_learning_stats()
        }
    
    def _get_overall_stats(self) -> Dict:
        """آمار کلی"""
        total_conversations = 0
        all_topics = {}
        first_conversation = None
        
        for date, daily in self.analytics["daily_stats"].items():
            total_conversations += daily.get("conversations", 0)
            
            if not first_conversation or date < first_conversation:
                first_conversation = date
                
            for topic, count in daily.get("topics", {}).items():
                all_topics[topic] = all_topics.get(topic, 0) + count
        
        # محاسبه روزهای فعال
        active_days = len([d for d, data in self.analytics["daily_stats"].items() 
                          if data.get("conversations", 0) > 0])
        
        return {
            "period": "کل دوره",
            "total_conversations": total_conversations,
            "active_days": active_days,
            "avg_per_day": round(total_conversations / max(active_days, 1), 1),
            "first_conversation": first_conversation,
            "top_topics": dict(sorted(all_topics.items(), 
                                    key=lambda x: x[1], reverse=True)[:10]),
            "user_engagement": self._calculate_engagement()
        }
    
    def _calculate_trend(self, period: str) -> str:
        """محاسبه روند"""
        if period == "week":
            # مقایسه این هفته با هفته قبل
            this_week = 0
            last_week = 0
            
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                this_week += self.analytics["daily_stats"].get(date, {}).get("conversations", 0)
                
                date_last_week = (datetime.now() - timedelta(days=i+7)).strftime("%Y-%m-%d")
                last_week += self.analytics["daily_stats"].get(date_last_week, {}).get("conversations", 0)
            
            if last_week == 0:
                return "جدید"
            
            change = ((this_week - last_week) / last_week) * 100
            
            if change > 10:
                return f"📈 افزایش {change:.1f}%"
            elif change < -10:
                return f"📉 کاهش {abs(change):.1f}%"
            else:
                return "📊 ثابت"
        
        return "نامشخص"
    
    def _get_learning_stats(self) -> Dict:
        """آمار یادگیری"""
        total_sessions = 0
        total_duration = 0
        success_count = 0
        
        for date, data in self.analytics.get("learning_progress", {}).items():
            sessions = data.get("sessions", [])
            total_sessions += len(sessions)
            total_duration += data.get("total_duration", 0)
            success_count += sum(1 for s in sessions if s.get("success", False))
        
        return {
            "total_sessions": total_sessions,
            "total_duration_minutes": total_duration,
            "success_rate": round(success_count / max(total_sessions, 1) * 100, 1),
            "avg_session_duration": round(total_duration / max(total_sessions, 1), 1)
        }
    
    def _calculate_engagement(self) -> Dict:
        """محاسبه میزان تعامل"""
        # محاسبه بر اساس تعداد روزهای فعال، طول مکالمات، و تنوع موضوعات
        active_days = len([d for d, data in self.analytics["daily_stats"].items() 
                          if data.get("conversations", 0) > 0])
        
        total_conversations = sum(data.get("conversations", 0) 
                                for data in self.analytics["daily_stats"].values())
        
        unique_topics = set()
        for data in self.analytics["daily_stats"].values():
            unique_topics.update(data.get("topics", {}).keys())
        
        # امتیاز تعامل (0-100)
        engagement_score = min(100, 
            (active_days * 2) +  # روزهای فعال
            (len(unique_topics) * 5) +  # تنوع موضوعات
            min(total_conversations, 50)  # تعداد مکالمات (حداکثر 50 امتیاز)
        )
        
        if engagement_score >= 80:
            level = "عالی 🌟"
        elif engagement_score >= 60:
            level = "خوب 👍"
        elif engagement_score >= 40:
            level = "متوسط 📊"
        else:
            level = "کم 📉"
        
        return {
            "score": engagement_score,
            "level": level,
            "active_days": active_days,
            "topic_diversity": len(unique_topics)
        }
    
    def export_report(self, format: str = "json") -> str:
        """خروجی گزارش"""
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "summary": self.get_dashboard_data("month"),
            "detailed_stats": {
                "today": self._get_today_stats(),
                "week": self._get_week_stats(),
                "month": self._get_month_stats(),
                "overall": self._get_overall_stats()
            }
        }
        
        if format == "json":
            return json.dumps(report_data, ensure_ascii=False, indent=2)
        
        # TODO: اضافه کردن فرمت‌های دیگر (PDF, HTML)
        return str(report_data)

# نمونه استفاده
analytics_dashboard = AnalyticsDashboard()
