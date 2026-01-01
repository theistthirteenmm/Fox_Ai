# 🚀 Fox AI - راهنمای Deployment

راهنمای کامل نصب و راه‌اندازی Fox AI روی سرورهای مختلف

## 📋 پیش‌نیازها

- **سیستم عامل**: Linux (Ubuntu/CentOS/Debian)
- **Python**: 3.8 یا بالاتر
- **Docker**: برای Ollama
- **RAM**: حداقل 8GB (برای مدل 7B)
- **فضای دیسک**: حداقل 10GB

## 🔧 نصب سریع (یک دستوری)

```bash
# کلون و نصب خودکار
git clone https://github.com/theistthirteenmm/Fox_Ai.git
cd Fox_Ai
chmod +x setup.sh
./setup.sh
```

## 📝 نصب دستی (مرحله به مرحله)

### 1. کلون کردن پروژه
```bash
git clone https://github.com/theistthirteenmm/Fox_Ai.git
cd Fox_Ai
```

### 2. نصب Python Dependencies
```bash
# ایجاد محیط مجازی
python3 -m venv venv
source venv/bin/activate

# نصب کتابخانه‌ها
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. راه‌اندازی Ollama
```bash
# نصب Docker (اگه نصب نیست)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# راه‌اندازی Ollama
docker run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama ollama/ollama

# دانلود مدل فارسی (ممکنه چند دقیقه طول بکشه)
docker exec ollama ollama pull qwen2:7b
```

### 4. تنظیمات محیط
```bash
# کپی فایل تنظیمات
cp .env.example .env

# ویرایش تنظیمات (اختیاری)
nano .env
```

### 5. تست سیستم
```bash
# اجرای تست خودکار
./test.sh
```

## 🌐 راه‌اندازی سرویس‌ها

### CLI Interface
```bash
# فعال‌سازی محیط مجازی
source venv/bin/activate

# اجرای CLI
python cli/main.py
```

### Web Interface
```bash
# فعال‌سازی محیط مجازی
source venv/bin/activate

# اجرای وب سرور
python start_web.py
```

سپس مرورگر را به آدرس `http://localhost:8080` باز کنید.

## 🌍 دسترسی از راه دور

### تنظیم IP و Port
```bash
# ویرایش .env
nano .env

# تغییر تنظیمات
WEB_HOST=0.0.0.0  # برای دسترسی از همه IP ها
WEB_PORT=8080     # پورت دلخواه
```

### دسترسی از سیستم‌های دیگر
```bash
# Web Interface
http://[SERVER_IP]:8080

# Web Terminal (CLI در مرورگر)
http://[SERVER_IP]:8080/terminal

# SSH Access
ssh username@[SERVER_IP]
cd Fox_Ai
source venv/bin/activate
python cli/main.py
```

## 🔧 Production Deployment

### اجرا در Background
```bash
# با nohup
nohup python start_web.py > fox.log 2>&1 &

# یا با screen
screen -S fox-ai
python start_web.py
# Ctrl+A, D برای detach کردن
```

### Systemd Service (Ubuntu/CentOS)
```bash
# ایجاد service file
sudo nano /etc/systemd/system/fox-ai.service
```

محتوای فایل:
```ini
[Unit]
Description=Fox AI Assistant
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/Fox_Ai
Environment=PATH=/path/to/Fox_Ai/venv/bin
ExecStart=/path/to/Fox_Ai/venv/bin/python start_web.py
Restart=always

[Install]
WantedBy=multi-user.target
```

فعال‌سازی:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fox-ai
sudo systemctl start fox-ai
sudo systemctl status fox-ai
```

### Nginx Reverse Proxy (اختیاری)
```bash
# نصب Nginx
sudo apt install nginx  # Ubuntu/Debian
sudo yum install nginx  # CentOS

# تنظیم proxy
sudo nano /etc/nginx/sites-available/fox-ai
```

محتوای فایل:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

فعال‌سازی:
```bash
sudo ln -s /etc/nginx/sites-available/fox-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 امنیت

### Firewall
```bash
# Ubuntu (UFW)
sudo ufw allow 8080
sudo ufw enable

# CentOS (firewalld)
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload
```

### SSL/HTTPS (با Let's Encrypt)
```bash
# نصب Certbot
sudo apt install certbot python3-certbot-nginx

# دریافت گواهی SSL
sudo certbot --nginx -d your-domain.com
```

## 🔧 عیب‌یابی

### مشکلات رایج

**1. Ollama در دسترس نیست:**
```bash
# چک کردن وضعیت Docker
docker ps | grep ollama

# راه‌اندازی مجدد
docker restart ollama
```

**2. مدل یافت نشد:**
```bash
# لیست مدل‌ها
docker exec ollama ollama list

# دانلود مجدد
docker exec ollama ollama pull qwen2:7b
```

**3. پورت در استفاده:**
```bash
# پیدا کردن پروسه
sudo lsof -i :8080

# کشتن پروسه
sudo kill -9 PID
```

**4. مشکل میکروفن در وب:**
- از Chrome یا Edge استفاده کنید
- اجازه دسترسی به میکروفن را بدهید
- برای HTTPS از Nginx + SSL استفاده کنید

### لاگ‌ها
```bash
# لاگ‌های سیستم
journalctl -u fox-ai -f

# لاگ‌های Docker
docker logs ollama

# لاگ‌های Fox
tail -f fox.log
```

## 📊 مانیتورینگ

### Health Check
```bash
# چک سلامت API
curl http://localhost:8080/health

# چک Ollama
curl http://localhost:11434/api/tags
```

### Resource Usage
```bash
# استفاده CPU/RAM
htop

# استفاده دیسک
df -h

# استفاده Docker
docker stats ollama
```

## 🔄 بروزرسانی

```bash
# دریافت آخرین تغییرات
git pull origin main

# بروزرسانی dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# راه‌اندازی مجدد
sudo systemctl restart fox-ai
```

## 📞 پشتیبانی

اگر مشکلی داشتید:

1. **مستندات**: README.md را مطالعه کنید
2. **تست**: `./test.sh` را اجرا کنید
3. **لاگ‌ها**: فایل‌های log را بررسی کنید
4. **GitHub Issues**: مشکل را در GitHub گزارش دهید

---

**Fox AI آماده خدمت‌رسانی در هر محیطی! 🦊🚀**
