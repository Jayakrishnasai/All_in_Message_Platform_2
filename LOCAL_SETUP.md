# Local Development Setup (Without Docker)

This guide will help you run the Dailyfix Messaging application on your local machine without Docker.

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ and npm installed
- PostgreSQL (optional, SQLite works for development)
- Git

## Step 1: Clone and Setup Project

```bash
cd dailyfix-messaging
```

## Step 2: Backend Setup (Python/FastAPI)

### 2.1 Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt

# Install spaCy English model
python -m spacy download en_core_web_sm
```

### 2.3 Create Data Directories

```bash
mkdir -p vector_store
```

### 2.4 Run Backend

```bash
# From backend directory
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be available at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

## Step 3: Frontend Setup (Next.js)

### 3.1 Install Dependencies

```bash
cd frontend
npm install
```

### 3.2 Configure Environment

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_MATRIX_SERVER=http://localhost:8008
NEXT_PUBLIC_AI_BACKEND=http://localhost:8000
```

### 3.3 Run Frontend

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Step 4: Matrix Synapse Setup (Local)

### Option A: Use Existing Matrix Server (Recommended for Testing)

If you have access to an existing Matrix server, update the frontend config to point to it.

### Option B: Install Matrix Synapse Locally

#### 4.1 Install Synapse

```bash
# On Ubuntu/Debian
sudo apt-get install -y build-essential python3-dev libffi-dev \
    python3-pip python3-setuptools sqlite3 libssl-dev \
    python3-venv libjpeg-dev libxslt1-dev

# Create synapse directory
mkdir -p ~/synapse
cd ~/synapse

# Create virtual environment
python3 -m venv env
source env/bin/activate

# Install Synapse
pip install --upgrade pip
pip install matrix-synapse

# Install PostgreSQL driver (optional, for production)
# pip install psycopg2
```

#### 4.2 Generate Configuration

```bash
python -m synapse.app.homeserver \
    --server-name localhost \
    --config-path homeserver.yaml \
    --generate-config \
    --report-stats=no
```

#### 4.3 Edit Configuration

Edit `homeserver.yaml`:
```yaml
server_name: "localhost"
public_baseurl: "http://localhost:8008"

# Database (SQLite for development)
database:
  name: sqlite3
  args:
    database: /path/to/synapse/homeserver.db

# Registration (allow registration for dev)
enable_registration: true
enable_registration_without_verification: true

# Listen on all interfaces
listeners:
  - port: 8008
    type: http
    tls: false
    bind_addresses: ['::1', '127.0.0.1']
    x_forwarded: true
    resources:
      - names: [client, federation]
        compress: false
```

#### 4.4 Create First User

```bash
# Register admin user
register_new_matrix_user -c homeserver.yaml -a -u admin -p admin123 http://localhost:8008
```

#### 4.5 Run Synapse

```bash
synctl start
# Or
python -m synapse.app.homeserver --config-path homeserver.yaml
```

Synapse will be available at: `http://localhost:8008`

## Step 5: Update Frontend Matrix Client

Edit `frontend/services/matrix.js` to ensure it points to your local Synapse:

```javascript
const MATRIX_SERVER = process.env.NEXT_PUBLIC_MATRIX_SERVER || 'http://localhost:8008';
```

## Step 6: Testing

### Test Backend
```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

### Test Matrix
```bash
curl http://localhost:8008/_matrix/client/versions
```

### Test Frontend
Open browser: `http://localhost:3000`

## Troubleshooting

### Backend Issues

**Import errors:**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Model download issues:**
- Models download automatically on first use
- May take several minutes
- Check internet connection

**Port already in use:**
```bash
# Change port in uvicorn command
uvicorn main:app --port 8001
```

### Frontend Issues

**Cannot connect to Matrix:**
- Verify Synapse is running: `curl http://localhost:8008/_matrix/client/versions`
- Check CORS settings in Synapse config
- Verify `.env.local` has correct Matrix server URL

**Cannot connect to Backend:**
- Verify backend is running: `curl http://localhost:8000/health`
- Check `NEXT_PUBLIC_AI_BACKEND` in `.env.local`

### Matrix Synapse Issues

**Port conflicts:**
- Change port in `homeserver.yaml`
- Update frontend config accordingly

**Database errors:**
- Check database path in config
- Ensure write permissions

**Registration fails:**
- Enable registration in config
- Check logs: `tail -f ~/synapse/homeserver.log`

## Development Workflow

### Start All Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Matrix (if running locally):**
```bash
cd ~/synapse
source env/bin/activate
synctl start
```

### Hot Reload

- Backend: `--reload` flag enables auto-reload on code changes
- Frontend: Next.js has built-in hot reload

## Environment Variables

### Backend
No environment variables needed for basic setup.

### Frontend
Create `frontend/.env.local`:
```env
NEXT_PUBLIC_MATRIX_SERVER=http://localhost:8008
NEXT_PUBLIC_AI_BACKEND=http://localhost:8000
```

### Matrix Synapse
Configured in `homeserver.yaml`

## Alternative: Use Public Matrix Server

If setting up Synapse is too complex, you can use a public Matrix server for testing:

1. Create account on https://app.element.io
2. Update frontend config:
   ```env
   NEXT_PUBLIC_MATRIX_SERVER=https://matrix.org
   ```
3. Use your public Matrix credentials

**Note:** This limits some features but works for frontend/backend testing.

## Quick Start Script

Create `start-local.sh`:

```bash
#!/bin/bash

# Start Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload &
BACKEND_PID=$!

# Start Frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "Backend running on http://localhost:8000"
echo "Frontend running on http://localhost:3000"
echo "Press Ctrl+C to stop all services"

wait
```

## Windows Quick Start

Create `start-local.bat`:

```batch
@echo off

REM Start Backend
cd backend
call venv\Scripts\activate
start "Backend" cmd /k "uvicorn main:app --reload"

REM Start Frontend
cd ..\frontend
start "Frontend" cmd /k "npm run dev"

echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
pause
```

## Summary

1. **Backend**: Python virtual env → install deps → run uvicorn
2. **Frontend**: npm install → npm run dev
3. **Matrix**: Install Synapse OR use public server
4. **Access**: Frontend at `http://localhost:3000`

All services run independently and can be started/stopped separately.

---

**Note**: For production, use Docker. This local setup is for development only.
