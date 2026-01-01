#!/usr/bin/env python3
"""
Personal AI Assistant - CLI Interface with Voice Support
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from backend.core.llm_engine import LLMEngine, ChatMessage
from backend.core.conversation import ConversationManager
from backend.core.internet import InternetAccess
from backend.core.ai_connector import AIConnector
from backend.core.voice import VoiceManager
from backend.core.personality import PersonalitySystem
from backend.core.user_profile import UserProfile, FoxPersonality
from backend.core.introduction import FoxIntroduction
from backend.core.multi_user import MultiUserManager
from backend.config.settings import settings

console = Console()

class PersonalAI:
    def __init__(self):
        self.console = Console()
        self.llm = LLMEngine(
            model_name=settings.default_model,
            host=settings.ollama_host
        )
        self.conversation = ConversationManager()
        self.internet = InternetAccess()
        self.ai_connector = AIConnector()
        self.voice = VoiceManager()
        self.personality = PersonalitySystem()
        
        # Initialize multi-user system
        self.multi_user = MultiUserManager(self.conversation.memory.db)
        self.user_profile = self.multi_user.current_user
        self.fox_personality = None
        self.introduction = None
        self.pending_user_switch = None
        
        # Setup user profile and personality
        if self.user_profile:
            self.fox_personality = FoxPersonality(self.user_profile)
            if self.user_profile.is_first_time():
                self.introduction = FoxIntroduction(self.user_profile)
        else:
            # No users yet, will be handled in first interaction
            pass
        
    def display_welcome(self):        
        voice_status = self.voice.is_available()
        voice_info = ""
        if voice_status['speech_to_text'] and voice_status['text_to_speech']:
            voice_info = "\n🎤 پشتیبانی صوتی فعال است!"
        elif voice_status['speech_to_text']:
            voice_info = "\n🎤 تشخیص گفتار فعال است"
        elif voice_status['text_to_speech']:
            voice_info = "\n🔊 تولید گفتار فعال است"
        
        # Show introduction for first-time users or no users
        if not self.user_profile:
            # No users yet, start with first user
            intro_message = "سلام! 🦊✨\n\nمن Fox هستم! اولین باری که باهام صحبت می‌کنی؟\nاسمت چیه تا بتونم بشناسمت؟"
            self.console.print(Panel(intro_message, title="🦊 Fox - آشنایی", border_style="cyan"))
            return
        elif self.introduction:
            intro_message = self.introduction.start_introduction()
            self.console.print(Panel(intro_message, title="🦊 Fox - آشنایی", border_style="cyan"))
            return
        
        # Show user info
        users = self.multi_user.get_all_users()
        user_info = f"کاربر فعال: {self.user_profile.get_name()}"
        if len(users) > 1:
            other_users = [u['name'] for u in users if u['name'] != self.user_profile.get_name()]
            user_info += f" | سایر کاربران: {', '.join(other_users)}"
        
        welcome_text = f"""
# 🦊 Fox - دستیار هوش مصنوعی شخصی

{self.fox_personality.get_greeting_style()}{voice_info}

**👤 {user_info}**

**دستورات موجود:**
- `/help` - نمایش راهنما
- `/models` - لیست مدل‌های موجود
- `/history` - نمایش تاریخچه مکالمات
- `/search <متن>` - جستجو در تاریخچه
- `/memory` - نمایش حافظه ذخیره شده
- `/web <سوال>` - جستجو در اینترنت
- `/news [موضوع]` - دریافت اخبار
- `/weather [شهر]` - وضعیت آب و هوا
- `/url <آدرس>` - دریافت محتوای صفحه وب
- `/compare <سوال>` - مقایسه پاسخ AI های مختلف
- `/voice` - شروع مکالمه صوتی
- `/speak <متن>` - تولید گفتار
- `/listen` - گوش دادن به گفتار
- `/mood` - نمایش وضعیت احساسی
- `/feel <احساس> <مقدار>` - تنظیم احساس (0-10)
- `/happy`, `/sad`, `/excited`, `/serious` - تغییر سریع حالت
- `/users` - نمایش همه کاربران
- `/switch <نام>` - تغییر کاربر فعال
- `/new` - شروع مکالمه جدید
- `/clear` - پاک کردن مکالمه فعلی
- `/quit` - خروج

برای شروع مکالمه، پیام خود را تایپ کنید...
        """
        console.print(Panel(Markdown(welcome_text), title="خوش آمدید", border_style="blue"))
    
    def handle_command(self, user_input: str) -> bool:
        """Handle special commands. Returns True if command was handled."""
        if user_input.startswith('/'):
            parts = user_input[1:].split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if command == 'help':
                self.display_welcome()
                return True
                
            elif command == 'models':
                self.show_models()
                return True
            
            elif command == 'history':
                self.show_conversation_history()
                return True
            
            elif command == 'search':
                if args:
                    self.search_history(args)
                else:
                    console.print("لطفاً متن جستجو را وارد کنید: /search <متن>", style="yellow")
                return True
            
            elif command == 'memory':
                self.show_memory()
                return True
            
            elif command == 'web':
                if args:
                    self.web_search(args)
                else:
                    console.print("لطفاً سوال خود را وارد کنید: /web <سوال>", style="yellow")
                return True
            
            elif command == 'news':
                topic = args if args else "Iran"
                self.get_news(topic)
                return True
            
            elif command == 'weather':
                city = args if args else "Tehran"
                self.get_weather(city)
                return True
            
            elif command == 'url':
                if args:
                    self.get_webpage(args)
                else:
                    console.print("لطفاً آدرس وب را وارد کنید: /url <آدرس>", style="yellow")
                return True
            
            elif command == 'compare':
                if args:
                    self.compare_ai_responses(args)
                else:
                    console.print("لطفاً سوال خود را وارد کنید: /compare <سوال>", style="yellow")
                return True
            
            elif command == 'voice':
                self.start_voice_conversation()
                return True
            
            elif command == 'speak':
                if args:
                    self.speak_text(args)
                else:
                    console.print("لطفاً متن را وارد کنید: /speak <متن>", style="yellow")
                return True
            
            elif command == 'listen':
                self.listen_to_speech()
                return True
            
            elif command == 'mood':
                self.show_mood()
                return True
            
            elif command == 'feel':
                if args:
                    parts = args.split(' ', 1)
                    if len(parts) == 2:
                        emotion, value = parts[0], parts[1]
                        try:
                            value = float(value)
                            result = self.personality.set_emotion(emotion, value)
                            console.print(result, style="green")
                        except ValueError:
                            console.print("مقدار باید عدد باشد (0-10)", style="red")
                    else:
                        console.print("استفاده: /feel <احساس> <مقدار>", style="yellow")
                else:
                    console.print("استفاده: /feel <احساس> <مقدار>", style="yellow")
                return True
            
            elif command in ['happy', 'sad', 'excited', 'serious', 'funny']:
                self.quick_mood_change(command)
                return True
            
            elif command == 'reset_mood':
                result = self.personality.reset_emotions()
                console.print(result, style="green")
                return True
            
            elif command == 'users':
                self.show_users()
                return True
            
            elif command == 'switch':
                if parts and len(parts) > 1:
                    user_name = ' '.join(parts[1:])
                    self.switch_to_user(user_name)
                else:
                    console.print("استفاده: /switch <نام کاربر>", style="yellow")
                return True
            
            elif command == 'new':
                session_id = self.conversation.start_new_session()
                console.print(f"✅ مکالمه جدید شروع شد: {session_id[:8]}...", style="green")
                return True
                
            elif command == 'clear':
                session_id = self.conversation.start_new_session()
                console.print("✅ مکالمه فعلی پاک شد", style="green")
                return True
                
            elif command == 'quit':
                console.print("خداحافظ! 👋", style="blue")
                return True
                
            else:
                console.print(f"دستور نامعتبر: {command}", style="red")
                return True
        
        return False
    
    def show_users(self):
        """نمایش همه کاربران"""
        users = self.multi_user.get_all_users()
        
        if not users:
            self.console.print("هیچ کاربری ثبت نشده است.", style="yellow")
            return
        
        table = Table(title="👥 کاربران Fox")
        table.add_column("نام", style="cyan")
        table.add_column("وضعیت", style="green")
        table.add_column("تاریخ ایجاد", style="blue")
        table.add_column("آخرین بازدید", style="magenta")
        
        for user in users:
            status = "🟢 فعال" if (self.user_profile and user['name'] == self.user_profile.get_name()) else "⚪ غیرفعال"
            created = user['created_at'][:10] if 'created_at' in user else "نامشخص"
            last_seen = user['last_seen'][:10] if 'last_seen' in user else "نامشخص"
            
            table.add_row(user['name'], status, created, last_seen)
        
        self.console.print(table)
    
    def switch_to_user(self, user_name: str):
        """تغییر به کاربر مشخص"""
        try:
            old_user = self.user_profile.get_name() if self.user_profile else "کاربر جدید"
            
            # Switch user
            self.user_profile, is_new_user = self.multi_user.switch_user(user_name)
            self.fox_personality = FoxPersonality(self.user_profile)
            
            if is_new_user:
                # New user needs introduction
                self.introduction = FoxIntroduction(self.user_profile)
                intro_message = self.introduction.start_introduction()
                self.console.print(Panel(intro_message, title=f"🦊 Fox - آشنایی با {user_name}", border_style="cyan"))
            else:
                # Existing user
                greeting = self.fox_personality.get_greeting_style()
                switch_message = f"سلام دوباره {user_name}! 🦊\n\n{greeting}\n\nخوشحالم که برگشتی!"
                self.console.print(Panel(switch_message, title=f"🔄 تغییر کاربر: {old_user} → {user_name}", border_style="green"))
            
        except Exception as e:
            self.console.print(f"خطا در تغییر کاربر: {e}", style="red")
    
    def start_voice_conversation(self):
        """Start voice conversation mode"""
        if not self.voice.is_available()['speech_to_text']:
            console.print("❌ تشخیص گفتار در دسترس نیست", style="red")
            console.print("برای نصب: pip install SpeechRecognition pyaudio", style="yellow")
            return
        
        console.print("🎤 مکالمه صوتی شروع شد", style="green")
        console.print("💡 برای خروج 'خروج' یا Ctrl+C", style="dim")
        
        def chat_callback(text):
            # Handle pending user switch confirmation
            if self.pending_user_switch:
                if any(word in text.lower() for word in ['بله', 'آره', 'yes']):
                    # Confirm switch
                    user_name = self.pending_user_switch
                    self.pending_user_switch = None
                    self.switch_to_user(user_name)
                    return
                elif any(word in text.lower() for word in ['نه', 'خیر', 'no']):
                    # Cancel switch
                    self.pending_user_switch = None
                    console.print("باشه! ادامه می‌دیم با همین کاربر 🦊", style="green")
                    return
                else:
                    # Maybe they gave their real name
                    potential_name = self.multi_user.detect_user_change(text)
                    if potential_name:
                        self.pending_user_switch = None
                        self.switch_to_user(potential_name)
                        return
            
            # Handle no current user (first time setup)
            if not self.user_profile:
                potential_name = self.multi_user.detect_user_change(text)
                if potential_name:
                    self.switch_to_user(potential_name)
                    return
                else:
                    console.print("لطفاً اسمتان را بگویید تا بتوانم شما را بشناسم! 🦊", style="yellow")
                    return
            
            # Handle introduction process
            if self.introduction and not self.introduction.is_introduction_complete():
                response = self.introduction.process_response(text)
                if self.introduction.is_introduction_complete():
                    self.introduction = None
                    # Update relationship level
                    self.user_profile.update_relationship_level(1)
                self.console.print(Panel(response, title="🦊 Fox", border_style="cyan"))
                return
            
            # Check for user switch suggestion
            suggested_user = self.multi_user.suggest_user_switch(text)
            if suggested_user:
                self.pending_user_switch = suggested_user
                switch_message = self.multi_user.get_switch_message(suggested_user)
                console.print(Panel(switch_message, title="🤔 تغییر کاربر؟", border_style="yellow"))
                return
            
            # Record interaction
            self.user_profile.record_interaction()
            
            # Add user message
            self.conversation.add_message("user", text)
            
            # Check for web search
            if any(keyword in text.lower() for keyword in ['جستجو کن', 'search', 'اینترنت', 'آخرین اخبار']):
                web_results = self.internet.search_web(text, 3)
                if web_results:
                    web_context = "نتایج جستجو در اینترنت:\n"
                    for result in web_results:
                        web_context += f"- {result['title']}: {result['content'][:200]}...\n"
                    self.conversation.add_message("system", web_context)
            
            # Get AI response with personality
            context_messages = self.conversation.get_enhanced_context()
            
            # Add personality context
            personality_context = f"""
شما Fox هستید، دستیار هوشمند فارسی‌زبان که با {self.user_profile.get_name()} دوست هستید.
سطح رابطه: {self.user_profile.get_relationship_status()}
علایق کاربر: {', '.join(self.user_profile.profile['interests'])}
ویژگی‌های شخصیتی کاربر: {', '.join(self.user_profile.profile['personality_traits'])}

سبک پاسخ: {self.fox_personality.get_response_style()}
"""
            
            context_messages.append({"role": "system", "content": personality_context})
            
            response = self.llm.chat(context_messages)
            
            # Add proactive question if appropriate
            if self.fox_personality.should_ask_question() and len(response) < 200:
                import random
                if random.random() < 0.3:  # 30% chance
                    question = self.fox_personality.get_random_question()
                    response += f"\n\n{question}"
            
            # Add AI response
            self.conversation.add_message("assistant", response)
            
            return response
        
        self.voice.start_voice_conversation(chat_callback)
    
    def speak_text(self, text: str):
        """Speak the given text"""
        if not self.voice.is_available()['text_to_speech']:
            console.print("❌ تولید گفتار در دسترس نیست", style="red")
            console.print("برای نصب: pip install pyttsx3", style="yellow")
            return
        
        console.print(f"🔊 در حال گفتن: {text}", style="blue")
        success = self.voice.speak(text)
        
        if success:
            console.print("✅ گفتار تولید شد", style="green")
        else:
            console.print("❌ خطا در تولید گفتار", style="red")
    
    def check_ollama_status(self):
        """Check if Ollama is available"""
        if not self.llm.is_available():
            console.print("❌ Ollama در دسترس نیست. لطفاً ابتدا Ollama را راه‌اندازی کنید.", style="red")
            console.print("برای راه‌اندازی: docker start ollama", style="yellow")
            return False
        
        # Check if model exists
        models = self.llm.list_models()
        if settings.default_model not in models:
            console.print(f"❌ مدل {settings.default_model} یافت نشد.", style="red")
            console.print(f"برای دانلود: docker exec ollama ollama pull {settings.default_model}", style="yellow")
            return False
            
        console.print("✅ Ollama آماده است", style="green")
        return True
    
    def show_models(self):
        """Show available models"""
        local_models = self.llm.list_models()
        external_models = self.ai_connector.get_available_models()
        
        console.print("مدل‌های محلی:", style="blue")
        if local_models:
            for model in local_models:
                marker = "✅" if model == settings.default_model else "  "
                console.print(f"{marker} {model}")
        else:
            console.print("هیچ مدلی یافت نشد", style="red")
        
        if external_models:
            console.print("\nمدل‌های خارجی:", style="blue")
            for model in external_models:
                console.print(f"🌐 {model}")
    
    def web_search(self, query: str):
        """Search the web"""
        console.print(f"🔍 جستجو در اینترنت: {query}", style="blue")
        
        results = self.internet.search_web(query)
        
        if results:
            for i, result in enumerate(results, 1):
                console.print(f"\n{i}. {result['title']}", style="cyan")
                console.print(f"   {result['content'][:200]}...")
                if result['url']:
                    console.print(f"   🔗 {result['url']}", style="dim")
        else:
            console.print("هیچ نتیجه‌ای یافت نشد", style="yellow")
    
    def get_news(self, topic: str):
        """Get latest news"""
        console.print(f"📰 دریافت اخبار: {topic}", style="blue")
        
        news = self.internet.get_news(topic)
        
        for i, item in enumerate(news, 1):
            console.print(f"\n{i}. {item['title']}", style="cyan")
            console.print(f"   {item['content'][:200]}...")
            if item['url']:
                console.print(f"   🔗 {item['url']}", style="dim")
    
    def get_weather(self, city: str):
        """Get weather information"""
        console.print(f"🌤️ وضعیت آب و هوا: {city}", style="blue")
        
        weather = self.internet.get_weather(city)
        console.print(f"📍 {weather['city']}")
        console.print(f"   {weather['info']}")
    
    def get_webpage(self, url: str):
        """Get webpage content"""
        console.print(f"📄 دریافت محتوای صفحه: {url}", style="blue")
        
        content = self.internet.get_webpage_content(url)
        console.print(f"📝 {content['title']}", style="cyan")
        console.print(f"   {content['content'][:500]}...")
        console.print(f"   وضعیت: {content['status']}", style="dim")
    
    def compare_ai_responses(self, question: str):
        """Compare responses from different AI models"""
        console.print(f"🤖 مقایسه پاسخ‌های AI: {question}", style="blue")
        
        messages = [{"role": "user", "content": question}]
        responses = self.ai_connector.compare_responses(messages)
        
        if responses:
            for model, response in responses.items():
                console.print(f"\n🤖 {model}:", style="cyan")
                console.print(f"   {response[:300]}...")
        else:
            console.print("هیچ API خارجی پیکربندی نشده است", style="yellow")
    
    def show_conversation_history(self):
        """Show recent conversations"""
        conversations = self.conversation.get_conversations_list()
        
        if not conversations:
            console.print("هیچ مکالمه‌ای یافت نشد", style="yellow")
            return
        
        table = Table(title="تاریخچه مکالمات")
        table.add_column("عنوان", style="cyan")
        table.add_column("تعداد پیام", justify="center")
        table.add_column("آخرین بروزرسانی", style="dim")
        
        for conv in conversations[:10]:
            table.add_row(
                conv['title'][:50] + "..." if len(conv['title']) > 50 else conv['title'],
                str(conv['message_count']),
                conv['updated_at'][:16].replace('T', ' ')
            )
        
        console.print(table)
    
    def search_history(self, query: str):
        """Search in conversation history"""
        results = self.conversation.search_history(query)
        
        if not results:
            console.print(f"هیچ نتیجه‌ای برای '{query}' یافت نشد", style="yellow")
            return
        
        console.print(f"نتایج جستجو برای '{query}':", style="blue")
        for result in results[:5]:
            console.print(f"📝 {result['title']}")
            console.print(f"   {result['content']}")
            console.print(f"   🕒 {result['timestamp'][:16].replace('T', ' ')}")
            console.print()
    
    def show_memory(self):
        """Show stored memories"""
        memories = self.conversation.memory.get_memories()
        
        if not memories:
            console.print("هیچ حافظه‌ای ذخیره نشده", style="yellow")
            return
        
        table = Table(title="حافظه ذخیره شده")
        table.add_column("کلید", style="cyan")
        table.add_column("مقدار", style="white")
        table.add_column("دسته", style="dim")
        table.add_column("اهمیت", justify="center")
        
        for mem in memories:
            table.add_row(
                mem['key'],
                mem['value'][:50] + "..." if len(mem['value']) > 50 else mem['value'],
                mem['category'],
                str(mem['importance'])
            )
        
        console.print(table)
        """Listen to speech and convert to text"""
        if not self.voice.is_available()['speech_to_text']:
            console.print("❌ تشخیص گفتار در دسترس نیست", style="red")
            return
        
        console.print("🎤 آماده گوش دادن...", style="blue")
        text = self.voice.listen_once()
        
        if text:
            console.print(f"✅ شنیده شد: {text}", style="green")
            return text
        else:
            console.print("❌ متنی تشخیص داده نشد", style="red")
            return None
    
    def show_models(self):
        """Show available models"""
        local_models = self.llm.list_models()
        external_models = self.ai_connector.get_available_models()
        
        console.print("مدل‌های محلی:", style="blue")
        if local_models:
            for model in local_models:
                marker = "✅" if model == settings.default_model else "  "
                console.print(f"{marker} {model}")
        else:
            console.print("هیچ مدلی یافت نشد", style="red")
        
        if external_models:
            console.print("\nمدل‌های خارجی:", style="blue")
            for model in external_models:
                console.print(f"🌐 {model}")
    
    def web_search(self, query: str):
        """Search the web"""
        console.print(f"🔍 جستجو در اینترنت: {query}", style="blue")
        
        results = self.internet.search_web(query)
        
        if results:
            for i, result in enumerate(results, 1):
                console.print(f"\n{i}. {result['title']}", style="cyan")
                console.print(f"   {result['content'][:200]}...")
                if result['url']:
                    console.print(f"   🔗 {result['url']}", style="dim")
        else:
            console.print("هیچ نتیجه‌ای یافت نشد", style="yellow")
    
    def get_news(self, topic: str):
        """Get latest news"""
        console.print(f"📰 دریافت اخبار: {topic}", style="blue")
        
        news = self.internet.get_news(topic)
        
        for i, item in enumerate(news, 1):
            console.print(f"\n{i}. {item['title']}", style="cyan")
            console.print(f"   {item['content'][:200]}...")
            if item['url']:
                console.print(f"   🔗 {item['url']}", style="dim")
    
    def get_weather(self, city: str):
        """Get weather information"""
        console.print(f"🌤️ وضعیت آب و هوا: {city}", style="blue")
        
        weather = self.internet.get_weather(city)
        console.print(f"📍 {weather['city']}")
        console.print(f"   {weather['info']}")
    
    def get_webpage(self, url: str):
        """Get webpage content"""
        console.print(f"📄 دریافت محتوای صفحه: {url}", style="blue")
        
        content = self.internet.get_webpage_content(url)
        console.print(f"📝 {content['title']}", style="cyan")
        console.print(f"   {content['content'][:500]}...")
        console.print(f"   وضعیت: {content['status']}", style="dim")
    
    def compare_ai_responses(self, question: str):
        """Compare responses from different AI models"""
        console.print(f"🤖 مقایسه پاسخ‌های AI: {question}", style="blue")
        
        messages = [{"role": "user", "content": question}]
        responses = self.ai_connector.compare_responses(messages)
        
        if responses:
            for model, response in responses.items():
                console.print(f"\n🤖 {model}:", style="cyan")
                console.print(f"   {response[:300]}...")
        else:
            console.print("هیچ API خارجی پیکربندی نشده است", style="yellow")
    
    def show_conversation_history(self):
        """Show recent conversations"""
        conversations = self.conversation.get_conversations_list()
        
        if not conversations:
            console.print("هیچ مکالمه‌ای یافت نشد", style="yellow")
            return
        
        table = Table(title="تاریخچه مکالمات")
        table.add_column("عنوان", style="cyan")
        table.add_column("تعداد پیام", justify="center")
        table.add_column("آخرین بروزرسانی", style="dim")
        
        for conv in conversations[:10]:
            table.add_row(
                conv['title'][:50] + "..." if len(conv['title']) > 50 else conv['title'],
                str(conv['message_count']),
                conv['updated_at'][:16].replace('T', ' ')
            )
        
        console.print(table)
    
    def search_history(self, query: str):
        """Search in conversation history"""
        results = self.conversation.search_history(query)
        
        if not results:
            console.print(f"هیچ نتیجه‌ای برای '{query}' یافت نشد", style="yellow")
            return
        
        console.print(f"نتایج جستجو برای '{query}':", style="blue")
        for result in results[:5]:
            console.print(f"📝 {result['title']}")
            console.print(f"   {result['content']}")
            console.print(f"   🕒 {result['timestamp'][:16].replace('T', ' ')}")
            console.print()
    
    def show_memory(self):
        """Show stored memories"""
        memories = self.conversation.memory.get_memories()
        
        if not memories:
            console.print("هیچ حافظه‌ای ذخیره نشده", style="yellow")
            return
        
        table = Table(title="حافظه ذخیره شده")
        table.add_column("کلید", style="cyan")
        table.add_column("مقدار", style="white")
        table.add_column("دسته", style="dim")
        table.add_column("اهمیت", justify="center")
        
        for mem in memories:
            table.add_row(
                mem['key'],
                mem['value'][:50] + "..." if len(mem['value']) > 50 else mem['value'],
                mem['category'],
                str(mem['importance'])
            )
        
        console.print(table)
    
    def chat_loop(self):
        """Main chat loop"""
        self.display_welcome()
        
        if not self.check_ollama_status():
            return
        
        # Start new session
        self.conversation.start_new_session()
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold blue]شما[/bold blue]")
                
                if not user_input.strip():
                    continue
                
                # Handle commands
                if self.handle_command(user_input):
                    if user_input.lower() == '/quit':
                        break
                    continue
                
                # Add user message to conversation
                self.conversation.add_message("user", user_input)
                
                # Analyze user input for emotional context
                self.personality.analyze_user_input(user_input)
                
                # Check if user is asking for web search
                if any(keyword in user_input.lower() for keyword in ['جستجو کن', 'search', 'اینترنت', 'آخرین اخبار']):
                    # Add web search results to context
                    web_results = self.internet.search_web(user_input, 3)
                    if web_results:
                        web_context = "نتایج جستجو در اینترنت:\n"
                        for result in web_results:
                            web_context += f"- {result['title']}: {result['content'][:200]}...\n"
                        
                        self.conversation.add_message("system", web_context)
                
                # Get enhanced context with memories AND personality
                context_messages = self.conversation.get_enhanced_context()
                
                # Add personality prompt
                personality_prompt = self.personality.get_personality_prompt()
                context_messages.insert(0, ChatMessage("system", personality_prompt))
                
                # Get AI response
                console.print("\n[bold green]Fox[/bold green]: ", end="")
                
                try:
                    response = self.llm.chat(context_messages)
                    
                    # Apply personality styling to response
                    styled_response = self.personality.generate_response_style(response)
                    
                    console.print(styled_response)
                    
                    # Add AI response to conversation
                    self.conversation.add_message("assistant", styled_response)
                    
                except Exception as e:
                    console.print(f"خطا: {str(e)}", style="red")
                
            except KeyboardInterrupt:
                console.print("\n\nخداحافظ! 👋", style="blue")
                break
            except EOFError:
                break
    
    def show_mood(self):
        """Show current emotional state"""
        emotions = self.personality.get_emotion_state()
        dominant = self.personality.get_dominant_emotion()
        
        table = Table(title="🦊 وضعیت احساسی Fox")
        table.add_column("احساس", style="cyan")
        table.add_column("مقدار", justify="center")
        table.add_column("نمودار", style="blue")
        
        emotion_names = {
            "happiness": "خوشحالی",
            "sadness": "غم", 
            "anger": "عصبانیت",
            "excitement": "هیجان",
            "humor": "شوخ‌طبعی",
            "seriousness": "جدیت",
            "friendliness": "صمیمیت",
            "curiosity": "کنجکاوی"
        }
        
        for emotion, value in emotions.items():
            name = emotion_names.get(emotion, emotion)
            bar = "█" * int(value) + "░" * (10 - int(value))
            marker = "👑" if emotion == dominant else ""
            
            table.add_row(
                f"{marker} {name}",
                f"{value:.1f}/10",
                bar
            )
        
        console.print(table)
        console.print(f"\n🎭 حالت غالب: {emotion_names.get(dominant, dominant)}", style="bold blue")
    
    def quick_mood_change(self, mood: str):
        """Quick mood changes"""
        changes = {
            "happy": {"happiness": 8.0, "sadness": 2.0, "humor": 7.0},
            "sad": {"sadness": 7.0, "happiness": 3.0, "seriousness": 6.0},
            "excited": {"excitement": 9.0, "happiness": 7.0, "curiosity": 8.0},
            "serious": {"seriousness": 9.0, "humor": 2.0, "friendliness": 5.0},
            "funny": {"humor": 9.0, "happiness": 8.0, "excitement": 6.0}
        }
        
        if mood in changes:
            for emotion, value in changes[mood].items():
                self.personality.set_emotion(emotion, value)
            
            console.print(f"🎭 Fox حالا {mood} است!", style="green")
            
            # Show a mood-appropriate message
            greetings = {
                "happy": "یه‌هو! حالم خیلی خوبه! 😊",
                "sad": "اوه... کمی غمگینم... 😔", 
                "excited": "واااای! چقدر هیجان‌زده‌ام! 🚀",
                "serious": "حالا در حالت جدی هستم. 🎯",
                "funny": "آماده شوخی و خنده! 😄"
            }
            
            console.print(f"🦊 {greetings.get(mood, 'حالتم تغییر کرد!')}", style="blue")

def main():
    ai = PersonalAI()
    ai.chat_loop()

if __name__ == "__main__":
    main()
