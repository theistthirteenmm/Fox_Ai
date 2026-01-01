class ChatApp {
    constructor() {
        this.ws = null;
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.voiceButton = document.getElementById('voiceButton');
        this.messages = document.getElementById('messages');
        this.status = document.getElementById('status');
        this.typing = document.getElementById('typing');
        this.isRecording = false;
        this.recognition = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupVoiceRecognition();
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
    
    setupVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'fa-IR'; // Persian
            
            this.recognition.onstart = () => {
                this.isRecording = true;
                this.voiceButton.classList.add('recording');
                this.voiceButton.title = 'در حال ضبط... کلیک کنید تا متوقف شود';
            };
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.messageInput.value = transcript;
                this.adjustTextareaHeight();
                this.updateSendButton();
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.stopRecording();
            };
            
            this.recognition.onend = () => {
                this.stopRecording();
            };
        } else {
            this.voiceButton.style.display = 'none';
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
        this.scrollToBottom();
    }
    
    showTyping() {
        this.typing.style.display = 'flex';
        this.scrollToBottom();
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
        setTimeout(() => {
            this.messages.scrollTop = this.messages.scrollHeight;
        }, 100);
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
