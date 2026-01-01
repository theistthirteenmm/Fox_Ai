# Fox AI - Complete Docker Setup
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install Node.js dependencies for Electron
RUN cd electron && npm install && cd ..

# Create data directory
RUN mkdir -p data/database data/logs data/models data/profiles

# Set environment variables
ENV WEB_PORT=7070
ENV WEB_HOST=0.0.0.0
ENV OLLAMA_HOST=http://localhost:11434

# Expose ports
EXPOSE 7070 11434

# Create startup script
RUN echo '#!/bin/bash\n\
# Start Ollama in background\n\
ollama serve &\n\
sleep 5\n\
\n\
# Download default model if not exists\n\
if ! ollama list | grep -q "qwen2:7b"; then\n\
    echo "📥 Downloading AI model..."\n\
    ollama pull qwen2:7b\n\
fi\n\
\n\
# Start Fox AI\n\
echo "🦊 Starting Fox AI..."\n\
python start_web.py' > /app/start.sh && chmod +x /app/start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7070/health || exit 1

# Start command
CMD ["/app/start.sh"]
