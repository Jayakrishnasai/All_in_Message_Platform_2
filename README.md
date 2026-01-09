# Dailyfix Messaging Infrastructure Challenge

A complete messaging platform with Matrix Synapse, social media bridging, and AI-powered conversation analysis.

## 🚀 Quick Start

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker and Docker Compose installed
- Ubuntu 22.04 (or compatible Linux distribution)
- At least 4GB RAM
- Ports 80, 8000, 8008, 8448 available

### Option 2: Local Development (No Docker)

**Prerequisites:**
- Python 3.10+ installed
- Node.js 18+ and npm installed
- See [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed instructions
- Quick start: [QUICK_LOCAL.md](QUICK_LOCAL.md)

### Docker Setup Steps

1. **Clone and Navigate**
   ```bash
   cd dailyfix-messaging
   ```

2. **Configure Domain (Optional)**
   - Set up DuckDNS domain (e.g., `yourname.duckdns.org`)
   - Update `SYNAPSE_SERVER_NAME` in `.env` file:
     ```bash
     echo "SYNAPSE_SERVER_NAME=yourname.duckdns.org" > .env
     ```
   - Or use `localhost` for local testing

3. **Initialize Matrix Synapse**
   ```bash
   docker-compose run --rm synapse generate
   ```
   This creates the initial configuration in `synapse/data/homeserver.yaml`

4. **Configure Synapse Server Name**
   Edit `synapse/data/homeserver.yaml`:
   ```yaml
   server_name: "yourname.duckdns.org"  # or "localhost"
   ```

5. **Start All Services**
   ```bash
   docker-compose up -d
   ```

6. **Create First User**
   ```bash
   docker-compose exec synapse register_new_matrix_user -c /data/homeserver.yaml -a -u admin -p admin123 http://localhost:8008
   ```

7. **Access Services**
   - Matrix Client: http://localhost:8008 (or your domain)
   - Element Web: https://app.element.io (connect to your server)
   - AI Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

8. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Frontend runs on http://localhost:3000

---

## 🖥️ Local Development (Without Docker)

**Quick Start:**
```bash
# Windows
start-local.bat

# Linux/Mac
chmod +x start-local.sh
./start-local.sh
```

**Manual Setup:**
1. **Backend**: See [LOCAL_SETUP.md](LOCAL_SETUP.md) for Python setup
2. **Frontend**: `cd frontend && npm install && npm run dev`
3. **Matrix**: Use public server (https://matrix.org) or install locally

**For detailed instructions, see:**
- [LOCAL_SETUP.md](LOCAL_SETUP.md) - Complete local setup guide
- [QUICK_LOCAL.md](QUICK_LOCAL.md) - Quick local testing guide

## 📋 Services Overview

### Matrix Synapse
- **Port**: 8008 (HTTP), 8448 (Federation)
- **Data**: `./synapse/data`
- **Access**: http://localhost:8008

### Mautrix Instagram Bridge
- **Status**: Configured and ready
- **Note**: Instagram OAuth requires app registration. For demo, bridge runs in mock mode.

### AI Backend (FastAPI)
- **Port**: 8000
- **Endpoints**:
  - `POST /summarize` - Summarize conversations
  - `POST /intent` - Parse user intent
  - `POST /priority` - Rank messages by importance
  - `POST /vector/store` - Store conversation embeddings
  - `POST /vector/search` - Semantic search
  - `POST /daily-report` - Generate daily reports

### NGINX Reverse Proxy
- **Port**: 80
- **Routes**: 
  - `/` → Synapse
  - `/api` → AI Backend

## 🧪 Testing

### Test Matrix Synapse
```bash
curl http://localhost:8008/_matrix/client/versions
```

### Test AI Backend
```bash
# Summarize
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Long conversation text here..."}'

# Intent Parsing
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "I need help with my order"}'

# Daily Report
curl -X POST http://localhost:8000/daily-report \
  -H "Content-Type: application/json" \
  -d '{"user_id": "admin", "date": "2024-01-15"}'
```

## 📁 Project Structure

```
dailyfix-messaging/
├── docker-compose.yml       # Main orchestration
├── README.md                # This file
├── docs/                    # Documentation
│   ├── architecture.md
│   └── timeline.md
├── synapse/                 # Matrix Synapse data
│   └── data/
├── mautrix/                 # Mautrix bridge config
│   ├── config.yaml
│   └── data/
├── nginx/                   # NGINX config
│   └── default.conf
├── backend/                 # AI Backend (FastAPI)
│   ├── main.py
│   ├── ai/
│   ├── requirements.txt
│   └── Dockerfile
└── frontend/                # Next.js frontend
    ├── pages/
    └── services/
```

## 🔧 Configuration

### Environment Variables
Create `.env` file:
```
SYNAPSE_SERVER_NAME=yourname.duckdns.org
```

### Matrix Registration
After first start, register users via:
```bash
docker-compose exec synapse register_new_matrix_user \
  -c /data/homeserver.yaml \
  -u username \
  -p password \
  http://localhost:8008
```

## 🎯 Demo Checklist

1. ✅ Matrix Synapse running
2. ✅ User created and logged in
3. ✅ Frontend displays rooms
4. ✅ AI summarization working
5. ✅ Intent parsing functional
6. ✅ Daily reports generated
7. ✅ Vector search operational

## 🐛 Troubleshooting

### Synapse won't start
- Check `synapse/data/homeserver.yaml` exists
- Verify `server_name` is set correctly
- Check logs: `docker-compose logs synapse`

### Bridge not connecting
- Verify Mautrix config in `mautrix/config.yaml`
- Check bridge logs: `docker-compose logs mautrix-instagram`

### AI Backend errors
- Ensure models download on first run (may take time)
- Check Python dependencies: `docker-compose exec ai-backend pip list`

## 📚 Additional Resources

- [Matrix Documentation](https://matrix.org/docs/)
- [Mautrix Bridges](https://github.com/mautrix)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)

## 📝 Notes

- For production, enable HTTPS
- Instagram OAuth requires app registration with Meta
- Vector store persists in `backend/vector_store/`
- All data persists in Docker volumes

## 🎬 Demo Video Preparation

1. Show Matrix Synapse setup
2. Demonstrate user registration
3. Show frontend chat interface
4. Test AI features (summarization, intent, reports)
5. Show vector search capabilities
6. Display daily report generation

---

**Built for Dailyfix Challenge** | Production-ready MVP
