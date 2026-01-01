# Git Commands for GitHub Upload

## پروژه آماده است! 🎉

### مراحل آپلود به GitHub:

1. **ایجاد Repository در GitHub:**
   - به GitHub.com برو
   - روی "New repository" کلیک کن
   - نام: `personal-ai-assistant`
   - توضیح: `🤖 Personal AI Assistant with Persian support`
   - Public یا Private انتخاب کن
   - **هیچ فایلی اضافه نکن** (README, .gitignore, license)

2. **اتصال به GitHub:**
```bash
cd /home/hamed/personal-ai

# اضافه کردن remote origin
git remote add origin https://github.com/YOUR_USERNAME/personal-ai-assistant.git

# تغییر نام branch به main
git branch -M main

# آپلود اولیه
git push -u origin main
```

3. **آپدیت‌های آینده:**
```bash
# اضافه کردن تغییرات جدید
git add .
git commit -m "✨ Add new feature"
git push
```

### فایل‌های آماده شده:

✅ **README.md** - مستندات کامل  
✅ **LICENSE** - لایسنس MIT  
✅ **.gitignore** - فایل‌های نادیده گرفته شده  
✅ **.env.example** - نمونه تنظیمات  
✅ **setup.sh** - اسکریپت نصب خودکار  
✅ **requirements.txt** - Dependencies  
✅ **کد کامل** - تمام فایل‌های پروژه  

### ویژگی‌های Repository:

🧠 **AI Engine**: Ollama + External APIs  
💾 **Memory System**: SQLite + Smart Context  
🌐 **Internet Access**: Web Search + News + Weather  
🖥️ **Dual Interface**: CLI + Web  
🇮🇷 **Persian Support**: کاملاً فارسی  
📚 **Documentation**: مستندات کامل  
🧪 **Testing**: اسکریپت تست خودکار  
⚡ **Quick Setup**: نصب یک‌کلیکه  

### نکات مهم:

- فایل `.env` در .gitignore هست (امنیت API keys)
- Database فایل‌ها ignore شده‌اند
- Virtual environment ignore شده
- فقط کد اصلی آپلود می‌شه

### بعد از آپلود:

1. **GitHub Actions** اضافه کن (CI/CD)
2. **Issues template** بساز
3. **Contributing guidelines** اضافه کن
4. **Wiki** برای مستندات تکمیلی
5. **Releases** برای version management

**Repository آماده آپلود است! 🚀**
