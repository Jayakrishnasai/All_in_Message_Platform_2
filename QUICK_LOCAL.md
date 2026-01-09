# Quick Local Setup (No Docker)

## Fastest Way to Test Locally

### Option 1: Backend + Frontend Only (No Matrix)

Test the AI features without Matrix:

**1. Backend:**
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload
```

**2. Frontend (in new terminal):**
```bash
cd frontend
npm install

# Create .env.local
echo "NEXT_PUBLIC_AI_BACKEND=http://localhost:8000" > .env.local

npm run dev
```

**3. Test AI Backend:**
- Open: http://localhost:8000/docs
- Test endpoints directly

**Note:** Frontend Matrix features won't work without a Matrix server, but you can test AI features via the API docs.

---

### Option 2: Full Setup with Public Matrix Server

**1. Backend (same as above)**

**2. Frontend:**
```bash
cd frontend
npm install

# Use public Matrix server
cat > .env.local << EOF
NEXT_PUBLIC_MATRIX_SERVER=https://matrix.org
NEXT_PUBLIC_AI_BACKEND=http://localhost:8000
EOF

npm run dev
```

**3. Create Matrix Account:**
- Go to https://app.element.io
- Create account
- Use those credentials in frontend

---

### Option 3: Use Startup Scripts

**Windows:**
```bash
start-local.bat
```

**Linux/Mac:**
```bash
chmod +x start-local.sh
./start-local.sh
```

---

## Testing Without Matrix

You can test all AI features via API:

```bash
# Health check
curl http://localhost:8000/health

# Summarize
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Long conversation text here..."}'

# Intent
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "I need help"}'
```

Open http://localhost:8000/docs for interactive API testing.

---

## Troubleshooting

**Python not found:**
- Install Python 3.10+ from python.org
- Make sure it's in PATH

**npm not found:**
- Install Node.js from nodejs.org

**Port already in use:**
- Change ports in commands
- Kill existing processes

**Import errors:**
- Make sure virtual environment is activated
- Reinstall: `pip install -r requirements.txt`

---

**For full Matrix setup, see LOCAL_SETUP.md**
