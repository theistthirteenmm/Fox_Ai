# 🦊 Fox AI Assistant - Web Edition

یک دستیار هوشمند فارسیزبان با رابط وب

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Ollama](https://img.shields.io/badge/Ollama-Latest-orange.svg)

## 🚀 راه‌اندازی سریع

```bash
python start_web.py
```

**همین!** این دستور:
- ✅ وب سرور را شروع می‌کند
- ✅ همه dependencies را بارگذاری می‌کند
- ✅ روی کامپیوتر و موبایل قابل دسترس

**دسترسی:**
- 🌐 **Browser**: http://localhost:4444 (کامپیوتر و موبایل)
- 📱 **Mobile**: همون آدرس در مرورگر موبایل

## ✨ ویژگی‌های Fox AI

### 🧠 هوش مصنوعی
- **مکالمه طبیعی** با Ollama
- **زبان فارسی** بهینه‌شده
- **یادگیری شخصی** از کاربر

### 🔊 صوت و گفتار
- **تشخیص گفتار فارسی**
- **تولید گفتار** با صدای فارسی
- **کنترل صوتی** کامل

### 🧠 حافظه و یادگیری
- **حافظه مکالمات** (`/recall`, `/history`)
- **آموزش پاسخ‌ها** (`/teach`, `/learn`)
- **یادگیری تدریجی** از کاربر

### 🌐 اتصال به اینترنت
- **جستجوی وب** (`/web`)
- **اخبار** (`/news`)
- **آب و هوا** (`/weather`)

### 👥 چند کاربره
- **پروفایل‌های جداگانه**
- **تنظیمات شخصی**
- **تاریخچه مجزا**

## 🎯 نحوه استفاده

### دستورات اصلی:
- `/help` - راهنمای کامل
- `/teach سلام سلام دوست عزیز!` - آموزش پاسخ
- `/learn ایران پایتخت ایران تهران است` - آموزش حقیقت
- `/recall موضوع` - یادآوری مکالمات
- `/web سوال` - جستجو در اینترنت
- `/speak متن` - گفتن متن
- `/voices` - تنظیم صدا

### مکالمه طبیعی:
فقط مثل یک دوست با Fox صحبت کنید!

## 🛠️ راه‌اندازی دستی

### پیش‌نیازها:
- Python 3.8+
- Ollama

### نصب:
```bash
# نصب Python dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### اجرا:
```bash
# سرور وب
python start_web.py
```

## 🔧 رابط‌های مختلف

### 1. Web Interface (پیشنهادی)
```bash
python start_web.py
# http://localhost:4444
```

### 2. CLI Interface  
```bash
python cli/main.py
```

## 📄 مستندات

- **[📚 مستندات کامل](COMPLETE_DOCUMENTATION.md)** - راهنمای جامع تمام قابلیت‌ها
- [راهنمای یادگیری](LEARNING_GUIDE.md) - نحوه آموزش Fox
- [راهنمای چندکاربره](MULTI_USER_GUIDE.md) - مدیریت چند کاربر
- [راهنمای روابط](RELATIONSHIP_GUIDE.md) - سیستم روابط
- [راهنمای استقرار](DEPLOYMENT.md) - نصب و راه‌اندازی
- [راهنمای Docker](DOCKER.md) - کانتینرسازی

---

**Fox AI - دستیار هوشمند شما 🦊**

ساخته شده با ❤️ برای کاربران فارسیزبان
