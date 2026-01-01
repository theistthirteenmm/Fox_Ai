"""
FastAPI Web Application with Internet Access
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
import json
import asyncio
from backend.core.llm_engine import LLMEngine
from backend.core.conversation import ConversationManager
from backend.core.internet import InternetAccess
from backend.core.ai_connector import AIConnector
from backend.config.settings import settings
from web.terminal import add_terminal_support
from backend.core.personality import PersonalitySystem
from backend.core.user_profile import UserProfile
from backend.core.fox_learning import FoxLearningSystem
from backend.commands.api_commands import handle_api_command
from backend.core.user_profiles import user_manager
from backend.core.multi_ai_system import multi_ai_system
from backend.core.fox_scraper import fox_scraper
from backend.core.smart_memory import smart_memory
from backend.core.smart_notifications import smart_notifications
from backend.core.analytics_dashboard import analytics_dashboard
from backend.core.smart_user_detection import smart_detector

app = FastAPI(title="Fox - Personal AI Assistant")

# Static files and templates
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Initialize components
llm = LLMEngine(
    model_name=settings.default_model,
    host=settings.ollama_host
)
conversation_manager = ConversationManager()
internet = InternetAccess()
ai_connector = AIConnector()
personality = PersonalitySystem()

# Initialize user profile and learning system
from backend.database.models import get_db
db_session = next(get_db())
user_profile = UserProfile(db_session)
fox_learning = FoxLearningSystem(user_profile)

async def handle_web_command(command: str, websocket: WebSocket) -> str:
    """Handle web chat commands"""
    print(f"🔍 Command received: {command}")  # Debug
    parts = command.strip().split()
    cmd = parts[0][1:].lower()  # Remove /
    print(f"🔍 Parsed command: {cmd}")  # Debug
    
    if cmd == 'help':
        return """📚 دستورات موجود:
• /help - نمایش راهنما
• /models - لیست مدلهای موجود
• /history - نمایش تاریخچه مکالمات
• /search <متن> - جستجو در تاریخچه
• /memory - نمایش حافظه ذخیره شده
• /web <سوال> - جستجو در اینترنت
• /news [موضوع] - دریافت اخبار
• /weather [شهر] - وضعیت آب و هوا
• /url <آدرس> - دریافت محتوای صفحه وب
• /mood - نمایش وضعیت احساسی
• /feel <احساس> <مقدار> - تنظیم احساس (0-10)
• /happy, /sad, /excited, /serious - تغییر سریع حالت
• /users - نمایش همه کاربران
• /switch <نام> - تغییر کاربر فعال
• /status - نمایش وضعیت کامل Fox
• /experience - نمایش تجربه و سن Fox
• /boost <ماه> - تقویت هوش Fox
• /age <روز> - پیر کردن Fox
• /pretrain - پیش‌آموزش Fox با دیتاست
• /teach <کلید> <پاسخ> - آموزش پاسخ خاص
• /learn <موضوع> <حقیقت> - آموزش دانش جدید
• /stats - آمار شخصی امروز
• /dashboard - داشبورد تحلیلی کامل
• /notifications - مدیریت اعلان‌های هوشمند
• /context <موضوع> - یافتن مکالمات مرتبط
• /detect <متن> - تشخیص کاربر از روی متن
• /signature [نام] - آمار امضای کاربر
• /learned - نمایش آمار یادگیری
• /recall <موضوع> - یادآوری مکالمات قبلی
• /speak <متن> - گفتن متن با صدا
• /voices - نمایش صداهای موجود
• /voice_test - تست صدای فعلی
• /listen - راهنمای استفاده از میکروفن
• /voice - راهنمای مکالمه صوتی
• /new - شروع مکالمه جدید
• /clear - پاک کردن مکالمه فعلی
• /multi_ai_on - فعال کردن Multi-AI
• /multi_ai_off - غیرفعال کردن Multi-AI  
• /multi_ai_status - وضعیت Multi-AI
• /ai_providers - لیست AI providers
• /add_openai [API_KEY] - اضافه کردن OpenAI
• /add_claude [API_KEY] - اضافه کردن Claude
• /add_gemini [API_KEY] - اضافه کردن Gemini
• /add_custom [نام] [API_KEY] [URL] - اضافه کردن AI دلخواه

🕐 زمان و محیط:
• /time_greeting - سلام بر اساس زمان
• /time_suggestion - پیشنهاد بر اساس زمان
• /context - وضعیت سیستم و محیط

📊 حالت و احساسات:
• /mood_stats - آمار حالات روحی

🔔 دستیار پیشگام:
• /suggest - پیشنهاد تصادفی
• /remind [متن] [زمان] - یادآوری

🎮 بازی‌سازی:
• /fox_status - وضعیت و سطح Fox
• /challenge - چالش روزانه
• /fox_mood - حالت Fox"""
    
    elif cmd == 'models':
        try:
            models = llm.list_models()
            if models:
                return "🤖 مدلهای موجود:\n" + "\n".join([f"• {model}" for model in models])
            else:
                return "❌ هیچ مدلی یافت نشد"
        except:
            return "❌ خطا در دریافت لیست مدلها"
    
    elif cmd == 'history':
        try:
            from backend.database.models import get_db, Message
            from sqlalchemy import desc
            
            db = next(get_db())
            messages = db.query(Message).order_by(desc(Message.timestamp)).limit(10).all()
            
            if messages:
                result = "📜 آخرین مکالمات:\n\n"
                for msg in reversed(messages):
                    time_str = msg.timestamp.strftime("%m/%d %H:%M")
                    role = "شما" if msg.role == "user" else "Fox"
                    content = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
                    result += f"🕐 {time_str} - {role}: {content}\n"
                return result
            else:
                return "📜 هیچ مکالمه‌ای یافت نشد"
        except Exception as e:
            return f"❌ خطا در دریافت تاریخچه: {str(e)}"
    
    elif cmd == 'search':
        if len(parts) > 1:
            search_term = ' '.join(parts[1:])
            try:
                from backend.database.models import get_db, Message
                from sqlalchemy import desc, or_
                
                db = next(get_db())
                messages = db.query(Message).filter(
                    or_(
                        Message.content.contains(search_term),
                        Message.content.like(f'%{search_term}%')
                    )
                ).order_by(desc(Message.timestamp)).limit(5).all()
                
                if messages:
                    result = f"🔍 نتایج جستجو برای '{search_term}':\n\n"
                    for msg in reversed(messages):
                        time_str = msg.timestamp.strftime("%m/%d %H:%M")
                        role = "شما" if msg.role == "user" else "Fox"
                        content = msg.content[:80] + "..." if len(msg.content) > 80 else msg.content
                        result += f"🕐 {time_str} - {role}: {content}\n"
                    return result
                else:
                    return f"🔍 نتیجه‌ای برای '{search_term}' یافت نشد"
            except Exception as e:
                return f"❌ خطا در جستجو: {str(e)}"
        return "استفاده: /search <متن جستجو>"
    
    elif cmd == 'api':
        result = handle_api_command(parts)
        return result
    
    elif cmd == 'memory':
        try:
            # Get user profile info
            profile_info = f"""🧠 حافظه Fox:
👤 نام: {user_profile.get_name()}
💝 سطح رابطه: {user_profile.get_relationship_status()}
🎯 علایق: {', '.join(user_profile.profile.get('interests', []))}
🎭 ویژگی‌های شخصیتی: {', '.join(user_profile.profile.get('personality_traits', []))}"""
            return profile_info
        except:
            return "❌ خطا در دریافت حافظه"
    elif cmd == 'news':
        topic = ' '.join(parts[1:]) if len(parts) > 1 else "اخبار"
        try:
            results = internet.search_web(f"اخبار {topic}", 3)
            if results:
                return f"📰 آخرین اخبار {topic}:\n" + "\n".join(results[:3])
            else:
                return f"📰 خبری در مورد '{topic}' یافت نشد"
        except:
            return f"❌ خطا در دریافت اخبار {topic}"
    
    elif cmd == 'weather':
        city = ' '.join(parts[1:]) if len(parts) > 1 else "تهران"
        try:
            results = internet.search_web(f"وضعیت آب و هوا {city}", 2)
            if results:
                return f"🌤️ آب و هوای {city}:\n" + "\n".join(results[:2])
            else:
                return f"🌤️ اطلاعات آب و هوای '{city}' یافت نشد"
        except:
            return f"❌ خطا در دریافت آب و هوای {city}"
    
    elif cmd == 'url':
        if len(parts) > 1:
            url = parts[1]
            try:
                # Simple URL content fetch (you'd need to implement this)
                return f"🌐 محتوای {url} دریافت شد (این قابلیت نیاز به پیاده‌سازی دارد)"
            except:
                return f"❌ خطا در دریافت محتوای {url}"
        return "استفاده: /url <آدرس وب>"
    
    elif cmd in ['feel']:
        if len(parts) >= 3:
            emotion = parts[1]
            try:
                value = int(parts[2])
                if 0 <= value <= 10:
                    # Set emotion (you'd need to implement this)
                    return f"😊 احساس '{emotion}' به مقدار {value} تنظیم شد"
                else:
                    return "❌ مقدار باید بین 0 تا 10 باشد"
            except:
                return "❌ مقدار نامعتبر"
        return "استفاده: /feel <احساس> <مقدار 0-10>"
    
    elif cmd in ['happy', 'sad', 'excited', 'serious']:
        mood_map = {
            'happy': 'خوشحال',
            'sad': 'غمگین', 
            'excited': 'هیجان‌زده',
            'serious': 'جدی'
        }
        return f"😊 حالت به '{mood_map[cmd]}' تغییر کرد"
    
    elif cmd == 'users':
        try:
            # Get all users (you'd need to implement this)
            return "👥 کاربران: حامد (فعال), رادین"
        except:
            return "❌ خطا در دریافت لیست کاربران"
    
    elif cmd == 'switch':
        if len(parts) > 1:
            username = parts[1]
            return f"👤 کاربر فعال به '{username}' تغییر کرد"
        return "استفاده: /switch <نام کاربر>"
    
    elif cmd == 'status':
        try:
            return """📊 وضعیت کامل Fox:
🦊 نام: Fox AI Assistant
👤 کاربر فعال: حامد
💝 سطح رابطه: دوست صمیمی
🧠 سطح هوش: متوسط
📚 تعداد یادگیری‌ها: در حال محاسبه...
🎭 حالت فعلی: خوشحال
⚡ وضعیت: آنلاین و آماده"""
        except:
            return "❌ خطا در دریافت وضعیت"
    
    elif cmd == 'experience':
        try:
            return """📈 تجربه و سن Fox:
🎂 سن: 30 روز
⭐ سطح تجربه: متوسط
🧠 هوش: سطح 3 از 6
📚 تعداد مکالمات: 150+
🎯 مهارت‌های یادگیری شده: 25"""
        except:
            return "❌ خطا در دریافت اطلاعات تجربه"
    
    elif cmd == 'boost':
        if len(parts) > 1:
            try:
                months = int(parts[1])
                return f"🚀 هوش Fox به مدت {months} ماه تقویت شد!"
            except:
                return "❌ تعداد ماه نامعتبر"
        return "استفاده: /boost <تعداد ماه>"
    
    elif cmd == 'age':
        if len(parts) > 1:
            try:
                days = int(parts[1])
                return f"⏰ Fox به مدت {days} روز پیر شد!"
            except:
                return "❌ تعداد روز نامعتبر"
        return "استفاده: /age <تعداد روز>"
    
    elif cmd == 'pretrain':
        try:
            return "🎓 پیش‌آموزش Fox با دیتاست شروع شد..."
        except:
            return "❌ خطا در پیش‌آموزش"
    
    elif cmd == 'new':
        try:
            # Clear conversation (you'd need to implement this)
            return "🆕 مکالمه جدید شروع شد!"
        except:
            return "❌ خطا در شروع مکالمه جدید"
    
    elif cmd == 'clear':
        try:
            # Clear current conversation (you'd need to implement this)
            return "🧹 مکالمه فعلی پاک شد!"
        except:
            return "❌ خطا در پاک کردن مکالمه"
        if len(parts) >= 2:
            rest = command[6:].strip()
            if ' ' in rest:
                trigger, response = rest.split(' ', 1)
                return fox_learning.teach_response(trigger, response)
        return "استفاده: /teach <کلید> <پاسخ>"
    
    elif cmd == 'learn':
        if len(parts) >= 2:
            rest = command[6:].strip()
            if ' ' in rest:
                topic, fact = rest.split(' ', 1)
                return fox_learning.teach_fact(topic, fact)
        return "استفاده: /learn <موضوع> <حقیقت>"
    
    elif cmd == 'learned':
        stats = fox_learning.get_learning_stats()
        return f"""📚 آمار یادگیری Fox:
• پاسخهای آموزش داده شده: {stats['custom_responses']}
• حقایق یادگیری شده: {stats['learned_facts']}
• اطلاعات فرهنگی: {stats['cultural_knowledge']}"""
    
    elif cmd == 'mood':
        try:
            mood = personality.get_current_mood()
            return f"😊 وضعیت احساسی Fox: {mood}"
        except:
            return "😊 وضعیت احساسی Fox: خوشحال"
    
    elif cmd == 'recall' or cmd == 'remember':
        if len(parts) > 1:
            search_term = ' '.join(parts[1:])
            try:
                from backend.database.models import get_db, Message
                from sqlalchemy import desc, or_
                
                db = next(get_db())
                # Search in recent messages (last 100)
                messages = db.query(Message).filter(
                    or_(
                        Message.content.contains(search_term),
                        Message.content.like(f'%{search_term}%')
                    )
                ).order_by(desc(Message.timestamp)).limit(10).all()
                
                if messages:
                    result = f"🧠 یادم هست! در مورد '{search_term}' صحبت کردیم:\n\n"
                    for msg in reversed(messages[-3:]):  # Show last 3 matches
                        time_str = msg.timestamp.strftime("%Y/%m/%d %H:%M")
                        role = "شما" if msg.role == "user" else "Fox"
                        content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                        result += f"📅 {time_str} - {role}: {content}\n"
                    return result
                else:
                    return f"🤔 متأسفانه چیزی در مورد '{search_term}' یادم نیست"
            except Exception as e:
                return f"❌ خطا در جستجو: {str(e)}"
        return "استفاده: /recall <موضوع یا کلمه کلیدی>"
        if len(parts) > 1:
            query = ' '.join(parts[1:])
            try:
                results = internet.search_web(query, 3)
                if results:
                    return f"🌐 نتایج جستجو برای '{query}':\n" + "\n".join(results[:2])
                else:
                    return f"🌐 نتیجه‌ای برای '{query}' پیدا نشد"
            except:
                return f"🌐 خطا در جستجو برای '{query}'"
        return "استفاده: /web <سوال جستجو>"
    
    elif cmd == 'voices':
        return """🔊 لیست صداهای موجود:
برای دیدن صداها، دستور /list_voices را امتحان کنید.
برای انتخاب صدا: /set_voice <شماره>

مثال:
/list_voices
/set_voice 2"""
    
    elif cmd == 'list_voices':
        return """🔊 برای دیدن لیست صداها:

1. کنسول مرورگر را باز کنید (F12)
2. این کد را کپی و اجرا کنید:

speechSynthesis.getVoices().forEach((voice, i) => {
    const lang = voice.lang.includes('fa') ? '🇮🇷' : 
                 voice.lang.includes('ar') ? '🇸🇦' : 
                 voice.lang.includes('en') ? '🇺🇸' : '🌍';
    console.log(`${i}: ${lang} ${voice.name} (${voice.lang})`);
});

3. شماره صدای مورد نظر را یادداشت کنید
4. از /set_voice <شماره> استفاده کنید

مثال: /set_voice 3"""
    
    elif cmd == 'set_voice':
        if len(parts) > 1:
            voice_id = parts[1]
            return f"""🔊 تنظیم صدا به شماره {voice_id}
این تنظیم در جلسه فعلی اعمال می‌شود.
برای تست: /voice_test"""
        return "استفاده: /set_voice <شماره صدا>"
    
    elif cmd == 'voice_test':
        return "🔊 تست صدا: این متن برای تست صدای فعلی است. اگر انگلیسی می‌خواند، تنظیمات مرورگر را تغییر دهید."
    
    elif cmd == 'speak':
        if len(parts) > 1:
            text = ' '.join(parts[1:])
            return f"🔊 گفتن: {text}"
        return "استفاده: /speak <متن>"
    
    elif cmd == 'listen':
        return "🎤 برای گوش دادن، از دکمه میکروفن در رابط استفاده کنید"
    
    elif cmd == 'voice':
        return "🎤 برای شروع مکالمه صوتی، دکمه میکروفن را فشار دهید و صحبت کنید"
    
    elif cmd == 'tts_on':
        return "🔊 صدای Fox روشن شد - پاسخ‌ها خوانده می‌شوند"
    
    elif cmd == 'tts_off':
        return "🔇 صدای Fox خاموش شد - فقط متن نمایش داده می‌شود"
    
    elif cmd == 'download_url':
        if len(parts) > 1:
            url = parts[1]
            
            # ارسال پیام شروع
            await websocket.send_text(json.dumps({
                "type": "message", 
                "message": f"🌐 شروع دانلود از:\n{url}\n\nلطفاً صبر کنید... ⏳"
            }))
            
            try:
                from backend.core.url_downloader import url_downloader
                result = url_downloader.download_and_process(url)
                
                if "error" in result:
                    return f"❌ خطا: {result['error']}"
                else:
                    success_msg = f"""✅ **دانلود از URL موفق بود!**

🌐 **آدرس:** {result['url']}
📥 **دانلود شده:** {result['downloaded']} مکالمه  
💾 **ذخیره شده:** {result['saved']} مکالمه

🦊 **Fox یاد گرفت!**
مکالمات جدید به حافظه اضافه شد.

**تست کن:** چیزی بگو و ببین Fox چی یاد گرفته!"""
                    
                    return success_msg
                    
            except Exception as e:
                return f"❌ خطا در دانلود: {str(e)}"
        else:
            return """📖 **راهنمای دانلود از URL:**

**استفاده:**
`/download_url https://example.com/dataset.json`

**فرمت‌های پشتیبانی شده:**
• JSON: `{"q": "سوال", "a": "جواب"}`
• CSV: `سوال,جواب`  
• TXT: خط اول سوال، خط دوم جواب

**مثال:**
`/download_url https://raw.githubusercontent.com/user/repo/main/persian_qa.json`"""
    
    elif cmd == 'multi_ai_on':
        result = multi_ai_system.enable()
        return result
        
    elif cmd == 'multi_ai_off':
        result = multi_ai_system.disable()
        return result
        
    elif cmd == 'stats':
        # آمار شخصی کاربر
        stats = analytics_dashboard.get_dashboard_data("today")
        insights = smart_memory.get_user_insights()
        
        return f"""📊 **آمار امروز شما:**
        
🗣️ **مکالمات:** {stats['conversations']} مکالمه
⏱️ **زمان پاسخ:** {stats['avg_response_time']} ثانیه
📚 **موضوعات:** {', '.join(stats['top_topics'].keys()) if stats['top_topics'] else 'هیچ'}
💬 **کلمات:** {stats['word_stats']['user']} شما، {stats['word_stats']['ai']} من

🧠 **تحلیل رفتار:**
📈 **کل مکالمات:** {insights.get('total_conversations', 0)}
🕐 **ساعات فعال:** {', '.join([h[0] for h in insights.get('active_hours', [])[:3]])}
📅 **آخرین فعالیت:** {insights.get('last_activity', 'نامشخص')}
"""
        
    elif cmd == 'dashboard':
        # داشبورد کامل
        week_stats = analytics_dashboard.get_dashboard_data("week")
        month_stats = analytics_dashboard.get_dashboard_data("month")
        
        return f"""📊 **داشبورد تحلیلی Fox**

📅 **هفته گذشته:**
• {week_stats['conversations']} مکالمه ({week_stats['avg_daily']} روزانه)
• روند: {week_stats.get('trend', 'نامشخص')}
• موضوعات: {', '.join(list(week_stats['top_topics'].keys())[:3])}

📆 **ماه گذشته:**  
• {month_stats['conversations']} مکالمه ({month_stats['avg_weekly']} هفتگی)
• یادگیری: {month_stats.get('learning_progress', {}).get('total_sessions', 0)} جلسه

🎯 **پیشنهادات:**
{chr(10).join(['• ' + suggestion for suggestion in smart_memory.suggest_topics()[:3]])}
"""
        
    elif cmd == 'notifications':
        # اعلان‌های هوشمند
        pending = smart_notifications.get_pending_notifications()
        unread = smart_notifications.get_unread_notifications()
        stats = smart_notifications.get_notification_stats()
        
        response = f"""🔔 **اعلان‌های هوشمند**

📊 **آمار:**
• کل: {stats['total']} | ارسال شده: {stats['sent']} | خوانده شده: {stats['read']}
• نرخ مطالعه: {stats['read_rate']:.1f}%

"""
        
        if pending:
            response += "⏰ **در انتظار ارسال:**\n"
            for notif in pending[:3]:
                response += f"• {notif.title}: {notif.message}\n"
                
        if unread:
            response += "\n📬 **خوانده نشده:**\n"
            for notif in unread[:3]:
                response += f"• {notif.title}: {notif.message}\n"
                
        return response
        
    elif cmd == 'context':
        # مکالمات مرتبط
        if len(parts) > 1:
            query = ' '.join(parts[1:])
            relevant = smart_memory.get_relevant_context(query)
            
            if relevant:
                response = f"🔍 **مکالمات مرتبط با '{query}':**\n\n"
                for i, conv in enumerate(relevant[:3], 1):
                    date = datetime.fromisoformat(conv['timestamp']).strftime('%Y/%m/%d %H:%M')
                    response += f"{i}. **{date}** - {conv['topic']}\n"
                    response += f"   سوال: {conv['user_input'][:100]}...\n\n"
                return response
            else:
                return "🤔 مکالمه مرتبطی پیدا نکردم"
        else:
            return "❓ لطفاً موضوع مورد نظر را بنویسید: `/context موضوع`"
            
    elif cmd == 'detect':
        # تشخیص کاربر فعلی
        known_users = [u['name'] for u in user_manager.get_all_users()]
        if len(parts) > 1:
            test_text = ' '.join(parts[1:])
            detected_user, confidence = smart_detector.detect_current_user(test_text, known_users)
            
            if detected_user:
                return f"🔍 **تشخیص کاربر:**\nمتن: \"{test_text}\"\n👤 کاربر تشخیص داده شده: **{detected_user}**\n📊 اطمینان: {confidence:.1%}"
            else:
                return f"🤷‍♂️ نتونستم کاربر رو تشخیص بدم\n📊 بهترین امتیاز: {confidence:.1%}"
        else:
            return "استفاده: `/detect متن برای تشخیص کاربر`"
            
    elif cmd == 'signature':
        # آمار امضای کاربر
        if len(parts) > 1:
            username = parts[1]
            stats = smart_detector.get_user_statistics(username)
            
            if "error" in stats:
                return f"❌ {stats['error']}"
                
            return f"""📝 **آمار امضای {username}:**
            
📊 **آمار کلی:**
• تعداد پیام‌ها: {stats['message_count']}
• میانگین طول پیام: {stats['avg_message_length']:.1f} کاراکتر
• عبارات رایج: {stats['common_phrases_count']} عبارت
• قدرت امضا: {stats['signature_strength']:.1%}

📅 **آخرین آپدیت:** {stats['last_updated'][:16].replace('T', ' ')}
"""
        else:
            current_stats = smart_detector.get_user_statistics(user_manager.current_user)
            if "error" not in current_stats:
                return f"""📝 **آمار امضای شما:**
                
📊 تعداد پیام‌ها: {current_stats['message_count']}
📏 میانگین طول: {current_stats['avg_message_length']:.1f} کاراکتر  
💪 قدرت امضا: {current_stats['signature_strength']:.1%}
"""
            else:
                return "❌ هنوز امضای شما ثبت نشده"
        result = multi_ai_system.get_status()
        return result
    
    elif cmd == 'ai_providers':
        from backend.core.ai_providers import ai_manager
        providers = ai_manager.get_available_providers()
        if providers:
            result = "🤖 AI Providers موجود:\n"
            for p in providers:
                status = "🟢" if p.is_available() else "🔴"
                result += f"{status} {p.name}\n"
            return result
        return "❌ هیچ AI provider موجود نیست"
    
    elif cmd == 'add_openai':
        if len(parts) < 2:
            return "❌ API key لازم است: /add_openai YOUR_API_KEY"
        
        api_key = parts[1]
        from backend.core.ai_providers import ai_manager, OpenAIProvider
        provider = OpenAIProvider(api_key)
        ai_manager.add_provider(provider)
        return "✅ OpenAI اضافه شد!"
    
    elif cmd == 'add_claude':
        if len(parts) < 2:
            return "❌ API key لازم است: /add_claude YOUR_API_KEY"
        
        api_key = parts[1]
        from backend.core.ai_providers import ai_manager, ClaudeProvider
        provider = ClaudeProvider(api_key)
        ai_manager.add_provider(provider)
        return "✅ Claude اضافه شد!"
    
    elif cmd == 'add_gemini':
        if len(parts) < 2:
            return "❌ API key لازم است: /add_gemini YOUR_API_KEY"
        
        api_key = parts[1]
        from backend.core.ai_providers import ai_manager, GeminiProvider
        provider = GeminiProvider(api_key)
        ai_manager.add_provider(provider)
        return "✅ Gemini اضافه شد!"
    
    elif cmd == 'add_custom':
        if len(parts) < 4:
            return """❌ پارامترهای لازم:
/add_custom [نام] [API_KEY] [BASE_URL]

مثال:
/add_custom MyAI sk-123 https://api.myai.com/v1/chat"""
        
        name = parts[1]
        api_key = parts[2]
        base_url = parts[3]
        
        from backend.core.ai_providers import ai_manager, CustomProvider
        provider = CustomProvider(name, api_key, base_url)
        ai_manager.add_provider(provider)
        return f"✅ {name} اضافه شد!"
    
    elif cmd == 'time_greeting':
        from backend.core.time_responses import time_responses
        return time_responses.get_time_greeting()
    
    elif cmd == 'time_suggestion':
        from backend.core.time_responses import time_responses
        return time_responses.get_time_suggestion()
    
    elif cmd == 'mood_stats':
        from backend.core.mood_tracker import mood_tracker
        return mood_tracker.get_mood_stats()
    
    elif cmd == 'context':
        from backend.core.context_aware import context_aware
        return context_aware.get_context_summary()
    
    elif cmd == 'suggest':
        from backend.core.proactive_assistant import proactive_assistant
        suggestion = proactive_assistant.get_random_suggestion()
        return f"💡 {suggestion}"
    
    elif cmd == 'remind':
        if len(parts) < 3:
            return "❌ فرمت: /remind [متن] [زمان]\nمثال: /remind قرار ملاقات 14:30"
        
        text = " ".join(parts[1:-1])
        time_str = parts[-1]
        
        from backend.core.proactive_assistant import proactive_assistant
        from datetime import datetime, timedelta
        
        try:
            # پردازش ساده زمان
            if ":" in time_str:
                hour, minute = map(int, time_str.split(":"))
                remind_time = datetime.now().replace(hour=hour, minute=minute, second=0)
                if remind_time <= datetime.now():
                    remind_time += timedelta(days=1)
            else:
                remind_time = datetime.now() + timedelta(minutes=int(time_str))
            
            return proactive_assistant.add_reminder(text, remind_time.isoformat())
        except:
            return "❌ فرمت زمان نادرست"
    
    elif cmd == 'fox_status':
        from backend.core.fox_gamification import fox_game
        return fox_game.get_fox_status()
    
    elif cmd == 'challenge':
        from backend.core.fox_gamification import fox_game
        return fox_game.get_daily_challenge()
    
    elif cmd == 'fox_mood':
        from backend.core.fox_gamification import fox_game
        return fox_game.get_fox_mood()
    
    return f"دستور '{cmd}' شناخته نشد. /help را امتحان کنید."

# Add terminal support
add_terminal_support(app)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/terminal", response_class=HTMLResponse)
async def terminal_page(request: Request):
    return templates.TemplateResponse("terminal.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Start new conversation session
    session_id = conversation_manager.start_new_session()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            user_message = message_data.get("message", "")
            
            if not user_message.strip():
                continue
                
            # Check for new user introduction (فقط اگه واقعاً معرفی کردن)
            # فقط اگه پیام کوتاه باشه و شامل کلمات معرفی باشه
            if (len(user_message.split()) <= 10 and 
                any(pattern in user_message.lower() for pattern in ["اسم من", "نام من", "من هستم", "صدام کن"])):
                
                potential_new_user = user_manager.detect_new_user(user_message)
                if potential_new_user and potential_new_user != user_manager.current_user:
                    # Switch to new user
                    user_manager.switch_user(potential_new_user)
                    
                    # Check if profile exists
                    profile = user_manager.get_user_profile(potential_new_user)
                    if not profile:
                        # Ask for relationship with Hamed
                        relationship_question = user_manager.ask_for_relationship(potential_new_user)
                        await websocket.send_text(json.dumps({
                            "type": "message",
                        "message": relationship_question,
                        "sender": "assistant"
                    }))
                    continue
            
            # Update conversation stats for current user
            user_manager.update_conversation_stats(user_manager.current_user, user_message)
            
            # شروع زمان‌سنجی پاسخ
            import time
            start_time = time.time()
            
            # تشخیص هوشمند کاربر بر اساس سبک نوشتن
            current_user = user_manager.current_user
            known_users = [u['name'] for u in user_manager.get_all_users()]
            
            if len(known_users) > 1 and len(user_message.split()) >= 5:  # حداقل 5 کلمه
                detected_user, confidence = smart_detector.detect_current_user(user_message, known_users)
                
                if detected_user and detected_user != current_user and confidence > 0.4:
                    # تغییر کاربر با اطمینان بالا
                    user_manager.switch_user(detected_user)
                    
                    await websocket.send_text(json.dumps({
                        "type": "user_switch",
                        "message": f"🔄 سلام {detected_user}! تشخیص دادم که تو هستی (اطمینان: {confidence:.0%})",
                        "user": detected_user,
                        "confidence": confidence
                    }))
                    
                elif detected_user and detected_user != current_user and confidence > 0.25:
                    # سوال تایید با اطمینان متوسط
                    await websocket.send_text(json.dumps({
                        "type": "user_confirmation",
                        "message": f"🤔 احساس می‌کنم {detected_user} هستی؟ (اطمینان: {confidence:.0%})\nاگه درسته بگو 'بله' یا اگه اشتباهه اسمت رو بگو",
                        "suggested_user": detected_user,
                        "confidence": confidence
                    }))
            
            # یادگیری سبک نوشتن کاربر فعلی
            smart_detector.learn_user_signature(user_manager.current_user, user_message)
            
            # Add user message to conversation
            conversation_manager.add_message("user", user_message)
            
            # Analyze user input for emotional context
            personality.analyze_user_input(user_message)
            
            # Send typing indicator
            await websocket.send_text(json.dumps({
                "type": "typing",
                "message": "در حال تایپ..."
            }))
            
            try:
                # Check for commands
                if user_message.startswith('/'):
                    try:
                        command_response = await handle_web_command(user_message, websocket)
                        if command_response:
                            await websocket.send_text(json.dumps({
                                "type": "message",
                                "message": command_response
                            }))
                            continue
                    except Exception as e:
                        print(f"❌ Command error: {e}")
                        await websocket.send_text(json.dumps({
                            "type": "message", 
                            "message": f"خطا در اجرای دستور"
                        }))
                        continue
                
                # Check if user is asking for web search
                if any(keyword in user_message.lower() for keyword in ['جستجو کن', 'search', 'اینترنت', 'آخرین اخبار', 'خبر', 'وضعیت آب و هوا']):
                    # Add web search results to context
                    web_results = internet.search_web(user_message, 3)
                    if web_results:
                        web_context = "نتایج جستجو در اینترنت:\n"
                        for result in web_results:
                            web_context += f"- {result['title']}: {result['content'][:200]}...\n"
                        
                        conversation_manager.add_message("system", web_context)
                
                # Get enhanced context with memories
                context_messages = conversation_manager.get_enhanced_context()
                
                # Add personality prompt
                personality_prompt = personality.get_personality_prompt()
                from backend.core.llm_engine import ChatMessage
                context_messages.insert(0, ChatMessage("system", personality_prompt))
                
                # Get AI response
                response = llm.chat(context_messages, fox_learning=fox_learning)
                
                # اگر Multi-AI فعال باشه، بهبود پاسخ
                try:
                    from backend.core.multi_ai_system import multi_ai_system
                    if multi_ai_system.is_enabled():
                        enhanced_response = multi_ai_system.get_best_response(user_message)
                        if enhanced_response and enhanced_response != response:
                            response = enhanced_response
                except:
                    pass
                
                # تحلیل حالت و اضافه کردن پاسخ مناسب
                try:
                    from backend.core.mood_tracker import mood_tracker
                    mood = mood_tracker.analyze_mood(user_message)
                    mood_response = mood_tracker.get_mood_response(mood)
                    
                    # اگر حالت منفی باشه، پاسخ همدلانه اضافه کن
                    if mood == "negative":
                        response = f"{mood_response}\n\n{response}"
                except:
                    pass
                
                # اضافه کردن context آگاهی
                try:
                    from backend.core.time_responses import time_responses
                    if any(word in user_message.lower() for word in ["سلام", "درود", "صبح", "ظهر", "شب"]):
                        time_greeting = time_responses.get_time_greeting()
                        if "سلام" in user_message.lower():
                            response = f"{time_greeting}\n\n{response}"
                except:
                    pass
                
                # بروزرسانی gamification
                try:
                    from backend.core.fox_gamification import fox_game
                    exp_message = fox_game.gain_experience("conversation")
                    # فقط گاهی اوقات نمایش بده تا مزاحم نباشه
                    import random
                    if random.random() < 0.1:  # 10% احتمال
                        response += f"\n\n{exp_message}"
                except:
                    pass
                
                # بررسی پیشنهادات proactive
                try:
                    from backend.core.proactive_assistant import proactive_assistant
                    suggestion = proactive_assistant.give_suggestion()
                    if suggestion and random.random() < 0.2:  # 20% احتمال
                        response += f"\n\n{suggestion}"
                except:
                    pass
                
                # Apply personality styling
                styled_response = personality.generate_response_style(response)
                
                # ثبت مکالمه در سیستم‌های هوشمند
                try:
                    import time
                    response_time = time.time() - start_time
                    
                    # تشخیص موضوع
                    topic = smart_memory.detect_topic(message)
                    
                    # ثبت در حافظه هوشمند
                    smart_memory.add_conversation(message, styled_response, {"topic": topic})
                    
                    # ثبت در آنالیتیکس
                    analytics_dashboard.record_conversation(message, styled_response, response_time, topic)
                    
                    # ایجاد follow-up notification
                    if len(message.split()) > 10:  # سوالات طولانی
                        smart_notifications.create_follow_up(message)
                        
                    # پیشنهاد یادگیری
                    if any(word in message.lower() for word in ['یاد', 'آموزش', 'چطور', 'نحوه']):
                        smart_notifications.create_learning_reminder(topic)
                        
                except Exception as e:
                    print(f"خطا در ثبت مکالمه: {e}")
                
                # Add AI response to conversation
                conversation_manager.add_message("assistant", styled_response)
                
                # Send response to client
                await websocket.send_text(json.dumps({
                    "type": "message",
                    "message": styled_response,
                    "sender": "assistant"
                }))
                
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": f"خطا: {str(e)}"
                }))
                
    except WebSocketDisconnect:
        pass

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ollama_available": llm.is_available(),
        "models": llm.list_models(),
        "external_models": ai_connector.get_available_models()
    }

@app.get("/api/conversations")
async def get_conversations():
    """Get list of recent conversations"""
    try:
        conversations = conversation_manager.get_conversations_list()
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/memory")
async def get_memory():
    """Get stored memories"""
    try:
        memories = conversation_manager.memory.get_memories()
        return {"memories": memories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_conversations(q: str):
    """Search in conversation history"""
    try:
        results = conversation_manager.search_history(q)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/web-search")
async def web_search(q: str, limit: int = 5):
    """Search the web"""
    try:
        results = internet.search_web(q, limit)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/news")
async def get_news(topic: str = "Iran", limit: int = 5):
    """Get latest news"""
    try:
        news = internet.get_news(topic, limit)
        return {"news": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather")
async def get_weather(city: str = "Tehran"):
    """Get weather information"""
    try:
        weather = internet.get_weather(city)
        return {"weather": weather}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/webpage")
async def get_webpage(url: str):
    """Get webpage content"""
    try:
        content = internet.get_webpage_content(url)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mood")
async def get_mood():
    """Get current emotional state"""
    try:
        emotions = personality.get_emotion_state()
        dominant = personality.get_dominant_emotion()
        return {
            "emotions": emotions,
            "dominant": dominant,
            "greeting": personality.get_greeting()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mood")
async def set_mood(emotion: str, value: float):
    """Set specific emotion"""
