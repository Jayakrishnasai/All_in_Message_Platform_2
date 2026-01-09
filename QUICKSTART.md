# Quick Start Guide

## Prerequisites

- Docker and Docker Compose installed
- Node.js 18+ (for frontend)
- 4GB+ RAM available
- Ports 80, 8000, 8008 available

## 5-Minute Setup

### 1. Clone and Navigate
```bash
cd dailyfix-messaging
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
# Create .env
echo "SYNAPSE_SERVER_NAME=localhost" > .env

# Initialize Synapse
docker-compose run --rm synapse generate

# Start services
docker-compose up -d

# Create admin user
docker-compose exec synapse register_new_matrix_user \
  -c /data/homeserver.yaml -a -u admin -p admin123 http://localhost:8008
```

### 3. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:3000
- Matrix API: http://localhost:8008
- AI Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 5. Login
- Username: `admin`
- Password: `admin123`

## Testing

### Test Matrix Synapse
```bash
curl http://localhost:8008/_matrix/client/versions
```

### Test AI Backend
```bash
chmod +x test-api.sh
./test-api.sh
```

Or manually:
```bash
# Health check
curl http://localhost:8000/health

# Summarize
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Long conversation text here..."}'
```

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart
```

### Can't login
- Verify user was created: `docker-compose logs synapse | grep register`
- Try creating user again (may already exist)

### Frontend can't connect
- Verify Matrix server is running: `curl http://localhost:8008/health`
- Check browser console for errors
- Verify CORS settings in backend

### AI features not working
- Check backend logs: `docker-compose logs ai-backend`
- Models download on first request (may take time)
- Verify backend is accessible: `curl http://localhost:8000/health`

## Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Review [docs/architecture.md](docs/architecture.md) for system design
3. Check [docs/timeline.md](docs/timeline.md) for development timeline

## Demo Checklist

- [ ] All services running (`docker-compose ps`)
- [ ] Can login to frontend
- [ ] Can view rooms
- [ ] Can send/receive messages
- [ ] AI summarization works
- [ ] Intent parsing works
- [ ] Daily reports generate
- [ ] Vector search functional

---

**Need help?** Check the main [README.md](README.md) for detailed instructions.
