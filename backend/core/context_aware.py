"""
🎯 Context Awareness - آگاهی از محیط و وضعیت
"""

import subprocess
import json
import os
from datetime import datetime

class ContextAware:
    def __init__(self):
        self.context_file = "data/context/system_context.json"
        
    def get_system_context(self):
        """دریافت اطلاعات سیستم"""
        context = {
            "timestamp": datetime.now().isoformat(),
            "time_info": self.get_time_info(),
            "system_info": self.get_system_info(),
            "weather_info": self.get_weather_info(),
            "user_activity": self.get_user_activity()
        }
        
        self.save_context(context)
        return context
    
    def get_time_info(self):
        """اطلاعات زمان"""
        now = datetime.now()
        return {
            "current_time": now.strftime("%H:%M"),
            "current_date": now.strftime("%Y-%m-%d"),
            "day_of_week": now.strftime("%A"),
            "persian_date": self.get_persian_date(),
            "season": self.get_season()
        }
    
    def get_persian_date(self):
        """تاریخ شمسی تقریبی"""
        import datetime
        now = datetime.datetime.now()
        # تبدیل ساده میلادی به شمسی (تقریبی)
        persian_year = now.year - 621
        return f"{persian_year}/{now.month}/{now.day}"
    
    def get_season(self):
        """فصل سال"""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return "زمستان"
        elif month in [3, 4, 5]:
            return "بهار"
        elif month in [6, 7, 8]:
            return "تابستان"
        else:
            return "پاییز"
    
    def get_system_info(self):
        """اطلاعات سیستم"""
        try:
            # CPU usage
            cpu_usage = self.get_cpu_usage()
            
            # Memory usage
            memory_info = self.get_memory_info()
            
            # Disk usage
            disk_usage = self.get_disk_usage()
            
            return {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_info,
                "disk_usage": disk_usage,
                "fox_status": "running"
            }
        except:
            return {"status": "unknown"}
    
    def get_cpu_usage(self):
        """استفاده CPU"""
        try:
            result = subprocess.run(['top', '-bn1'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'Cpu(s)' in line:
                    return line.split(',')[0].split(':')[1].strip()
        except:
            pass
        return "نامشخص"
    
    def get_memory_info(self):
        """اطلاعات حافظه"""
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                total = int(lines[0].split()[1]) // 1024  # MB
                available = int(lines[2].split()[1]) // 1024  # MB
                used = total - available
                usage_percent = (used / total) * 100
                return f"{usage_percent:.1f}% ({used}MB/{total}MB)"
        except:
            return "نامشخص"
    
    def get_disk_usage(self):
        """استفاده دیسک"""
        try:
            result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                return f"{parts[4]} ({parts[2]}/{parts[1]})"
        except:
            return "نامشخص"
    
    def get_weather_info(self):
        """اطلاعات آب و هوا (شبیه‌سازی)"""
        # در آینده می‌تونیم از API واقعی استفاده کنیم
        import random
        weather_conditions = ["آفتابی", "ابری", "بارانی", "برفی", "مه‌آلود"]
        temperatures = list(range(-5, 35))
        
        return {
            "condition": random.choice(weather_conditions),
            "temperature": f"{random.choice(temperatures)}°C",
            "suggestion": self.get_weather_suggestion()
        }
    
    def get_weather_suggestion(self):
        """پیشنهاد بر اساس آب و هوا"""
        suggestions = [
            "لباس گرم بپوش",
            "چتر همراه داشته باش", 
            "آفتاب خوبیه، بیرون برو",
            "هوا خنکه، قدم بزن"
        ]
        import random
        return random.choice(suggestions)
    
    def get_user_activity(self):
        """فعالیت کاربر"""
        return {
            "last_interaction": datetime.now().strftime("%H:%M"),
            "session_duration": "نامشخص",
            "activity_level": "متوسط"
        }
    
    def save_context(self, context):
        """ذخیره context"""
        os.makedirs(os.path.dirname(self.context_file), exist_ok=True)
        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(context, f, ensure_ascii=False, indent=2)
    
    def get_context_summary(self):
        """خلاصه context"""
        context = self.get_system_context()
        
        return f"""🎯 وضعیت فعلی:
⏰ زمان: {context['time_info']['current_time']} - {context['time_info']['season']}
💻 سیستم: CPU {context['system_info']['cpu_usage']}, RAM {context['system_info']['memory_usage']}
🌤️ هوا: {context['weather_info']['condition']} {context['weather_info']['temperature']}
💡 پیشنهاد: {context['weather_info']['suggestion']}"""

# Instance سراسری
context_aware = ContextAware()
