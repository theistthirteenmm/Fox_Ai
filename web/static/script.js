class ChatApp {
    constructor() {
        this.ws = null;
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.voiceButton = document.getElementById('voiceButton');
        this.ttsToggle = document.getElementById('ttsToggle');
        this.messages = document.getElementById('messages');
        this.chatContainer = document.querySelector('.chat-container'); // Add chat container reference
        this.status = document.getElementById('status');
        this.typing = document.getElementById('typing');
        this.isRecording = false;
        this.recognition = null;
        this.ttsEnabled = true; // TTS enabled by default
        this.selectedVoiceIndex = -1; // For voice selection
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupVoiceRecognition();
        this.setupScrollObserver(); // Add scroll observer
        this.connect();
        this.setWelcomeTime();
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.voiceButton.addEventListener('click', () => this.toggleVoiceRecording());
        this.ttsToggle.addEventListener('click', () => this.toggleTTS());
        
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.messageInput.addEventListener('input', (e) => {
            this.adjustTextareaHeight();
            this.updateSendButton();
            this.handleCommandSuggestions(e.target.value);
        });
    }
    
    handleCommandSuggestions(value) {
        if (value === '/') {
            this.showCommandMenu();
        } else {
            this.hideCommandMenu();
        }
    }
    
    showCommandMenu() {
        let menu = document.getElementById('commandMenu');
        if (!menu) {
            menu = document.createElement('div');
            menu.id = 'commandMenu';
            menu.className = 'command-menu';
            menu.innerHTML = `
                <div class="command-item" data-cmd="/help">📚 /help - نمایش راهنما</div>
                <div class="command-item" data-cmd="/models">🤖 /models - لیست مدلها</div>
                <div class="command-item" data-cmd="/history">📜 /history - تاریخچه مکالمات</div>
                <div class="command-item" data-cmd="/search ">🔍 /search - جستجو در تاریخچه</div>
                <div class="command-item" data-cmd="/memory">🧠 /memory - نمایش حافظه</div>
                <div class="command-item" data-cmd="/recall ">🧠 /recall - یادآوری مکالمات</div>
                <div class="command-item" data-cmd="/teach ">🎓 /teach - آموزش پاسخ خاص</div>
                <div class="command-item" data-cmd="/learn ">📖 /learn - آموزش دانش جدید</div>
                <div class="command-item" data-cmd="/learned">📊 /learned - آمار یادگیری</div>
                <div class="command-item" data-cmd="/mood">😊 /mood - وضعیت احساسی</div>
                <div class="command-item" data-cmd="/status">📊 /status - وضعیت کامل</div>
                <div class="command-item" data-cmd="/experience">📈 /experience - تجربه Fox</div>
                <div class="command-item" data-cmd="/web ">🌐 /web - جستجو در اینترنت</div>
                <div class="command-item" data-cmd="/news ">📰 /news - دریافت اخبار</div>
                <div class="command-item" data-cmd="/weather ">🌤️ /weather - آب و هوا</div>
                <div class="command-item" data-cmd="/speak ">🔊 /speak - گفتن متن</div>
                <div class="command-item" data-cmd="/voices">🎵 /voices - صداهای موجود</div>
                <div class="command-item" data-cmd="/voice_test">🔊 /voice_test - تست صدا</div>
            `;
            
            menu.addEventListener('click', (e) => {
                if (e.target.classList.contains('command-item')) {
                    const cmd = e.target.getAttribute('data-cmd');
                    this.messageInput.value = cmd;
                    this.hideCommandMenu();
                    
                    // Auto-send simple commands, focus for complex ones
                    if (cmd === '/help' || cmd === '/learned' || cmd === '/mood' || cmd === '/models' || 
                        cmd === '/history' || cmd === '/memory' || cmd === '/status' || cmd === '/experience' ||
                        cmd === '/voices' || cmd === '/voice_test' || cmd === '/listen' || cmd === '/voice' ||
                        cmd === '/tts_on' || cmd === '/tts_off') {
                        this.sendMessage();
                    } else {
                        this.messageInput.focus();
                        if (cmd.endsWith(' ')) {
                            this.messageInput.setSelectionRange(cmd.length, cmd.length);
                        }
                    }
                }
            });
            
            document.body.appendChild(menu);
        }
        
        const rect = this.messageInput.getBoundingClientRect();
        menu.style.left = rect.left + 'px';
        menu.style.bottom = (window.innerHeight - rect.top + 10) + 'px';
        menu.style.display = 'block';
    }
    
    hideCommandMenu() {
        const menu = document.getElementById('commandMenu');
        if (menu) {
            menu.style.display = 'none';
        }
    }
    
    setupScrollObserver() {
        // Observer to auto-scroll when new content is added
        const observer = new MutationObserver(() => {
            this.scrollToBottom();
        });
        
        observer.observe(this.messages, {
            childList: true,
            subtree: true
        });
    }
    
    setupVoiceRecognition() {
        // Check if browser supports speech recognition
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.voiceButton.style.display = 'none';
            console.log('Speech recognition not supported in this browser');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        try {
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'fa-IR'; // Persian first
            
            this.recognition.onstart = () => {
                this.isRecording = true;
                this.voiceButton.classList.add('recording');
                this.voiceButton.title = 'در حال ضبط... کلیک کنید تا متوقف شود';
                this.voiceButton.innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <rect x="6" y="6" width="12" height="12" fill="currentColor"/>
                    </svg>
                `;
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.messageInput.value = transcript;
                this.adjustTextareaHeight();
                this.updateSendButton();
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                
                if (event.error === 'not-allowed') {
                    alert('لطفاً اجازه دسترسی به میکروفن را بدهید');
                } else if (event.error === 'no-speech') {
                    alert('صدایی شنیده نشد، دوباره تلاش کنید');
                } else {
                    // Try English if Persian failed
                    if (this.recognition.lang === 'fa-IR') {
                        this.recognition.lang = 'en-US';
                        setTimeout(() => this.recognition.start(), 100);
                        return;
                    }
                }
                
                this.stopRecording();
            };
            
            this.recognition.onend = () => {
                this.stopRecording();
            };
            
            // Show microphone button
            this.voiceButton.style.display = 'flex';
            
        } catch (error) {
            console.error('Failed to initialize speech recognition:', error);
            this.voiceButton.style.display = 'none';
            
            // Show browser info message
            const browserInfo = document.getElementById('browserInfo');
            if (browserInfo) {
                browserInfo.style.display = 'block';
                setTimeout(() => {
                    browserInfo.style.display = 'none';
                }, 10000); // Hide after 10 seconds
            }
        }
    }
    
    toggleVoiceRecording() {
        if (!this.recognition) {
            alert('تشخیص گفتار در این مرورگر پشتیبانی نمی‌شود');
            return;
        }
        
        if (this.isRecording) {
            this.recognition.stop();
        } else {
            // Request microphone permission first
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(() => {
                    this.recognition.start();
                })
                .catch((error) => {
                    console.error('Microphone permission denied:', error);
                    alert('لطفاً دسترسی میکروفن را در تنظیمات مرورگر فعال کنید و صفحه را رفرش کنید');
                });
        }
    }
    
    stopRecording() {
        this.isRecording = false;
        this.voiceButton.classList.remove('recording');
        this.voiceButton.title = 'ضبط صوتی';
        this.voiceButton.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" fill="currentColor"/>
                <path d="M19 10V12C19 16.42 15.42 20 11 20H9V22H15C19.42 22 23 18.42 23 14V10H19Z" fill="currentColor"/>
                <path d="M5 10V12C5 15.31 7.69 18 11 18V20C6.58 20 3 16.42 3 12V10H5Z" fill="currentColor"/>
            </svg>
        `;
    }
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            this.updateStatus(true);
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onclose = () => {
            this.updateStatus(false);
            setTimeout(() => this.connect(), 3000);
        };
        
        this.ws.onerror = () => {
            this.updateStatus(false);
        };
    }
    
    updateStatus(online) {
        const dot = this.status.querySelector('.status-dot');
        const text = this.status.querySelector('span:last-child');
        
        if (online) {
            dot.classList.add('online');
            text.textContent = 'آنلاین';
            this.sendButton.disabled = false;
        } else {
            dot.classList.remove('online');
            text.textContent = 'آفلاین - تلاش برای اتصال...';
            this.sendButton.disabled = true;
        }
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'typing':
                this.showTyping();
                break;
            case 'message':
                this.hideTyping();
                
                // Check for voice commands
                if (data.message.includes('/set_voice')) {
                    const match = data.message.match(/\/set_voice (\d+)/);
                    if (match) {
                        this.selectedVoiceIndex = parseInt(match[1]);
                        console.log('Voice index set to:', this.selectedVoiceIndex);
                    }
                }
                
                this.addMessage(data.message, 'assistant');
                // Add text-to-speech for Fox responses
                this.speakText(data.message);
                break;
            case 'error':
                this.hideTyping();
                this.addMessage(data.message, 'assistant error');
                break;
        }
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || !this.ws || this.ws.readyState !== WebSocket.OPEN) return;
        
        this.addMessage(message, 'user');
        this.ws.send(JSON.stringify({ message }));
        
        this.messageInput.value = '';
        this.adjustTextareaHeight();
        this.updateSendButton();
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.getCurrentTime();
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.messages.appendChild(messageDiv);
        
        // Force scroll to bottom after adding message
        this.scrollToBottom();
        
        // Also scroll when content might change size
        requestAnimationFrame(() => {
            this.scrollToBottom();
        });
    }
    
    showTyping() {
        this.typing.style.display = 'flex';
        // Scroll when typing indicator appears
        this.scrollToBottom();
        requestAnimationFrame(() => {
            this.scrollToBottom();
        });
    }
    
    hideTyping() {
        this.typing.style.display = 'none';
    }
    
    adjustTextareaHeight() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }
    
    updateSendButton() {
        const hasText = this.messageInput.value.trim().length > 0;
        const isConnected = this.ws && this.ws.readyState === WebSocket.OPEN;
        this.sendButton.disabled = !hasText || !isConnected;
    }
    
    scrollToBottom() {
        // Use chat container for scrolling (it has overflow-y: auto)
        const container = this.chatContainer;
        
        // Immediate scroll
        container.scrollTop = container.scrollHeight;
        
        // Smooth scroll as backup
        container.scrollTo({
            top: container.scrollHeight,
            behavior: 'smooth'
        });
        
        // Delayed scroll to ensure content is rendered
        setTimeout(() => {
            container.scrollTop = container.scrollHeight;
        }, 50);
        
        // Additional scroll for slow rendering
        setTimeout(() => {
            container.scrollTop = container.scrollHeight;
        }, 200);
    }
    
    getCurrentTime() {
        return new Date().toLocaleTimeString('fa-IR', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    speakText(text) {
        // Text-to-Speech for Fox responses
        if ('speechSynthesis' in window && this.ttsEnabled) {
            // Cancel any ongoing speech
            speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            
            // Wait for voices to load
            const setVoice = () => {
                const voices = speechSynthesis.getVoices();
                console.log('Available voices:', voices.map(v => `${v.name} (${v.lang})`));
                
                // Try to find Persian/Farsi voice with better matching
                const persianVoice = voices.find(voice => 
                    voice.lang.startsWith('fa') || 
                    voice.lang.includes('fa-') ||
                    voice.lang.includes('persian') ||
                    voice.name.toLowerCase().includes('persian') ||
                    voice.name.toLowerCase().includes('farsi') ||
                    voice.name.toLowerCase().includes('زهرا') ||
                    voice.name.toLowerCase().includes('مریم')
                );
                
                if (persianVoice) {
                    utterance.voice = persianVoice;
                    console.log('Using Persian voice:', persianVoice.name);
                } else if (this.selectedVoiceIndex >= 0 && voices[this.selectedVoiceIndex]) {
                    // Use user-selected voice
                    utterance.voice = voices[this.selectedVoiceIndex];
                    console.log('Using selected voice:', voices[this.selectedVoiceIndex].name);
                } else {
                    // Fallback: try Arabic or similar
                    const arabicVoice = voices.find(voice => 
                        voice.lang.startsWith('ar') ||
                        voice.name.toLowerCase().includes('arabic')
                    );
                    if (arabicVoice) {
                        utterance.voice = arabicVoice;
                        console.log('Using Arabic voice as fallback:', arabicVoice.name);
                    } else {
                        console.log('No Persian/Arabic voice found, using default');
                    }
                }
                
                utterance.rate = 0.8;  // Slower for Persian
                utterance.pitch = 1.0;
                utterance.volume = 0.9;
                utterance.lang = 'fa-IR';  // Set Persian language
                
                speechSynthesis.speak(utterance);
            };
            
            // Check if voices are already loaded
            if (speechSynthesis.getVoices().length > 0) {
                setVoice();
            } else {
                // Wait for voices to load
                speechSynthesis.onvoiceschanged = setVoice;
            }
        }
    }
    
    toggleTTS() {
        this.ttsEnabled = !this.ttsEnabled;
        
        if (this.ttsEnabled) {
            this.ttsToggle.textContent = '🔊';
            this.ttsToggle.title = 'خاموش کردن صدا';
            this.ttsToggle.classList.remove('disabled');
        } else {
            this.ttsToggle.textContent = '🔇';
            this.ttsToggle.title = 'روشن کردن صدا';
            this.ttsToggle.classList.add('disabled');
            // Cancel any ongoing speech
            if ('speechSynthesis' in window) {
                speechSynthesis.cancel();
            }
        }
    }
    
    setWelcomeTime() {
        const welcomeTime = document.getElementById('welcome-time');
        if (welcomeTime) {
            welcomeTime.textContent = this.getCurrentTime();
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
