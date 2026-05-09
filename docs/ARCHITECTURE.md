# AgroFamíliApp - System Architecture

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         END USERS                                     │
│   WhatsApp          Telegram         WebApp (PWA)         Voice       │
└──────────────┬───────────────┬──────────────┬──────────────┬──────────┘
               │               │              │              │
               ▼               ▼              ▼              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     CHANNEL LAYER                                     │
│   Twilio Webhook   Telegram Bot   React Frontend    Web Speech API     │
│                   (python-telegram-bot)                               │
└─────────────────────────────┬────────────────────────────────────────┘
                              │ JSON / HTTP
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    CORE GATEWAY (FastAPI)                             │
│                                                                       │
│   ┌─────────────┐  ┌──────────────┐  ┌────────────────────────────┐  │
│   │  STT/Whisper│  │ Intent Detect│  │  Rate Limiting / Auth     │  │
│   │  (if audio) │  │  (keyword)   │  │  (user_id, throttle)      │  │
│   └─────────────┘  └──────────────┘  └────────────────────────────┘  │
│                              │                                        │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                CONVERSATION MEMORY (Redis)                   │   │
│   │          Context window: last 20 messages, 30d TTL          │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                              │                                        │
│                              ▼                                        │
│              ┌───────────────────────────────┐                       │
│              │      AGENT ROUTING            │                       │
│              │   LangChain + LangGraph       │                       │
│              └───────────────────────────────┘                       │
│                              │                                        │
│         ┌──────────┬─────────┼──────────┬──────────┐                │
│         ▼          ▼         ▼          ▼          ▼                │
│    ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐      │
│    │  ATER  │ │CRÉDITO│ │MERCADO │ │ CLIMA  │ │ DOCS  │ │TERRIT.│      │
│    └────────┘└────────┘└────────┘└────────┘└────────┘└────────┘      │
└──────────────────────────────────────┬───────────────────────────────┘
                                       │
           ┌────────────────────────────┼────────────────────────────┐
           │                            │                            │
           ▼                            ▼                            ▼
┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│   LLM LAYER (vLLM)      │  │     RAG LAYER            │  │    DATA LAYER            │
│                         │  │                         │  │                         │
│  AMD Instinct MI300X   │  │  ChromaDB +             │  │  External APIs:          │
│  Llama 3.1 70B         │  │  sentence-transformers  │  │  - INMET (weather)       │
│  (FP16, 192GB VRAM)    │  │  (paraphrase-multilin- │  │  - CEPEA (prices)        │
│  vLLM PagedAttention   │  │   gual-MiniLM-L12-v2)  │  │  - CONAB (markets)       │
│  ~24k tokens/sec       │  │                         │  │  - IBGE (municipal)     │
│                         │  │  Knowledge Base:       │  │  - MAPA (certification)  │
│                         │  │  - sintropia/          │  │                         │
│                         │  │  - biodinamica/        │  │                         │
│                         │  │  - organica/           │  │                         │
│                         │  │  - natural/            │  │                         │
│                         │  │  - politicas/          │  │                         │
│                         │  │                         │  │                         │
│                         │  │  External APIs:         │  │                         │
│                         │  │  - EMBRAPA              │  │                         │
│                         │  │  - MAPA                 │  │                         │
│                         │  │  - MDA                  │  │                         │
│                         │  │  - INMET                │  │                         │
│                         │  │                         │  │                         │
│                         │  │                         │  │                         │
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    FEEDBACK LAYER                                      │
│   Anonymous interaction logging (SHA256 hashed user_id)              │
│   User ratings (1-5 stars) + comments                                  │
│   Aggregate stats for dashboard (Streamlit)                          │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Channel Layer

| Channel | Technology | Protocol |
|---------|-----------|----------|
| WhatsApp | Twilio / Z-API | Webhook (HTTPS POST) |
| Telegram | python-telegram-bot | Long Polling / Webhook |
| WebApp | React 18 + Vite | WebSocket + REST |
| Voice | Web Speech API + Whisper | MediaRecorder API |

### 2. Gateway (core/gateway.py)

- **FastAPI application** with CORS middleware
- **POST /chat**: Main entry point — accepts text or audio
- **Intent detection**: Keyword-based routing to 6 agents
- **Redis memory**: Conversation context per user
- **Feedback logging**: Anonymous interaction tracking

### 3. Agent Layer (agents/)

Each agent is a **LangChain chain** with:

1. **System prompt**: Specialized knowledge for the domain
2. **LLM call**: ChatOpenAI-compatible with vLLM backend
3. **Context augmentation**: RAG results injected into prompt
4. **Tool calls**: External API integrations

```
Agent Template:
┌─────────────────────────────────────┐
│ System: [Domain knowledge prompt]   │
├─────────────────────────────────────┤
│ Context: [RAG retrieved docs]       │
├─────────────────────────────────────┤
│ History: [Redis conversation]       │
├─────────────────────────────────────┤
│ Input:  [User question]             │
├─────────────────────────────────────┤
│ LLM:   [Llama 3.1 70B via vLLM]    │
├─────────────────────────────────────┤
│ Output: [Response + suggestions]   │
└─────────────────────────────────────┘
```

### 4. Knowledge Base (knowledge/base.py)

- **ChromaDB** vector store with persistent storage
- **Embedding model**: paraphrase-multilingual-MiniLM-L12-v2 (384d)
- **Chunking**: RecursiveCharacterTextSplitter (500 chars, 50 overlap)
- **Search**: Top-3 similarity search per query

### 5. Data Layer (data/)

| Module | API | Data |
|--------|-----|------|
| `inmet.py` | INMET public API | Weather forecasts, stations |
| `cepea.py` | CEPEA/ESALQ | Commodity prices |
| `conab.py` | CONAB portal | PAA calls, reference prices |
| `mapa_sda.py` | MAPA/Gov.br | Organic certification |

---

## Data Flow Examples

### Example 1: Text Query - "Como obter PRONAF?"

```
User types → WhatsApp → Twilio webhook → POST /chat
                                                  │
                                                  ▼
                                          Gateway (gateway.py)
                                                  │
                                                  ▼
                                          Intent Detection:
                                          keywords["empréstimo", "pronaf"]
                                          → agent: "credito"
                                                  │
                                                  ▼
                                          CreditoAgent.generate()
                                                  │
                                      ┌───────────┴───────────┐
                                      ▼                       ▼
                              ChromaDB RAG           Redis Memory
                              (credit policies)      (no prior history)
                                      │                       │
                                      └───────────┬───────────┘
                                                  ▼
                                          LLM (vLLM/MI300X)
                                          "PRONAF requires CAF..."
                                                  │
                                                  ▼
                                          Response + suggestions
                                                  │
                                                  ▼
                                          Redis (log interaction)
                                          Telegram (send reply)
```

### Example 2: Voice Query - "Quando planto meu milho?"

```
User speaks → WebApp (MediaRecorder) → Audio blob
                                            │
                                            ▼
                                    POST /chat {audio: "..."}
                                            │
                                            ▼
                                    gateway.py:
                                    stt_engine.transcribe(audio)
                                            │
                                            ▼
                                    Whisper output: "Quando planto meu milho?"
                                            │
                                            ▼
                                    Intent detection → "clima"
                                            │
                                            ▼
                                    ClimaAgent:
                                    - fetch_weather(city)
                                    - RAG: planting calendars
                                            │
                                            ▼
                                    LLM response
                                            │
                                            ▼
                                    Audio text response
                                    (TTS optional for future)
```

---

## Deployment Topology

```
                    INTERNET
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
    WhatsApp       Telegram        WebApp
    (Twilio)       (Bot API)      (Browser)
         │              │              │
         └──────────────┴──────────────┘
                        │
                        ▼
              ┌─────────────────────┐
              │   AMD Developer     │
              │   Cloud             │
              │                     │
              │  ┌───────────────┐  │
              │  │  nginx       │  │
              │  │  (SSL, LB)   │  │
              │  └───────┬───────┘  │
              │          │          │
              │  ┌───────┴───────┐  │
              │  │ FastAPI       │  │
              │  │ Gateway       │  │
              │  │ (uvicorn)     │  │
              │  └───────┬───────┘  │
              │          │          │
              │  ┌───────┴───────┐  │
              │  │ vLLM Server   │  │
              │  │ Llama 3.1 70B │  │
              │  │ (MI300X GPU)  │  │
              │  └───────────────┘  │
              │                     │
              │  ┌───────────────┐  │
              │  │ Redis         │  │
              │  │ ChromaDB      │  │
              │  │ (Volumes)     │  │
              │  └───────────────┘  │
              └─────────────────────┘
```

---

## Security Model

1. **User privacy**: User IDs hashed with SHA256 before logging
2. **API authentication**: Environment variables, no secrets in code
3. **Webhook validation**: Twilio signature verification
4. **Rate limiting**: Per-user throttling (configurable)
5. **Input sanitization**: Pydantic validation on all inputs
6. **AGPL license**: Any derivative work must be open-source

---

## Scalability Considerations

| Component | Scaling Strategy |
|-----------|-----------------|
| FastAPI Gateway | Horizontal (multiple replicas behind load balancer) |
| vLLM | Vertical (MI300X handles Llama 3.1 70B in 1 GPU) or Horizontal (tensor-parallel on 2+ MI300X) |
| Redis | Redis Cluster for session persistence |
| ChromaDB | Chroma supports distributed deployment |
| WebApp | CDN for static assets, SSR for SEO |

Current design supports **~10,000 concurrent conversations** on a single MI300X node (vLLM can handle ~100+ concurrent users at good latency). For higher scale, deploy multiple gateway replicas behind nginx. |
|  |  |