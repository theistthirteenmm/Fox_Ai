# Personal AI Assistant 🤖

یک دستیار هوش مصنوعی شخصی و محلی با قابلیت‌های پیشرفته

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Latest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ ویژگی‌ها

### 🧠 هوش مصنوعی
- **مدل‌های محلی**: پشتیبانی کامل از Ollama
- **مدل‌های فارسی**: بهینه‌سازی شده برای زبان فارسی
- **AI خارجی**: اتصال اختیاری به OpenAI، Claude، Gemini

### 💾 سیستم حافظه
- **حافظه بلندمدت**: ذخیره مکالمات و اطلاعات مهم
- **تاریخچه هوشمند**: جستجو و بازیابی مکالمات قبلی
- **پروفایل کاربر**: یادگیری تدریجی علایق و تنظیمات

### 🌐 دسترسی به اینترنت
- **جستجوی وب**: جستجو در اینترنت با DuckDuckGo
- **اخبار**: دریافت آخرین اخبار
- **آب و هوا**: اطلاعات آب و هوایی
- **محتوای وب**: استخراج محتوا از صفحات وب

### 🖥️ رابط‌های کاربری
- **CLI**: رابط خط فرمان قدرتمند با Rich
- **Web**: رابط وب مدرن با WebSocket
- **Real-time**: پاسخ‌دهی فوری و تعاملی

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.8+
- Docker (برای Ollama)
- Git

### 1. کلون کردن پروژه
```bash
git clone https://github.com/your-username/personal-ai.git
cd personal-ai
```

### 2. نصب Dependencies
```bash
# ایجاد محیط مجازی
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate     # Windows

# نصب کتابخانه‌ها
pip install -r requirements.txt
```

### 3. راه‌اندازی Ollama
```bash
# راه‌اندازی با Docker
docker run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama ollama/ollama

# دانلود مدل فارسی
docker exec ollama ollama pull qwen2:7b
```

### 4. تنظیمات (اختیاری)
```bash
# کپی کردن فایل تنظیمات
cp .env.example .env

# ویرایش تنظیمات
nano .env
```

## 🎯 استفاده

### رابط خط فرمان (CLI)
```bash
python cli/main.py
```

### رابط وب
```bash
python start_web.py
```
سپس مرورگر را به آدرس `http://localhost:8080` باز کنید.

## 📋 دستورات CLI

| دستور | توضیح |
|--------|-------|
| `/help` | نمایش راهنما |
| `/models` | لیست مدل‌های موجود |
| `/history` | تاریخچه مکالمات |
| `/search <متن>` | جستجو در تاریخچه |
| `/memory` | نمایش حافظه ذخیره شده |
| `/web <سوال>` | جستجو در اینترنت |
| `/news [موضوع]` | دریافت اخبار |
| `/weather [شهر]` | وضعیت آب و هوا |
| `/url <آدرس>` | محتوای صفحه وب |
| `/compare <سوال>` | مقایسه AI های مختلف |
| `/new` | شروع مکالمه جدید |
| `/clear` | پاک کردن مکالمه فعلی |
| `/quit` | خروج |

## 🔌 API Endpoints

### اصلی
- `GET /` - رابط وب
- `GET /health` - وضعیت سیستم
- `WebSocket /ws` - ارتباط real-time

### حافظه
- `GET /api/conversations` - لیست مکالمات
- `GET /api/memory` - حافظه ذخیره شده
- `GET /api/search?q=<query>` - جستجو در تاریخچه

### اینترنت
- `GET /api/web-search?q=<query>` - جستجوی وب
- `GET /api/news?topic=<topic>` - اخبار
- `GET /api/weather?city=<city>` - آب و هوا
- `GET /api/webpage?url=<url>` - محتوای صفحه

## ⚙️ تنظیمات

### متغیرهای محیطی (.env)
```bash
# Debug
DEBUG=true
LOG_LEVEL=INFO

# Database
DATABASE_URL=sqlite:///./data/database/personal_ai.db

# Ollama
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=qwen2:7b

# API Ports
API_PORT=8000
WEB_PORT=8080

# External AI APIs (اختیاری)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

## 🏗️ ساختار پروژه

```
personal-ai/
├── backend/
│   ├── core/
│   │   ├── llm_engine.py      # موتور LLM
│   │   ├── conversation.py    # مدیریت مکالمات
│   │   ├── memory.py          # سیستم حافظه
│   │   ├── internet.py        # دسترسی اینترنت
│   │   └── ai_connector.py    # اتصال AI خارجی
│   ├── database/
│   │   └── models.py          # مدل‌های دیتابیس
│   └── config/
│       └── settings.py        # تنظیمات
├── cli/
│   └── main.py               # رابط CLI
├── web/
│   ├── app.py               # سرور وب
│   ├── static/              # فایل‌های استاتیک
│   └── templates/           # قالب‌های HTML
├── data/                    # داده‌های پروژه
├── requirements.txt         # Dependencies
├── start_web.py            # راه‌انداز وب
└── test.sh                 # اسکریپت تست
```

## 🧪 تست

```bash
# اجرای تست‌های کامل
./test.sh

# تست دستی CLI
python cli/main.py

# تست API
curl http://localhost:8080/health
```

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/amazing-feature`)
3. تغییرات را commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request بسازید

## 📝 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. فایل [LICENSE](LICENSE) را برای جزئیات بیشتر مطالعه کنید.

## 🙏 تشکر

- [Ollama](https://ollama.ai/) برای موتور LLM محلی
- [FastAPI](https://fastapi.tiangolo.com/) برای فریمورک وب
- [Rich](https://rich.readthedocs.io/) برای رابط CLI زیبا
- [SQLAlchemy](https://sqlalchemy.org/) برای ORM

## 📞 پشتیبانی

اگر مشکلی داشتید یا سوالی دارید:

- Issue جدید در GitHub بسازید
- مستندات را مطالعه کنید
- کد نمونه‌ها را بررسی کنید

---

**ساخته شده با ❤️ برای جامعه فارسی‌زبان**
