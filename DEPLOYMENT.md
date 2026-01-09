# Deployment Guide

## Cloud Deployment (Azure VM)

### Prerequisites
- Azure account with VM access
- Ubuntu 22.04 VM (Standard_B2s or larger recommended)
- SSH access to VM
- Domain name (DuckDNS or custom)

### Step 1: VM Setup

```bash
# SSH into VM
ssh username@your-vm-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for group changes
```

### Step 2: Domain Configuration

#### Option A: DuckDNS (Free)
```bash
# Install DuckDNS updater
sudo apt install curl -y

# Create update script
cat > ~/duckdns-update.sh << EOF
#!/bin/bash
echo url="https://www.duckdns.org/update?domains=yourname&token=YOUR_TOKEN&ip=" | curl -k -o ~/duckdns.log -K -
EOF

chmod +x ~/duckdns-update.sh

# Add to crontab (runs every 5 minutes)
(crontab -l 2>/dev/null; echo "*/5 * * * * ~/duckdns-update.sh") | crontab -
```

#### Option B: Custom Domain
- Point DNS A record to VM IP
- Update `.env` with your domain

### Step 3: Deploy Application

```bash
# Clone repository
git clone <your-repo-url>
cd dailyfix-messaging

# Configure environment
echo "SYNAPSE_SERVER_NAME=yourname.duckdns.org" > .env

# Run setup
chmod +x setup.sh
./setup.sh
```

### Step 4: Firewall Configuration

```bash
# Azure Portal: Add inbound rules for:
# - Port 80 (HTTP)
# - Port 8008 (Matrix)
# - Port 22 (SSH)

# Or via Azure CLI:
az vm open-port --port 80 --resource-group <rg> --name <vm-name>
az vm open-port --port 8008 --resource-group <rg> --name <vm-name>
```

### Step 5: NGINX Configuration Update

Edit `nginx/default.conf` to use your domain:
```nginx
server_name yourname.duckdns.org;
```

### Step 6: Start Services

```bash
docker-compose up -d
docker-compose logs -f  # Monitor startup
```

### Step 7: Verify Deployment

```bash
# Check services
docker-compose ps

# Test endpoints
curl http://yourname.duckdns.org/_matrix/client/versions
curl http://yourname.duckdns.org/api/health
```

## Local Development

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Node.js 18+

### Setup

```bash
# Clone and setup
cd dailyfix-messaging
./setup.sh

# Start frontend
cd frontend
npm install
npm run dev
```

## Production Considerations

### Security
- [ ] Enable HTTPS/TLS (Let's Encrypt)
- [ ] Set up firewall rules
- [ ] Use strong passwords
- [ ] Enable rate limiting
- [ ] Regular security updates

### Monitoring
- [ ] Set up log aggregation
- [ ] Monitor resource usage
- [ ] Set up alerts
- [ ] Backup data regularly

### Scaling
- [ ] Use PostgreSQL instead of SQLite
- [ ] Deploy to Kubernetes
- [ ] Use managed vector DB (Pinecone)
- [ ] Add load balancer
- [ ] Implement caching (Redis)

### Backup

```bash
# Backup Synapse data
docker-compose exec synapse tar -czf /data/backup-$(date +%Y%m%d).tar.gz /data

# Backup vector store
docker-compose exec ai-backend tar -czf /app/vector_store/backup.tar.gz /app/vector_store
```

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs synapse
docker-compose logs ai-backend

# Check resources
docker stats

# Restart services
docker-compose restart
```

### Domain not resolving
- Verify DNS settings
- Check firewall rules
- Test with `curl` from external machine

### High memory usage
- Reduce model sizes
- Use CPU-only models
- Increase VM size
- Implement model caching

## Maintenance

### Update Services
```bash
# Pull latest images
docker-compose pull

# Restart with new images
docker-compose up -d
```

### Clean Up
```bash
# Remove unused images
docker image prune -a

# Remove old logs
docker-compose logs --tail=0 -f  # Clear logs
```

---

**Note**: This is an MVP deployment. For production, implement proper security, monitoring, and scaling strategies.
