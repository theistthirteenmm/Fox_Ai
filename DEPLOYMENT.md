# Fox AI - Production Deployment Guide

## 🚀 Quick Deployment

### One-line install:
```bash
curl -sSL https://raw.githubusercontent.com/theistthirteenmm/Fox_Ai/main/deploy.sh | bash
```

### Manual deployment:
```bash
# 1. Clone repository
git clone https://github.com/theistthirteenmm/Fox_Ai.git
cd Fox_Ai

# 2. Run deployment script
chmod +x deploy.sh
./deploy.sh
```

## 🔧 Server Requirements

- **OS**: Ubuntu 20.04+ / Debian 11+
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 5GB free space
- **Network**: Internet access for dependencies

## 🌐 Access Methods

After deployment:
- **Web Interface**: http://your-server-ip
- **Direct Port**: http://your-server-ip:7070
- **With Domain**: Configure DNS to point to your server

## ⚙️ Service Management

```bash
# Check status
sudo systemctl status fox-ai

# Start/Stop/Restart
sudo systemctl start fox-ai
sudo systemctl stop fox-ai
sudo systemctl restart fox-ai

# View logs
sudo journalctl -u fox-ai -f

# Update Fox AI
cd Fox_Ai
git pull origin main
sudo systemctl restart fox-ai
```

## 🔒 Security Setup

### SSL Certificate (Let's Encrypt):
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Firewall:
```bash
sudo ufw status
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 📊 Monitoring

### Check Fox AI status:
```bash
curl http://localhost:7070/health
```

### Monitor resources:
```bash
htop
df -h
free -h
```

## 🔄 Backup & Restore

### Backup data:
```bash
tar -czf fox-ai-backup-$(date +%Y%m%d).tar.gz Fox_Ai/data/
```

### Restore data:
```bash
tar -xzf fox-ai-backup-YYYYMMDD.tar.gz
```

## 🐛 Troubleshooting

### Service not starting:
```bash
sudo journalctl -u fox-ai --no-pager
```

### Port conflicts:
```bash
sudo netstat -tlnp | grep :7070
```

### Permission issues:
```bash
sudo chown -R $USER:$USER Fox_Ai/
```

## 📞 Support

- GitHub Issues: https://github.com/theistthirteenmm/Fox_Ai/issues
- Documentation: Check README.md
