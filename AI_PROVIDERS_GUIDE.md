# 🤖 AI Providers System - راهنمای کامل

سیستم مدیریت API های مختلف هوش مصنوعی در Fox AI

## 🎯 ویژگی‌ها

### ✅ AI Providers پشتیبانی شده:
- **Ollama** (محلی) - پیش‌فرض
- **OpenAI GPT** - با API key
- **Anthropic Claude** - با API key  
- **Google Gemini** - با API key
- **Custom AI** - هر API دلخواه

### 🔧 قابلیت‌ها:
- **مدیریت خودکار** providers
- **Multi-AI consultation** - مشورت با چند AI
- **انتخاب بهترین پاسخ** با امتیازدهی
- **کانفیگ فایل** برای تنظیمات
- **اضافه کردن آسان** AI جدید

## 🚀 نحوه استفاده

### دستورات اصلی:

```bash
# نمایش AI های موجود
/ai_providers

# فعال/غیرفعال کردن Multi-AI
/multi_ai_on
/multi_ai_off
/multi_ai_status
```

### اضافه کردن AI جدید:

```bash
# OpenAI
/add_openai sk-your-api-key-here

# Claude
/add_claude your-claude-api-key

# Gemini  
/add_gemini your-gemini-api-key

# Custom AI
/add_custom MyAI sk-123 https://api.myai.com/v1/chat
```

## ⚙️ کانفیگ فایل

فایل: `backend/config/ai_providers.json`

```json
{
  "ollama": {
    "enabled": true,
    "base_url": "http://localhost:11434",
    "model": "qwen2:7b"
  },
  "openai": {
    "enabled": false,
    "api_key": "sk-your-key",
    "model": "gpt-3.5-turbo"
  },
  "claude": {
    "enabled": false,
    "api_key": "your-key",
    "model": "claude-3-sonnet-20240229"
  }
}
```

## 🔨 اضافه کردن AI جدید

### 1. ایجاد Provider Class:

```python
class MyAIProvider(AIProvider):
    def __init__(self, api_key):
        super().__init__("MyAI", api_key)
        self.base_url = "https://api.myai.com"
    
    def generate_response(self, prompt):
        # پیاده‌سازی API call
        response = requests.post(f"{self.base_url}/chat", 
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"message": prompt})
        return response.json()["response"]
```

### 2. اضافه کردن به Manager:

```python
# در ai_providers.py
if config.get("myai", {}).get("enabled", False):
    api_key = config["myai"].get("api_key")
    if api_key:
        self.providers["myai"] = MyAIProvider(api_key)
```

## 🎯 الگوریتم انتخاب بهترین پاسخ

```python
def select_best_response(responses):
    best_score = 0
    best_response = None
    
    for provider, response in responses.items():
        score = len(response)  # طول پاسخ
        
        # ترجیح متن فارسی
        persian_chars = sum(1 for c in response if '\u0600' <= c <= '\u06FF')
        score += persian_chars * 2
        
        # امتیاز provider (اختیاری)
        if provider == "claude":
            score += 50
        elif provider == "openai":
            score += 30
            
        if score > best_score:
            best_score = score
            best_response = response
    
    return best_response
```

## 🔒 امنیت

- **API Keys** در فایل کانفیگ محفوظ
- **Timeout** برای درخواست‌ها
- **Error Handling** کامل
- **Fallback** به Ollama محلی

## 📊 مثال استفاده

```python
from backend.core.ai_providers import ai_manager
from backend.core.multi_ai_system import multi_ai_system

# فعال کردن Multi-AI
multi_ai_system.enable()

# دریافت پاسخ از همه AI ها
responses = ai_manager.get_responses("سلام چطوری؟")
print(responses)
# {'ollama': 'سلام! خوبم تو چطوری؟', 'openai': 'درود! حالم عالیه'}

# انتخاب بهترین پاسخ
best = multi_ai_system.get_best_response("سلام چطوری؟")
print(best)
# سلام! خوبم تو چطوری؟
# 💡 *از ollama*
```

## 🚨 عیب‌یابی

### مشکلات رایج:

1. **API Key نامعتبر**
   ```
   ❌ خطا: 401 Unauthorized
   ✅ حل: بررسی API key در کانفیگ
   ```

2. **اتصال به اینترنت**
   ```
   ❌ خطا: Connection timeout
   ✅ حل: بررسی اتصال و proxy
   ```

3. **Ollama در دسترس نیست**
   ```
   ❌ خطا: Connection refused
   ✅ حل: راه‌اندازی Ollama
   ```

## 🔄 بروزرسانی

برای اضافه کردن AI جدید:

1. کلاس Provider بسازید
2. به AIProviderManager اضافه کنید  
3. کانفیگ بروزرسانی کنید
4. دستور جدید اضافه کنید

---

**Fox AI - قدرت چند AI در یک مکان! 🦊🤖**
