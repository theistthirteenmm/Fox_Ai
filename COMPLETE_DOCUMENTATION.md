# 🦊 Fox AI Assistant - مستندات کامل

یک دستیار هوشمند فارسیزبان با قابلیت‌های پیشرفته یادگیری و تشخیص کاربر

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Latest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 فهرست مطالب

- [🚀 راه‌اندازی سریع](#-راهاندازی-سریع)
- [🏗️ معماری سیستم](#️-معماری-سیستم)
- [🧠 قابلیت‌های هوشمند](#-قابلیتهای-هوشمند)
- [👥 سیستم چندکاربره](#-سیستم-چندکاربره)
- [📊 آنالیتیکس و گزارش‌گیری](#-آنالیتیکس-و-گزارشگیری)
- [🔔 سیستم اعلان‌های هوشمند](#-سیستم-اعلانهای-هوشمند)
- [🧠 حافظه و یادگیری](#-حافظه-و-یادگیری)
- [🌐 اتصال به اینترنت](#-اتصال-به-اینترنت)
- [🎮 گیمیفیکیشن](#-گیمیفیکیشن)
- [🔧 دستورات کامل](#-دستورات-کامل)
- [⚙️ تنظیمات و پیکربندی](#️-تنظیمات-و-پیکربندی)
- [🐳 استقرار و DevOps](#-استقرار-و-devops)

---

## 🚀 راه‌اندازی سریع

### نصب و اجرا
```bash
# کلون پروژه
git clone https://github.com/theistthirteenmm/Fox_Ai.git
cd Fox_Ai

# راه‌اندازی محیط مجازی
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا venv\Scripts\activate  # Windows

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای سرور
python start_web.py
```

### دسترسی
- 🌐 **Web Interface**: http://localhost:4444
- 💻 **CLI Interface**: `python cli/main.py`
- 📱 **Mobile**: همان آدرس در مرورگر موبایل

---

## 🏗️ معماری سیستم

### نمای کلی
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Engine    │
│                 │    │                 │    │                 │
│ • Web UI        │◄──►│ • FastAPI       │◄──►│ • Ollama        │
│ • CLI           │    │ • WebSocket     │    │ • qwen2:7b      │
│ • Mobile        │    │ • REST API      │    │ • Multi-AI      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Layer    │    │  Smart Systems  │    │   External      │
│                 │    │                 │    │                 │
│ • SQLite DB     │    │ • Memory        │    │ • Internet      │
│ • JSON Files    │    │ • Analytics     │    │ • Web Search    │
│ • User Profiles │    │ • Notifications │    │ • News APIs     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### ساختار فایل‌ها
```
Fox_Ai/
├── 🌐 web/                    # رابط وب
│   ├── app.py                 # سرور اصلی FastAPI
│   ├── templates/             # قالب‌های HTML
│   └── static/                # فایل‌های استاتیک
├── 🧠 backend/                # منطق کسب‌وکار
│   ├── core/                  # هسته اصلی
│   │   ├── llm_engine.py      # موتور AI
│   │   ├── smart_memory.py    # حافظه هوشمند
│   │   ├── smart_notifications.py # اعلان‌های هوشمند
│   │   ├── analytics_dashboard.py # آنالیتیکس
│   │   ├── smart_user_detection.py # تشخیص کاربر
│   │   ├── fox_gamification.py # گیمیفیکیشن
│   │   ├── internet.py        # دسترسی اینترنت
│   │   └── personality.py     # شخصیت Fox
│   ├── config/                # تنظیمات
│   ├── database/              # مدیریت دیتابیس
│   └── commands/              # دستورات خاص
├── 💾 data/                   # ذخیره‌سازی
│   ├── database/              # دیتابیس اصلی
│   ├── profiles/              # پروفایل کاربران
│   ├── context/               # حافظه مکالمات
│   ├── analytics/             # داده‌های آنالیتیکس
│   ├── notifications/         # اعلان‌ها
│   └── gamification/          # داده‌های بازی
├── 💻 cli/                    # رابط خط فرمان
└── 🐳 docker/                 # کانتینرسازی
```

---

## 🧠 قابلیت‌های هوشمند

### 1. موتور AI چندگانه
- **Ollama**: موتور اصلی (qwen2:7b)
- **Multi-AI Support**: OpenAI, Claude, Gemini
- **Fallback System**: تغییر خودکار در صورت خرابی
- **Load Balancing**: توزیع بار بین مدل‌ها

### 2. شخصیت پویا
- **Personality System**: شخصیت قابل تنظیم
- **Mood Tracking**: ردیابی حالت کاربر
- **Adaptive Responses**: پاسخ‌های متناسب با موقعیت
- **Time-Aware**: پاسخ‌های مناسب زمان

### 3. یادگیری پیشرفته
- **Custom Learning**: آموزش دانش شخصی
- **Experience System**: سیستم تجربه و رشد
- **Pattern Recognition**: تشخیص الگوهای رفتاری
- **Continuous Improvement**: بهبود مداوم عملکرد

---

## 👥 سیستم چندکاربره

### تشخیص هوشمند کاربر
```python
# تحلیل سبک نوشتن
- طول جملات و پاراگراف‌ها
- استفاده از علائم نگارشی
- واژگان و عبارات شخصی
- الگوهای گفتاری (رسمی/غیررسمی)

# تشخیص خودکار
- اطمینان بالا (40%+): تغییر فوری
- اطمینان متوسط (25%+): سوال تایید
- یادگیری مداوم از هر مکالمه
```

### مدیریت پروفایل
- **پروفایل‌های جداگانه**: تنظیمات شخصی هر کاربر
- **تاریخچه مجزا**: حافظه مستقل برای هر کاربر
- **روابط خانوادگی**: تشخیص روابط بین کاربران
- **تنظیمات امنیتی**: کنترل دسترسی

---

## 📊 آنالیتیکس و گزارش‌گیری

### داشبورد تحلیلی
```
📈 آمار لحظه‌ای:
├── تعداد مکالمات امروز
├── زمان پاسخ میانگین
├── موضوعات پربحث
└── ساعات فعالیت

📊 تحلیل روند:
├── مقایسه هفتگی/ماهانه
├── نمودار پیشرفت
├── الگوهای استفاده
└── امتیاز تعامل

📋 گزارش‌های تخصصی:
├── آمار یادگیری
├── عملکرد AI
├── رضایت کاربر
└── پیشنهادات بهبود
```

### متریک‌های کلیدی
- **Engagement Score**: امتیاز تعامل (0-100)
- **Learning Progress**: پیشرفت یادگیری
- **Response Quality**: کیفیت پاسخ‌ها
- **User Satisfaction**: رضایت کاربر

---

## 🔔 سیستم اعلان‌های هوشمند

### انواع اعلان‌ها
```
🔄 Follow-up Questions:
├── 30 دقیقه بعد از سوالات مهم
├── پیگیری موضوعات ناتمام
└── درخواست بازخورد

📚 Learning Reminders:
├── یادآوری مطالعه موضوعات
├── تمرین مهارت‌های جدید
└── مرور دانش قبلی

📊 Daily Summaries:
├── خلاصه فعالیت‌های روز
├── دستاوردهای جدید
└── برنامه‌ریزی فردا

🏆 Achievements:
├── رسیدن به سطوح جدید
├── تکمیل چالش‌ها
└── رکوردهای شخصی
```

### تنظیمات هوشمند
- **Quiet Hours**: ساعات سکوت قابل تنظیم
- **Priority System**: اولویت‌بندی اعلان‌ها
- **Frequency Control**: کنترل تعدد اعلان‌ها
- **Context Awareness**: اعلان‌های متناسب با موقعیت

---

## 🧠 حافظه و یادگیری

### سیستم حافظه هوشمند
```
🔍 Context Memory:
├── یادآوری مکالمات مرتبط
├── ارتباط موضوعات
├── تاریخچه تصمیمات
└── الگوهای رفتاری

🎯 Smart Recall:
├── جستجوی معنایی
├── فیلتر زمانی
├── اولویت‌بندی اهمیت
└── پیشنهاد موضوعات

📚 Knowledge Base:
├── دانش شخصی کاربر
├── حقایق آموخته شده
├── تجربیات ثبت شده
└── ترجیحات شناسایی شده
```

### الگوریتم‌های یادگیری
- **Incremental Learning**: یادگیری تدریجی
- **Forgetting Curve**: منحنی فراموشی
- **Spaced Repetition**: تکرار فاصله‌دار
- **Active Learning**: یادگیری فعال

---

## 🌐 اتصال به اینترنت

### قابلیت‌های جستجو
```
🔍 Web Search:
├── جستجوی عمومی
├── اخبار روز
├── اطلاعات آب و هوا
└── محتوای صفحات وب

📰 News Integration:
├── اخبار موضوعی
├── خلاصه‌سازی اخبار
├── منابع معتبر
└── آپدیت لحظه‌ای

🌤️ Weather Service:
├── وضعیت فعلی
├── پیش‌بینی هفتگی
├── هشدارهای جوی
└── توصیه‌های لباس
```

### Web Scraping
- **Smart Extraction**: استخراج هوشمند محتوا
- **Content Filtering**: فیلتر محتوای مناسب
- **Rate Limiting**: محدودیت نرخ درخواست
- **Error Handling**: مدیریت خطاهای شبکه

---

## 🎮 گیمیفیکیشن

### سیستم امتیازدهی
```
🏆 Levels & XP:
├── سطح Fox (1-100)
├── امتیاز تجربه
├── مهارت‌های تخصصی
└── رتبه‌بندی عملکرد

🎯 Achievements:
├── اولین مکالمه
├── یادگیری 100 حقیقت
├── استفاده 30 روزه
└── تسلط بر موضوعات

📊 Statistics:
├── آمار روزانه
├── رکوردهای شخصی
├── مقایسه با دیگران
└── پیشرفت زمانی
```

### چالش‌ها و مأموریت‌ها
- **Daily Challenges**: چالش‌های روزانه
- **Learning Quests**: مأموریت‌های یادگیری
- **Social Goals**: اهداف اجتماعی
- **Personal Milestones**: نقاط عطف شخصی

---

## 🔧 دستورات کامل

### دستورات اصلی
```bash
# 🧠 هوش مصنوعی
/help                    # راهنمای کامل
/models                  # لیست مدل‌های AI
/multi_ai_on/off        # فعال/غیرفعال Multi-AI
/ai_providers           # لیست ارائه‌دهندگان AI

# 👤 مدیریت کاربر
/users                  # لیست کاربران
/switch <نام>           # تغییر کاربر
/profile               # مشاهده پروفایل
/detect <متن>          # تشخیص کاربر از متن
/signature [نام]       # آمار امضای کاربر

# 🧠 حافظه و یادگیری
/teach <سوال> <پاسخ>   # آموزش پاسخ خاص
/learn <موضوع> <حقیقت> # آموزش دانش جدید
/recall <موضوع>        # یادآوری مکالمات
/context <موضوع>       # مکالمات مرتبط
/history               # تاریخچه کامل
/memory                # حافظه ذخیره شده

# 📊 آنالیتیکس
/stats                 # آمار امروز
/dashboard             # داشبورد کامل
/notifications         # مدیریت اعلان‌ها
/experience            # تجربه و سن Fox
/achievements          # دستاوردها

# 🌐 اینترنت
/web <سوال>           # جستجوی وب
/news [موضوع]         # اخبار
/weather [شهر]        # آب و هوا
/url <آدرس>          # محتوای صفحه

# 🎭 شخصیت و حالت
/mood                  # وضعیت احساسی
/feel <احساس> <مقدار> # تنظیم احساس
/happy/sad/excited     # تغییر سریع حالت
/voices               # تنظیم صدا
/speak <متن>          # گفتن متن

# 🔧 تنظیمات
/settings             # تنظیمات کلی
/clear               # پاک کردن مکالمه
/new                 # شروع مکالمه جدید
/status              # وضعیت کامل سیستم
```

### دستورات پیشرفته
```bash
# 🤖 Multi-AI Management
/add_openai [API_KEY]     # اضافه کردن OpenAI
/add_claude [API_KEY]     # اضافه کردن Claude
/add_gemini [API_KEY]     # اضافه کردن Gemini
/add_custom <نام> <key>   # AI دلخواه

# 📚 Dataset Management
/pretrain                # پیش‌آموزش با دیتاست
/learned                 # آمار یادگیری
/boost <ماه>            # تقویت هوش
/age <روز>              # پیر کردن Fox

# 🕐 Time & Context
/time_greeting          # سلام بر اساس زمان
/time_suggestion        # پیشنهاد بر اساس زمان

# 🔍 Advanced Search
/search <متن>          # جستجو در تاریخچه
/filter <تاریخ>        # فیلتر بر اساس تاریخ
```

---

## ⚙️ تنظیمات و پیکربندی

### فایل تنظیمات (.env)
```bash
# Server Configuration
WEB_PORT=4444
WEB_HOST=0.0.0.0
API_PORT=8000

# AI Configuration
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=qwen2:7b

# External APIs
OPENAI_API_KEY=your_key_here
CLAUDE_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Features
DEBUG=false
LOG_LEVEL=INFO
MULTI_AI_ENABLED=true
```

### تنظیمات پیشرفته
```python
# backend/config/settings.py
class Settings:
    # Database
    database_url: str = "sqlite:///./data/database/fox_ai.db"
    
    # AI Models
    default_model: str = "qwen2:7b"
    fallback_models: List[str] = ["llama2", "mistral"]
    
    # Smart Systems
    memory_retention_days: int = 365
    notification_frequency: str = "smart"  # smart, high, medium, low
    analytics_enabled: bool = True
    
    # Security
    max_users: int = 10
    session_timeout: int = 3600
    rate_limit: int = 100  # requests per minute
```

---

## 🐳 استقرار و DevOps

### Docker Deployment
```bash
# Build & Run
docker-compose up -d

# Services
├── fox-ai-web      # Web Interface
├── fox-ai-api      # Backend API
├── ollama          # AI Engine
├── nginx           # Reverse Proxy
└── redis           # Cache (optional)
```

### Production Setup
```yaml
# docker-compose.yml
version: '3.8'
services:
  fox-ai:
    build: .
    ports:
      - "4444:4444"
    environment:
      - PRODUCTION=true
      - DATABASE_URL=postgresql://...
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - fox-ai
```

### Monitoring & Logging
```bash
# Health Check
curl http://localhost:4444/health

# Logs
docker logs fox-ai-web -f

# Metrics
/metrics endpoint for Prometheus
```

---

## 📈 Performance & Scalability

### بهینه‌سازی عملکرد
- **Caching**: کش هوشمند پاسخ‌ها
- **Connection Pooling**: مدیریت اتصالات دیتابیس
- **Async Processing**: پردازش غیرهمزمان
- **Load Balancing**: توزیع بار

### مقیاس‌پذیری
- **Horizontal Scaling**: افزایش سرورها
- **Database Sharding**: تقسیم دیتابیس
- **CDN Integration**: شبکه توزیع محتوا
- **Microservices**: معماری میکروسرویس

---

## 🔒 امنیت

### اقدامات امنیتی
- **Rate Limiting**: محدودیت نرخ درخواست
- **Input Sanitization**: پاکسازی ورودی‌ها
- **CORS Configuration**: تنظیمات CORS
- **API Key Management**: مدیریت کلیدهای API

### حریم خصوصی
- **Local Storage**: ذخیره‌سازی محلی داده‌ها
- **Data Encryption**: رمزنگاری اطلاعات حساس
- **User Consent**: رضایت کاربر برای ذخیره داده‌ها
- **GDPR Compliance**: انطباق با GDPR

---

## 🚀 آینده و توسعه

### ویژگی‌های در دست توسعه
- **Voice Interface**: رابط صوتی کامل
- **Mobile App**: اپلیکیشن موبایل نیتیو
- **Plugin System**: سیستم افزونه
- **API Marketplace**: بازار API

### مشارکت در توسعه
```bash
# Fork & Clone
git clone https://github.com/yourusername/Fox_Ai.git

# Create Feature Branch
git checkout -b feature/new-feature

# Make Changes & Test
python -m pytest tests/

# Submit Pull Request
```

---

## 📞 پشتیبانی و کمک

### منابع کمک
- **GitHub Issues**: گزارش باگ و درخواست ویژگی
- **Documentation**: مستندات کامل
- **Community**: انجمن کاربران
- **Email Support**: پشتیبانی ایمیلی

### FAQ
**Q: چطور مدل AI رو تغییر بدم؟**
A: از دستور `/models` لیست مدل‌ها رو ببین و با `/switch_model` تغییر بده

**Q: چطور چند کاربر رو مدیریت کنم؟**
A: Fox خودکار کاربران رو تشخیص می‌ده یا با `/switch` دستی تغییر بده

**Q: داده‌هام امن هستن؟**
A: بله، همه داده‌ها محلی ذخیره میشن و رمزنگاری می‌شوند

---

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر فایل [LICENSE](LICENSE) را مطالعه کنید.

---

**Fox AI - دستیار هوشمند شما 🦊**

*ساخته شده با ❤️ برای کاربران فارسیزبان*

---

## 📊 آمار پروژه

- **خطوط کد**: 15,000+
- **فایل‌ها**: 50+
- **ویژگی‌ها**: 100+
- **زبان‌های پشتیبانی شده**: فارسی، انگلیسی
- **پلتفرم‌ها**: Web, CLI, Mobile-Ready

**آخرین آپدیت**: 2026/01/01
