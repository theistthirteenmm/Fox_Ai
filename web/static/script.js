class ChatApp {
    constructor() {
        this.ws = null;
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.voiceButton = document.getElementById('voiceButton');
        this.messages = document.getElementById('messages');
        this.chatContainer = document.querySelector('.chat-container'); // Add chat container reference
        this.status = document.getElementById('status');
        this.typing = document.getElementById('typing');
        this.isRecording = false;
        this.recognition = null;
        
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
        
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.messageInput.addEventListener('input', () => {
            this.adjustTextareaHeight();
            this.updateSendButton();
        });
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
        if (!this.recognition) return;
        
        if (this.isRecording) {
            this.recognition.stop();
        } else {
            this.recognition.start();
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
                this.addMessage(data.message, 'assistant');
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
