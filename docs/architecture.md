# Architecture Documentation

## System Overview

The Dailyfix Messaging Infrastructure is a complete messaging platform that integrates Matrix Synapse with social media bridges and AI-powered conversation analysis.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Element Web  │  │  Next.js App │  │  Mobile Apps │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────┼──────────────────────────────────┐
│                    NGINX Reverse Proxy                         │
│                    (Port 80)                                   │
└────────────────────────────┼──────────────────────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
┌─────────▼──────────┐ ┌─────▼──────┐ ┌────────▼──────────┐
│  Matrix Synapse    │ │ AI Backend │ │  Mautrix Bridge   │
│  (Port 8008)       │ │ (Port 8000)│ │  (Instagram)      │
└─────────┬──────────┘ └────────────┘ └────────┬──────────┘
          │                                     │
          └─────────────────┬───────────────────┘
                            │
                ┌───────────▼───────────┐
                │   Matrix Protocol     │
                │   (Federation)        │
                └───────────────────────┘
```

## Component Details

### 1. Matrix Synapse (Homeserver)

**Purpose**: Core messaging server implementing the Matrix protocol.

**Technology**: 
- Docker container: `matrixdotorg/synapse:latest`
- Protocol: Matrix Client-Server API
- Storage: SQLite (default) or PostgreSQL

**Key Features**:
- User authentication and authorization
- Room management
- Message persistence
- Federation support
- RESTful API

**Configuration**:
- Server name: Configurable via `SYNAPSE_SERVER_NAME`
- Data persistence: `./synapse/data` volume
- Ports: 8008 (HTTP), 8448 (Federation)

**Why Matrix?**
- Open, decentralized protocol
- End-to-end encryption support
- Rich ecosystem of bridges
- Self-hostable
- Standard REST API

### 2. Mautrix Instagram Bridge

**Purpose**: Bridge Instagram DMs into Matrix rooms.

**Technology**:
- Docker container: `dock.mau.dev/tulir/mautrix-instagram`
- Protocol: Matrix Application Service API

**How It Works**:
1. Bridge registers as an application service with Synapse
2. Creates virtual Matrix users for Instagram contacts
3. Syncs messages bidirectionally
4. Maps Instagram conversations to Matrix rooms

**Configuration**:
- Registration file: Generated automatically
- Config: `mautrix/config.yaml`
- OAuth: Requires Instagram app registration (mocked for demo)

**Limitations**:
- Instagram OAuth requires Meta Developer account
- Rate limiting applies
- Some features may be restricted by Instagram API

### 3. AI Backend (FastAPI)

**Purpose**: Provide AI-powered conversation analysis.

**Technology Stack**:
- Framework: FastAPI
- ML Models: Hugging Face Transformers
- NLP: spaCy
- Vector DB: FAISS (local)

**Endpoints**:

#### POST /summarize
- **Model**: `facebook/bart-large-cnn`
- **Input**: Raw conversation text
- **Output**: Condensed summary
- **Use Case**: Long conversation summarization

#### POST /intent
- **Model**: `distilbert-base-uncased` (fine-tuned)
- **Input**: Single message
- **Output**: Intent classification
- **Intents**: question, complaint, order, support, general

#### POST /priority
- **Algorithm**: Multi-factor scoring
- **Factors**: 
  - Message length
  - Keywords (urgent, help, problem)
  - Time sensitivity
  - User importance
- **Output**: Ranked message list

#### POST /vector/store
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Storage**: FAISS index
- **Purpose**: Semantic search preparation

#### POST /vector/search
- **Method**: Cosine similarity search
- **Input**: Query text
- **Output**: Similar conversations

#### POST /daily-report
- **Aggregation**: Per-user, per-day
- **Includes**:
  - Conversation count
  - Summary of all chats
  - Priority messages
  - Intent distribution
  - Key insights

### 4. Frontend (Next.js)

**Purpose**: Web interface for viewing and managing messages.

**Technology**:
- Framework: Next.js (React)
- Matrix Client: Matrix Client SDK (REST API)
- Styling: CSS Modules / Tailwind (optional)

**Features**:
- User authentication
- Room list display
- Message viewing
- Real-time updates (polling)
- AI feature integration

**Matrix Integration**:
- Login via Matrix REST API
- Fetch rooms: `GET /_matrix/client/r0/joined_rooms`
- Fetch messages: `GET /_matrix/client/r0/rooms/{roomId}/messages`
- Polling interval: 5 seconds

### 5. NGINX Reverse Proxy

**Purpose**: Route traffic and provide single entry point.

**Configuration**:
- Routes `/` to Synapse (port 8008)
- Routes `/api` to AI Backend (port 8000)
- Enables domain-based access
- Prepares for HTTPS (future)

## Data Flow

### Message Flow (Instagram → Matrix)

1. User sends DM on Instagram
2. Mautrix bridge receives via Instagram API
3. Bridge creates/updates Matrix room
4. Bridge sends message to Synapse
5. Synapse stores message
6. Frontend polls Synapse API
7. Frontend displays message

### AI Analysis Flow

1. Frontend fetches messages from Matrix
2. Frontend sends to AI Backend `/summarize`
3. Backend loads BART model
4. Backend generates summary
5. Backend returns summary
6. Frontend displays summary

### Vector Search Flow

1. Messages stored via `/vector/store`
2. Backend generates embeddings
3. Embeddings stored in FAISS index
4. User queries via `/vector/search`
5. Backend searches FAISS
6. Returns similar conversations

## Why This Architecture?

### Matrix Synapse
- **Decentralized**: No single point of failure
- **Interoperable**: Bridges to any platform
- **Secure**: E2E encryption support
- **Scalable**: Handles millions of users

### Mautrix Bridges
- **Mature**: Well-maintained, active development
- **Flexible**: Supports multiple platforms
- **Reliable**: Battle-tested in production

### FastAPI Backend
- **Fast**: Async support, high performance
- **Modern**: Type hints, auto-docs
- **Easy**: Simple to extend and maintain

### FAISS Vector Store
- **Local**: No external dependencies
- **Fast**: Optimized similarity search
- **Free**: No API costs

## Scalability Considerations

### Current (MVP)
- SQLite database (Synapse)
- Local FAISS index
- Single instance deployment
- Suitable for: < 1000 users

### Production Scaling
- PostgreSQL for Synapse
- Redis for caching
- Pinecone/Weaviate for vectors
- Kubernetes orchestration
- Load balancer
- CDN for static assets

## Security Considerations

### Current
- Basic authentication
- HTTP (development)
- Docker network isolation

### Production
- HTTPS/TLS required
- OAuth2/SSO integration
- Rate limiting
- Input validation
- SQL injection prevention
- XSS protection

## Trade-offs

### Chosen for MVP
- ✅ Docker Compose (simple, single-machine)
- ✅ FAISS (local, no external service)
- ✅ SQLite (no DB setup needed)
- ✅ Polling (simpler than WebSockets)

### Future Improvements
- WebSocket for real-time updates
- PostgreSQL for production
- Redis for caching
- Kubernetes for orchestration
- HTTPS/TLS certificates
- Monitoring and logging

## Performance Metrics

### Expected Performance
- Message latency: < 100ms (local)
- Summarization: 2-5 seconds (first call)
- Intent parsing: < 500ms
- Vector search: < 100ms (small dataset)

### Bottlenecks
- Model loading (first request)
- Large conversation summarization
- Vector index size (scales with data)

## Monitoring

### Recommended Metrics
- Matrix API response time
- AI endpoint latency
- Container resource usage
- Message throughput
- Error rates

### Tools
- Docker stats
- Prometheus (future)
- Grafana (future)
- Application logs

---

**Architecture Version**: 1.0  
**Last Updated**: 2024
