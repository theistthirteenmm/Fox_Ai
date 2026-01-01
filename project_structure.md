# Personal AI Assistant - Project Structure

## Directory Layout
```
personal-ai/
├── backend/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm_engine.py       # Ollama integration
│   │   ├── conversation.py     # Chat logic
│   │   ├── memory.py          # Long-term memory
│   │   ├── internet.py        # Web search/access
│   │   └── ai_connector.py    # External AI APIs
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat_api.py        # REST endpoints
│   │   └── websocket.py       # Real-time chat
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py          # SQLAlchemy models
│   │   └── migrations/        # DB versions
│   └── config/
│       ├── __init__.py
│       └── settings.py        # Configuration
├── cli/
│   ├── __init__.py
│   ├── main.py               # Command line interface
│   └── commands/             # CLI commands
├── web/
│   ├── static/               # HTML/CSS/JS
│   ├── templates/            # Jinja2 templates
│   └── app.py               # Web interface
├── data/                     # Persistent data
│   ├── models/               # Downloaded LLM models
│   ├── database/             # Database files
│   └── logs/                 # Application logs
├── requirements.txt
├── .env                      # Environment variables
└── README.md
```

## Development Phases
1. Core LLM Engine (Ollama)
2. Basic CLI Interface
3. Memory System
4. Web Interface
5. Internet Access
6. External AI Connectors
7. Voice Integration (Future)
