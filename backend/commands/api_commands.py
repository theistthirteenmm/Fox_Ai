"""
CLI Commands for API Management
"""
from backend.core.api_manager import api_manager

def handle_api_command(command_parts):
    """مدیریت دستورات API"""
    if len(command_parts) < 2:
        return """
🤖 دستورات API Manager:

📝 اضافه کردن API:
/api add <name> <api_key> <base_url> <model> [free/paid]

📋 لیست API ها:
/api list

🗑️ حذف API:
/api remove <name>

🧪 تست API:
/api test <name>

💬 چت با API مشخص:
/api chat <name> <message>

🆓 API های رایگان پیشنهادی:
- HuggingFace (محدود ولی رایگان)
- Cohere Trial (رایگان با محدودیت)
- Together.AI (کریدیت رایگان)
- Groq (سریع و رایگان)
"""
    
    action = command_parts[1].lower()
    
    if action == "add":
        if len(command_parts) < 6:
            return "❌ فرمت: /api add <name> <api_key> <base_url> <model> [free/paid]"
        
        name = command_parts[2]
        api_key = command_parts[3]
        base_url = command_parts[4]
        model = command_parts[5]
        is_free = len(command_parts) > 6 and command_parts[6].lower() == "free"
        
        return api_manager.add_api(name, api_key, base_url, model, is_free)
    
    elif action == "list":
        apis = api_manager.list_apis()
        if not apis:
            return "📭 هیچ API ای تنظیم نشده"
        
        result = "🤖 لیست API ها:\n\n"
        for api in apis:
            result += f"• {api['name']}: {api['model']}\n"
            result += f"  {api['status']} | {api['type']}\n"
            result += f"  🔗 {api['base_url']}\n\n"
        return result
    
    elif action == "remove":
        if len(command_parts) < 3:
            return "❌ فرمت: /api remove <name>"
        return api_manager.remove_api(command_parts[2])
    
    elif action == "test":
        if len(command_parts) < 3:
            return "❌ فرمت: /api test <name>"
        
        name = command_parts[2]
        if api_manager.test_api(name):
            return f"✅ API {name} در دسترس است"
        else:
            return f"❌ API {name} در دسترس نیست"
    
    elif action == "chat":
        if len(command_parts) < 4:
            return "❌ فرمت: /api chat <name> <message>"
        
        name = command_parts[2]
        message = " ".join(command_parts[3:])
        messages = [{"role": "user", "content": message}]
        
        return api_manager.chat_with_api(name, messages)
    
    elif action == "free":
        return """
🆓 API های رایگان پیشنهادی:

1️⃣ **Groq** (سریع و رایگان):
   • ثبت نام: https://console.groq.com
   • مدل: llama3-8b-8192
   • محدودیت: 14,400 درخواست/روز

2️⃣ **HuggingFace**:
   • ثبت نام: https://huggingface.co
   • مدل: microsoft/DialoGPT-medium
   • محدودیت: 1000 درخواست/ماه

3️⃣ **Cohere Trial**:
   • ثبت نام: https://cohere.ai
   • مدل: command-light
   • محدودیت: کریدیت رایگان

4️⃣ **Together.AI**:
   • ثبت نام: https://together.ai
   • مدل: Llama-2-7b-chat
   • محدودیت: $25 کریدیت رایگان

مثال اضافه کردن Groq:
/api add groq YOUR_API_KEY https://api.groq.com/openai/v1 llama3-8b-8192 free
"""
    
    else:
        return "❌ دستور نامعتبر. از /api برای راهنما استفاده کنید"
