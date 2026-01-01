"""
Voice Support Module - Speech to Text and Text to Speech
"""
import io
import wave
import json
from typing import Optional
import requests

# Optional imports for voice features
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

class VoiceManager:
    def __init__(self):
        self.recognizer = None
        self.tts_engine = None
        self.microphone = None
        
        # Initialize Speech Recognition
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                
                # Adjust for ambient noise
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)
            except Exception as e:
                print(f"Warning: Could not initialize microphone: {e}")
                self.recognizer = None
                self.microphone = None
        
        # Initialize TTS
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                
                # Configure TTS settings for Persian
                voices = self.tts_engine.getProperty('voices')
                persian_voice_found = False
                
                # Try to find Persian/Arabic voice
                for voice in voices:
                    voice_name = voice.name.lower()
                    if any(keyword in voice_name for keyword in ['persian', 'farsi', 'arabic', 'urdu', 'zira', 'hazel']):
                        self.tts_engine.setProperty('voice', voice.id)
                        persian_voice_found = True
                        print(f"✅ Persian voice found: {voice.name}")
                        break
                
                if not persian_voice_found:
                    print("⚠️ No Persian voice found, using default")
                
                # Set speech rate and volume for better Persian pronunciation
                self.tts_engine.setProperty('rate', 120)  # Slower for Persian
                self.tts_engine.setProperty('volume', 0.9)  # Higher volume
                
            except Exception as e:
                print(f"Warning: Could not initialize TTS: {e}")
                self.tts_engine = None
    
    def is_available(self) -> dict:
        """Check which voice features are available"""
        return {
            'speech_to_text': SPEECH_RECOGNITION_AVAILABLE and self.recognizer is not None,
            'text_to_speech': TTS_AVAILABLE and self.tts_engine is not None,
            'microphone': self.microphone is not None
        }
    
    def listen_once(self, timeout: int = 5) -> Optional[str]:
        """Listen for speech and convert to text"""
        if not self.recognizer or not self.microphone:
            return None
        
        try:
            print("🎤 در حال گوش دادن...")
            
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("🔄 در حال تشخیص گفتار...")
            
            # Try different recognition services
            try:
                # Google Speech Recognition (free)
                text = self.recognizer.recognize_google(audio, language='fa-IR')
                return text
            except sr.UnknownValueError:
                try:
                    # Fallback to English
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    return text
                except:
                    return None
            except sr.RequestError:
                # Try offline recognition if available
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    return text
                except:
                    return None
                    
        except sr.WaitTimeoutError:
            print("⏰ زمان انتظار تمام شد")
            return None
        except Exception as e:
            print(f"❌ خطا در تشخیص گفتار: {str(e)}")
            return None
    
    def speak(self, text: str) -> bool:
        """Convert text to speech"""
        # Try eSpeak directly for Persian
        try:
            import subprocess
            # Use eSpeak with Persian voice
            subprocess.run(['espeak', '-v', 'fa', '-s', '150', text], 
                         check=True, capture_output=True)
            print(f"🔊 گفته شد: {text[:50]}...")
            return True
        except:
            pass
        
        # Fallback to pyttsx3
        if not self.tts_engine:
            return False
        
        try:
            print(f"🔊 در حال گفتن: {text[:50]}...")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"❌ خطا در تولید گفتار: {str(e)}")
            return False
    
    def start_voice_conversation(self, chat_callback):
        """Start interactive voice conversation"""
        if not self.is_available()['speech_to_text']:
            print("❌ تشخیص گفتار در دسترس نیست")
            return
        
        print("🎤 مکالمه صوتی شروع شد")
        print("💡 برای خروج 'خروج' یا 'quit' بگویید")
        
        while True:
            try:
                # Listen for user input
                user_speech = self.listen_once(timeout=10)
                
                if not user_speech:
                    print("🔇 صدایی شنیده نشد، دوباره تلاش کنید...")
                    continue
                
                print(f"👤 شما گفتید: {user_speech}")
                
                # Check for exit commands
                if any(word in user_speech.lower() for word in ['خروج', 'quit', 'exit', 'stop']):
                    print("👋 مکالمه صوتی پایان یافت")
                    break
                
                # Get AI response
                response = chat_callback(user_speech)
                
                if response:
                    print(f"🦊 Fox: {response}")
                    
                    # Speak the response
                    if self.is_available()['text_to_speech']:
                        self.speak(response)
                    
            except KeyboardInterrupt:
                print("\n👋 مکالمه صوتی متوقف شد")
                break
            except Exception as e:
                print(f"❌ خطا: {str(e)}")
    
    def process_audio_file(self, audio_file_path: str) -> Optional[str]:
        """Process uploaded audio file"""
        if not self.recognizer:
            return None
        
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            # Try to recognize
            text = self.recognizer.recognize_google(audio, language='fa-IR')
            return text
        except Exception as e:
            print(f"❌ خطا در پردازش فایل صوتی: {str(e)}")
            return None
