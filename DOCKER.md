# 🐳 Fox AI - Docker Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum (for AI models)
- 10GB free disk space

### One-Command Setup
```bash
# Clone and start
git clone https://github.com/theistthirteenmm/Fox_Ai.git
cd Fox_Ai
./docker-fox.sh build
./docker-fox.sh start
```

## 📋 Available Commands

### Basic Operations
```bash
./docker-fox.sh build      # Build Fox AI image
./docker-fox.sh start      # Start services
./docker-fox.sh stop       # Stop services
./docker-fox.sh restart    # Restart services
./docker-fox.sh status     # Show status
./docker-fox.sh logs       # View logs
```

### Production Deployment
```bash
./docker-fox.sh start-prod # Start with Nginx reverse proxy
```

### Maintenance
```bash
./docker-fox.sh update     # Update from Git
./docker-fox.sh backup     # Create data backup
./docker-fox.sh restore <file> # Restore from backup
./docker-fox.sh clean      # Clean up everything
```

## 🌐 Access Points

### Development
- **Web Interface**: http://localhost:7070
- **Ollama API**: http://localhost:11434

### Production (with Nginx)
- **Web Interface**: http://localhost (port 80)
- **Direct Access**: http://localhost:7070

## 📊 What's Included

### Services
- **fox-ai**: Main application container
- **nginx**: Reverse proxy (production only)

### Features
- ✅ Complete Fox AI application
- ✅ Ollama AI model server
- ✅ Automatic model download
- ✅ Persistent data storage
- ✅ Health checks
- ✅ Auto-restart on failure
- ✅ Nginx reverse proxy
- ✅ Backup/restore functionality

## 🔧 Configuration

### Environment Variables
```bash
# In docker-compose.yml
WEB_PORT=7070
WEB_HOST=0.0.0.0
OLLAMA_HOST=http://localhost:11434
```

### Volumes
- `fox_data`: Application data (database, profiles, configs)
- `fox_models`: AI models (Ollama)

### Ports
- `7070`: Fox AI web interface
- `11434`: Ollama API
- `80`: Nginx (production)

## 🔄 Model Management

### Default Model
- **qwen2:7b** (4GB) - Downloaded automatically

### Change Model
```bash
# Connect to container
docker exec -it fox-ai bash

# Download different model
ollama pull llama3.2:3b  # Smaller, faster
ollama pull llama3.2:8b  # Larger, better quality

# Update config
# Edit backend/config/settings.py
```

## 📦 Data Persistence

### Backup
```bash
./docker-fox.sh backup
# Creates: fox-ai-backup-YYYYMMDD_HHMMSS.tar.gz
```

### Restore
```bash
./docker-fox.sh restore fox-ai-backup-20260101_120000.tar.gz
```

### Manual Backup
```bash
# Backup volumes
docker run --rm -v fox-ai_fox_data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz -C /data .
docker run --rm -v fox-ai_fox_models:/models -v $(pwd):/backup alpine tar czf /backup/models-backup.tar.gz -C /models .
```

## 🔍 Troubleshooting

### Check Status
```bash
./docker-fox.sh status
```

### View Logs
```bash
./docker-fox.sh logs
```

### Container Issues
```bash
# Restart services
./docker-fox.sh restart

# Rebuild if needed
./docker-fox.sh stop
./docker-fox.sh build
./docker-fox.sh start
```

### Model Download Issues
```bash
# Connect to container
docker exec -it fox-ai bash

# Check Ollama
ollama list
ollama pull qwen2:7b
```

### Port Conflicts
```bash
# Check what's using ports
sudo netstat -tlnp | grep :7070
sudo netstat -tlnp | grep :11434

# Change ports in docker-compose.yml
```

## 🔒 Security

### Production Setup
1. Use Nginx reverse proxy
2. Configure SSL certificates
3. Set up firewall rules
4. Use non-root user in container

### SSL Configuration
```bash
# Place certificates in ssl/ directory
mkdir ssl/
# Add cert.pem and key.pem
# Uncomment HTTPS section in nginx.conf
```

## 📈 Scaling

### Resource Limits
```yaml
# In docker-compose.yml
services:
  fox-ai:
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '4'
        reservations:
          memory: 4G
          cpus: '2'
```

### Multiple Instances
```bash
# Scale Fox AI instances
docker-compose up -d --scale fox-ai=3
```

## 🆘 Support

### Health Checks
- Automatic health monitoring
- Auto-restart on failure
- Status endpoint: http://localhost:7070/health

### Monitoring
```bash
# Resource usage
docker stats

# Container info
docker inspect fox-ai
```

---
**Fox AI is now fully containerized and production-ready! 🦊🐳**
