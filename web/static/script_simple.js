class ChatApp {
    constructor() {
        this.ws = null;
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.messages = document.getElementById('messages');
        this.status = document.getElementById('status');
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.connect();
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.messageInput.addEventListener('input', (e) => {
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
                <div class="command-item" data-cmd="/history">📜 /history - تاریخچه</div>
                <div class="command-item" data-cmd="/mood">😊 /mood - وضعیت احساسی</div>
                <div class="command-item" data-cmd="/status">📊 /status - وضعیت Fox</div>
                <div class="command-item" data-cmd="/web ">🌐 /web - جستجو اینترنت</div>
            `;
            
            menu.addEventListener('click', (e) => {
                if (e.target.classList.contains('command-item')) {
                    const cmd = e.target.getAttribute('data-cmd');
                    this.messageInput.value = cmd;
                    this.hideCommandMenu();
                    
                    if (cmd === '/help' || cmd === '/history' || cmd === '/mood' || cmd === '/status') {
                        this.sendMessage();
                    } else {
                        this.messageInput.focus();
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
    
    connect() {
        this.ws = new WebSocket(`ws://${window.location.host}/ws`);
        
        this.ws.onopen = () => {
            this.updateStatus(true);
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'message') {
                this.addMessage(data.message, 'assistant');
            }
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
            text.textContent = 'در حال اتصال...';
            this.sendButton.disabled = true;
        }
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || !this.ws || this.ws.readyState !== WebSocket.OPEN) return;
        
        this.addMessage(message, 'user');
        this.ws.send(JSON.stringify({ message }));
        
        this.messageInput.value = '';
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;
        
        messageDiv.appendChild(contentDiv);
        this.messages.appendChild(messageDiv);
        
        this.messages.scrollTop = this.messages.scrollHeight;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
