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
from backend.core.fox_experience import FoxExperienceSystem
from backend.core.fox_learning import FoxLearningSystem
from backend.commands.api_commands import handle_api_command
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
            self.fox_experience = FoxExperienceSystem(self.user_profile)
            self.fox_learning = FoxLearningSystem(self.user_profile)
            if self.user_profile.is_first_time():
                self.introduction = FoxIntroduction(self.user_profile)
        else:
            # No users yet, will be handled in first interaction
            self.fox_experience = None
            self.fox_learning = None
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
- `/status` - نمایش وضعیت کامل Fox
- `/set <پارامتر> <مقدار>` - تغییر تنظیمات
- `/experience` - نمایش تجربه و سن Fox
- `/boost <ماه>` - تقویت هوش Fox
- `/age <روز>` - پیر کردن Fox
- `/pretrain` - پیش‌آموزش Fox با دیتاست
- `/teach <کلید> <پاسخ>` - آموزش پاسخ خاص
- `/learn <موضوع> <حقیقت>` - آموزش دانش جدید
- `/learned` - نمایش آمار یادگیری
- `/recall <موضوع>` - یادآوری مکالمات قبلی
- `/voices` - نمایش صداهای موجود
- `/voice_set <شماره>` - تغییر صدا
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
                    console.print("لطفاً نام کاربر را وارد کنید: /switch <نام>", style="yellow")
                return True
            
            elif command == 'api':
                result = handle_api_command(user_input.split())
                console.print(result, style="cyan")
                return True
                else:
                    console.print("استفاده: /switch <نام کاربر>", style="yellow")
                return True
            
            elif command == 'status':
                self.show_status()
                return True
            
            elif command == 'set':
                if parts and len(parts) >= 3:
                    param = parts[1].lower()
                    value = ' '.join(parts[2:])
                    self.set_parameter(param, value)
                else:
                    console.print("استفاده: /set <پارامتر> <مقدار>", style="yellow")
                    console.print("مثال: /set relationship 5", style="dim")
                return True
            
            elif command == 'experience':
                self.show_experience()
                return True
            
            elif command == 'boost':
                if parts and len(parts) > 1:
                    try:
                        months = int(parts[1])
                        self.boost_fox(months)
                    except ValueError:
                        console.print("❌ لطفاً عدد صحیح وارد کنید", style="red")
                else:
                    self.boost_fox(1)  # Default 1 month
                return True
            
            elif command == 'age':
                if parts and len(parts) > 1:
                    try:
                        days = int(parts[1])
                        self.age_fox(days)
                    except ValueError:
                        console.print("❌ لطفاً عدد صحیح وارد کنید", style="red")
                else:
                    self.age_fox(30)  # Default 30 days = 1 month
                return True
            
            elif command == 'pretrain':
                self.pretrain_fox()
                return True
            
            elif command == 'teach':
                if len(parts) >= 2:
                    # Split on first space after command
                    rest = user_input[6:].strip()  # Remove "/teach"
                    if ' ' in rest:
                        trigger, response = rest.split(' ', 1)
                        result = self.fox_learning.teach_response(trigger, response)
                        console.print(result, style="green")
                    else:
                        console.print("استفاده: /teach <کلمه کلیدی> <پاسخ>", style="yellow")
                        console.print("مثال: /teach سلام سلام عزیز! چطوری؟", style="dim")
                else:
                    console.print("استفاده: /teach <کلمه کلیدی> <پاسخ>", style="yellow")
                    console.print("مثال: /teach سلام سلام عزیز! چطوری؟", style="dim")
                return True
            
            elif command == 'learn':
                if len(parts) >= 2:
                    # Split on first space after command
                    rest = user_input[6:].strip()  # Remove "/learn"
                    if ' ' in rest:
                        topic, fact = rest.split(' ', 1)
                        result = self.fox_learning.teach_fact(topic, fact)
                        console.print(result, style="green")
                    else:
                        console.print("استفاده: /learn <موضوع> <حقیقت>", style="yellow")
                        console.print("مثال: /learn ایران پایتخت ایران تهران است", style="dim")
                else:
                    console.print("استفاده: /learn <موضوع> <حقیقت>", style="yellow")
                    console.print("مثال: /learn ایران پایتخت ایران تهران است", style="dim")
                return True
            
            elif command == 'learned':
                stats = self.fox_learning.get_learning_stats()
                console.print("\n📚 آمار یادگیری Fox:", style="bold cyan")
                console.print(f"• پاسخهای آموزش داده شده: {stats['custom_responses']}")
                console.print(f"• حقایق یادگیری شده: {stats['learned_facts']}")
                console.print(f"• اطلاعات فرهنگی: {stats['cultural_knowledge']}")
                console.print(f"• ترجیحات شخصی: {stats['personal_preferences']}")
                console.print(f"• کارهای روزمره: {stats['daily_routines']}")
                return True
            
            elif command == 'voices':
                if self.voice.tts_engine:
                    voices = self.voice.tts_engine.getProperty('voices')
                    console.print("\n🔊 صداهای موجود:", style="bold cyan")
                    for i, voice in enumerate(voices):
                        current = "✅" if voice.id == self.voice.tts_engine.getProperty('voice') else "  "
                        console.print(f"{current} {i}: {voice.name} ({voice.languages})")
                    console.print("\nبرای تغییر صدا: /voice_set <شماره>", style="dim")
                else:
                    console.print("❌ TTS در دسترس نیست", style="red")
                return True
            
            elif command == 'voice_set':
                if parts and len(parts) > 1:
                    try:
                        voice_index = int(parts[1])
                        voices = self.voice.tts_engine.getProperty('voices')
                        if 0 <= voice_index < len(voices):
                            self.voice.tts_engine.setProperty('voice', voices[voice_index].id)
                            console.print(f"✅ صدا تغییر کرد به: {voices[voice_index].name}", style="green")
                        else:
                            console.print("❌ شماره صدا نامعتبر است", style="red")
                    except:
                        console.print("❌ شماره صدا نامعتبر است", style="red")
                else:
                    console.print("استفاده: /voice_set <شماره صدا>", style="yellow")
                return True
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
                        ).order_by(desc(Message.timestamp)).limit(10).all()
                        
                        if messages:
                            console.print(f"\n🧠 یادم هست! در مورد '{search_term}' صحبت کردیم:", style="bold green")
                            for msg in reversed(messages[-3:]):
                                time_str = msg.timestamp.strftime("%Y/%m/%d %H:%M")
                                role = "شما" if msg.role == "user" else "Fox"
                                content = msg.content[:80] + "..." if len(msg.content) > 80 else msg.content
                                console.print(f"📅 {time_str} - {role}: {content}", style="dim")
                        else:
                            console.print(f"🤔 متأسفانه چیزی در مورد '{search_term}' یادم نیست", style="yellow")
                    except Exception as e:
                        console.print(f"❌ خطا در جستجو: {str(e)}", style="red")
                else:
                    console.print("استفاده: /recall <موضوع یا کلمه کلیدی>", style="yellow")
                    console.print("مثال: /recall برنامه‌نویسی", style="dim")
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
    
    def show_status(self):
        """نمایش وضعیت کامل Fox"""
        if not self.user_profile:
            self.console.print("هیچ کاربری فعال نیست.", style="yellow")
            return
        
        # User info
        table = Table(title="📊 وضعیت کامل Fox", show_header=True, header_style="bold magenta")
        table.add_column("پارامتر", style="cyan", width=20)
        table.add_column("مقدار فعلی", style="green", width=30)
        table.add_column("دستور تغییر", style="yellow", width=25)
        
        # Basic info
        table.add_row("نام کاربر", self.user_profile.get_name(), "/set name <نام>")
        table.add_row("سطح رابطه", f"{self.user_profile.get_relationship_status()} ({self.user_profile.profile['relationship_level']}/10)", "/set relationship <0-10>")
        table.add_row("تعداد تعامل", str(self.user_profile.profile['interaction_count']), "/set interactions <عدد>")
        
        # Interests
        interests = ', '.join(self.user_profile.profile['interests']) if self.user_profile.profile['interests'] else 'هیچ'
        table.add_row("علایق", interests, "/set interests <لیست>")
        
        # Personality traits
        traits = ', '.join(self.user_profile.profile['personality_traits']) if self.user_profile.profile['personality_traits'] else 'هیچ'
        table.add_row("ویژگی‌های شخصیتی", traits, "/set traits <لیست>")
        
        # Communication style
        table.add_row("سبک ارتباط", self.user_profile.profile.get('communication_style', 'friendly'), "/set style <سبک>")
        
        # Last interaction
        last_interaction = self.user_profile.profile.get('last_interaction')
        if last_interaction:
            last_interaction = last_interaction[:19].replace('T', ' ')
        else:
            last_interaction = 'هرگز'
        table.add_row("آخرین تعامل", last_interaction, "خودکار")
        
        self.console.print(table)
        
        # Personality/Mood status
        mood_table = Table(title="🎭 وضعیت احساسی", show_header=True, header_style="bold blue")
        mood_table.add_column("احساس", style="cyan", width=15)
        mood_table.add_column("مقدار", style="green", width=10)
        mood_table.add_column("نمودار", style="yellow", width=20)
        mood_table.add_column("دستور تغییر", style="magenta", width=20)
        
        emotions = self.personality.get_current_emotions()
        for emotion, value in emotions.items():
            bar = "█" * int(value) + "░" * (10 - int(value))
            persian_emotion = {
                'happiness': 'خوشحالی',
                'sadness': 'غم', 
                'anger': 'عصبانیت',
                'excitement': 'هیجان',
                'humor': 'شوخی',
                'seriousness': 'جدیت',
                'friendliness': 'صمیمیت',
                'curiosity': 'کنجکاوی'
            }.get(emotion, emotion)
            
            mood_table.add_row(persian_emotion, f"{value}/10", bar, f"/feel {emotion} <0-10>")
        
        self.console.print(mood_table)
        
        # Usage examples
        self.console.print("\n💡 مثال‌های استفاده:", style="bold")
        self.console.print("• /set relationship 8 - افزایش سطح رابطه", style="dim")
        self.console.print("• /set interests برنامه‌نویسی,موسیقی,ورزش - تغییر علایق", style="dim")
        self.console.print("• /feel happiness 9 - افزایش خوشحالی", style="dim")
    
    def set_parameter(self, param: str, value: str):
        """تنظیم پارامترهای Fox"""
        if not self.user_profile:
            self.console.print("هیچ کاربری فعال نیست.", style="red")
            return
        
        try:
            if param == 'name':
                old_name = self.user_profile.get_name()
                self.user_profile.profile['name'] = value
                self.user_profile.save_profile()
                self.console.print(f"✅ نام از '{old_name}' به '{value}' تغییر یافت", style="green")
            
            elif param == 'relationship':
                level = int(value)
                if 0 <= level <= 10:
                    old_level = self.user_profile.profile['relationship_level']
                    self.user_profile.profile['relationship_level'] = level
                    self.user_profile.save_profile()
                    self.console.print(f"✅ سطح رابطه از {old_level} به {level} تغییر یافت", style="green")
                else:
                    self.console.print("❌ سطح رابطه باید بین 0 تا 10 باشد", style="red")
            
            elif param == 'interactions':
                count = int(value)
                if count >= 0:
                    old_count = self.user_profile.profile['interaction_count']
                    self.user_profile.profile['interaction_count'] = count
                    self.user_profile.save_profile()
                    self.console.print(f"✅ تعداد تعامل از {old_count} به {count} تغییر یافت", style="green")
                else:
                    self.console.print("❌ تعداد تعامل نمی‌تواند منفی باشد", style="red")
            
            elif param == 'interests':
                interests = [i.strip() for i in value.split(',') if i.strip()]
                old_interests = self.user_profile.profile['interests']
                self.user_profile.profile['interests'] = interests
                self.user_profile.save_profile()
                self.console.print(f"✅ علایق تغییر یافت: {', '.join(interests)}", style="green")
            
            elif param == 'traits':
                traits = [t.strip() for t in value.split(',') if t.strip()]
                old_traits = self.user_profile.profile['personality_traits']
                self.user_profile.profile['personality_traits'] = traits
                self.user_profile.save_profile()
                self.console.print(f"✅ ویژگی‌های شخصیتی تغییر یافت: {', '.join(traits)}", style="green")
            
            elif param == 'style':
                valid_styles = ['friendly', 'formal', 'casual', 'professional']
                if value.lower() in valid_styles:
                    old_style = self.user_profile.profile.get('communication_style', 'friendly')
                    self.user_profile.profile['communication_style'] = value.lower()
                    self.user_profile.save_profile()
                    self.console.print(f"✅ سبک ارتباط از '{old_style}' به '{value}' تغییر یافت", style="green")
                else:
                    self.console.print(f"❌ سبک معتبر: {', '.join(valid_styles)}", style="red")
            
            else:
                self.console.print(f"❌ پارامتر نامعتبر: {param}", style="red")
                self.console.print("پارامترهای معتبر: name, relationship, interactions, interests, traits, style", style="yellow")
        
        except ValueError:
            self.console.print("❌ مقدار نامعتبر. لطفاً عدد صحیح وارد کنید.", style="red")
        except Exception as e:
            self.console.print(f"❌ خطا: {e}", style="red")
    
    def show_experience(self):
        """نمایش تجربه و سن Fox"""
        if not self.fox_experience:
            self.console.print("سیستم تجربه در دسترس نیست.", style="red")
            return
        
        exp_data = self.fox_experience.get_experience_level()
        
        # Experience table
        table = Table(title="🧠 تجربه و سن Fox", show_header=True, header_style="bold cyan")
        table.add_column("ویژگی", style="yellow", width=20)
        table.add_column("مقدار", style="green", width=25)
        table.add_column("توضیح", style="blue", width=30)
        
        table.add_row("سن (روز)", str(exp_data['days_old']), f"معادل {exp_data['days_old']} روز زندگی")
        table.add_row("سن (ماه)", str(exp_data['months_old']), f"معادل {exp_data['months_old']} ماه تجربه")
        table.add_row("سن (سال)", str(exp_data['years_old']), f"معادل {exp_data['years_old']} سال دانش")
        
        table.add_row("سطح تجربه", exp_data['experience_level'], "میزان دانش و تجربه")
        table.add_row("کل تعامل", str(exp_data['total_interactions']), "تعداد کل مکالمات")
        table.add_row("تجربه واقعی", str(exp_data['real_experience']), "از مکالمات واقعی")
        table.add_row("تجربه مصنوعی", str(exp_data['artificial_experience']), "از تقویت هوش")
        
        self.console.print(table)
        
        # Experience levels explanation
        levels_table = Table(title="📊 سطوح تجربه", show_header=True, header_style="bold magenta")
        levels_table.add_column("سطح", style="cyan")
        levels_table.add_column("تعامل مورد نیاز", style="yellow")
        levels_table.add_column("توانایی‌ها", style="green")
        
        levels_table.add_row("تازه‌کار", "0-100", "پاسخ‌های ساده")
        levels_table.add_row("مبتدی", "100-500", "درک بهتر مکالمه")
        levels_table.add_row("متوسط", "500-1000", "پاسخ‌های متنوع")
        levels_table.add_row("پیشرفته", "1000-2000", "درک عمیق‌تر")
        levels_table.add_row("خبره", "2000-5000", "پاسخ‌های پیچیده")
        levels_table.add_row("استاد", "5000+", "حکمت و تجربه بالا")
        
        self.console.print(levels_table)
        
        # Commands help
        self.console.print("\n💡 دستورات تجربه:", style="bold")
        self.console.print("• /boost 3 - تقویت هوش معادل 3 ماه", style="dim")
        self.console.print("• /age 90 - پیر کردن معادل 90 روز", style="dim")
    
    def boost_fox(self, months: int):
        """تقویت هوش Fox"""
        if not self.fox_experience:
            self.console.print("سیستم تجربه در دسترس نیست.", style="red")
            return
        
        if months < 1 or months > 12:
            self.console.print("❌ تعداد ماه باید بین 1 تا 12 باشد", style="red")
            return
        
        result = self.fox_experience.boost_fox_intelligence(months)
        
        self.console.print(f"🚀 Fox {months} ماه باهوش‌تر شد!", style="bold green")
        self.console.print(f"• تجربه اضافه شده: {result['experience_gained']}", style="green")
        self.console.print(f"• سطح رابطه: {result['old_level']} → {result['new_level']}", style="cyan")
        self.console.print(f"• تعامل: {result['old_interactions']} → {result['new_interactions']}", style="yellow")
        
        # Update fox_personality with new profile
        self.fox_personality = FoxPersonality(self.user_profile)
    
    def age_fox(self, days: int):
        """پیر کردن Fox"""
        if not self.fox_experience:
            self.console.print("سیستم تجربه در دسترس نیست.", style="red")
            return
        
        if days < 1 or days > 365:
            self.console.print("❌ تعداد روز باید بین 1 تا 365 باشد", style="red")
            return
        
        result = self.fox_experience.accelerate_experience(days)
        
        self.console.print(f"⏰ Fox {days} روز پیرتر شد!", style="bold blue")
        self.console.print(f"• تجربه اضافه شده: {result['experience_gained']}", style="blue")
        self.console.print(f"• سطح رابطه: {result['old_level']} → {result['new_level']}", style="cyan")
        self.console.print(f"• تعامل: {result['old_interactions']} → {result['new_interactions']}", style="yellow")
        
        # Update fox_personality with new profile
        self.fox_personality = FoxPersonality(self.user_profile)
    
    def pretrain_fox(self):
        """پیش‌آموزش Fox با دیتاست کامل"""
        if not self.fox_experience:
            self.console.print("سیستم تجربه در دسترس نیست.", style="red")
            return
        
        # بررسی اینکه قبلاً پیش‌آموزش شده یا نه
        if self.user_profile.profile.get('pretrained', False):
            self.console.print("⚠️ Fox قبلاً پیش‌آموزش شده است!", style="yellow")
            return
        
        # اضافه کردن تجربه پایه (معادل 3 ماه)
        base_experience = 2700  # 90 روز × 30 تعامل
        
        old_interactions = self.user_profile.profile['interaction_count']
        old_level = self.user_profile.profile['relationship_level']
        
        # بروزرسانی پروفایل
        self.user_profile.profile.update({
            'interaction_count': old_interactions + base_experience,
            'relationship_level': min(10, old_level + 5),
            'artificial_experience': self.user_profile.profile.get('artificial_experience', 0) + base_experience,
            'pretrained': True,
            'pretrain_date': datetime.now().isoformat()
        })
        
        # اضافه کردن ویژگی‌های پیش‌آموزش
        current_traits = self.user_profile.profile.get('personality_traits', [])
        pretrain_traits = ['آموزش‌دیده', 'دانشمند', 'پاسخگو']
        
        for trait in pretrain_traits:
            if trait not in current_traits:
                current_traits.append(trait)
        
        self.user_profile.profile['personality_traits'] = current_traits
        
        # اضافه کردن علایق پایه
        base_interests = ['گفتگو', 'یادگیری', 'کمک‌رسانی']
        current_interests = self.user_profile.profile.get('interests', [])
        
        for interest in base_interests:
            if interest not in current_interests:
                current_interests.append(interest)
        
        self.user_profile.profile['interests'] = current_interests
        
        self.user_profile.save_profile()
        
        # نمایش نتایج
        self.console.print("🎓 Fox با دیتاست کامل پیش‌آموزش شد!", style="bold green")
        self.console.print(f"• تجربه اضافه شده: {base_experience} (معادل 3 ماه)", style="green")
        self.console.print(f"• سطح رابطه: {old_level} → {self.user_profile.profile['relationship_level']}", style="cyan")
        self.console.print(f"• تعامل: {old_interactions} → {self.user_profile.profile['interaction_count']}", style="yellow")
        self.console.print(f"• ویژگی‌های جدید: {', '.join(pretrain_traits)}", style="magenta")
        self.console.print(f"• علایق پایه: {', '.join(base_interests)}", style="blue")
        
        # بروزرسانی شخصیت
        self.fox_personality = FoxPersonality(self.user_profile)
        self.fox_experience = FoxExperienceSystem(self.user_profile)
        
        self.console.print("\n🧠 Fox حالا با دانش کاملی آماده صحبت است!", style="bold blue")
    
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
            
            # Check for web search - expanded keywords
            web_keywords = [
                # Persian
                'جستجو کن', 'سرچ کن', 'اینترنت', 'آخرین اخبار', 'خبر', 'قیمت', 
                'آب و هوا', 'هوا', 'امروز', 'الان', 'فعلی', 'جدید', 'تازه',
                'چند', 'چقدر', 'کی', 'کجا', 'چطور', 'آخرین', 'جدیدترین',
                # English  
                'search', 'internet', 'news', 'price', 'weather', 'current',
                'latest', 'today', 'now', 'how much', 'what is', 'when',
                'where', 'how', 'recent'
            ]
            
            # Also check for question patterns that likely need internet
            question_patterns = [
                'قیمت', 'نرخ', 'چند تومان', 'چند درهم', 'چند دلار',
                'آب و هوا', 'دما', 'بارش', 'باران', 'برف',
                'اخبار', 'خبر', 'چه خبر', 'آخرین خبر',
                'کرونا', 'کووید', 'ویروس', 'بیماری',
                'انتخابات', 'سیاست', 'دولت', 'رئیس جمهور',
                'ورزش', 'فوتبال', 'جام جهانی', 'المپیک',
                'بورس', 'سهام', 'ارز', 'طلا', 'سکه', 'دلار', 'یورو'
            ]
            
            needs_web_search = (
                any(keyword in text.lower() for keyword in web_keywords) or
                any(pattern in text.lower() for pattern in question_patterns) or
                ('?' in text and len(text.split()) > 2)  # Questions longer than 2 words
            )
            
            if needs_web_search:
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
            
            response = self.llm.chat(context_messages, fox_learning=self.fox_learning)
            
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
                    response = self.llm.chat(context_messages, fox_learning=self.fox_learning)
                    
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
