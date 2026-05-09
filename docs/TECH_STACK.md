# AgroFamíliApp - Technical Stack Documentation

## Overview

AgroFamíliApp leverages a state-of-the-art AI stack optimized for AMD Instinct MI300X GPUs, enabling high-performance inference of large language models at scale for Brazilian family farmers.

---

## 1. LLM Inference - vLLM on AMD MI300X

### Why vLLM?

[vLLM](https://docs.vllm.ai/) is an open-source library for fast LLM inference and serving. It uses **PagedAttention** to manage attention KV cache memory efficiently, achieving:

- **2-4x higher throughput** than naive HuggingFace serving
- **24,000 tokens/second** on Llama 3.1 70B with MI300X (192GB VRAM)
- **Continuous batching** for dynamic request handling
- **Tensor parallelism** for multi-GPU scaling

### AMD MI300X Specifications

| Spec | Value |
|------|-------|
| GPU | AMD Instinct MI300X |
| Compute | 1.653 PFLOPS FP8, 3.305 PFLOPS FP16 |
| VRAM | 192GB HBM3 |
| Infinity Fabric | 896 GB/s bidirectional |
| Memory Bandwidth | 5.3 TB/s |

The 192GB VRAM allows **serving Llama 3.1 70B in a single GPU** at full precision (FP16), eliminating tensor-parallelism complexity for this model size.

### Deployment

```bash
# On AMD MI300X node with ROCm 6.0+
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-70B-Instruct \
    --host 0.0.0.0 --port 8001 \
    --gpu-memory-utilization 0.90 \
    --max-model-len 8192 \
    --trust-remote-code
```

### Alternative: Qwen2.5 72B

For higher multilingual capability (Portuguese with regional accents):

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-72B-Instruct \
    --host 0.0.0.0 --port 8001 \
    --gpu-memory-utilization 0.90 \
    --max-model-len 8192
```

---

## 2. Agent Orchestration - LangChain + LangGraph

### Architecture

```
User Query
    │
    ▼
┌─────────────────┐
│ Intent Detection│ ─── Keyword matching + heuristics
│ (gateway.py)    │
└────────┬────────┘
         │ Agent ID
         ▼
┌─────────────────────────────────────┐
│           LangGraph StateGraph      │
│                                     │
│  ┌─────────────────────────────────┐ │
│  │ ATER │ CRÉDITO │ MERCADO │ CLIMA│ │
│  │ DOCS │ TERRITÓRIO                │ │
│  └─────────────────────────────────┘ │
│                                     │
│  Tools:                             │
│  - ChromaDB (RAG)                   │
│  - INMET API                        │
│  - CEPEA API                        │
│  - CONAB API                        │
│  - Memory (Redis)                   │
└─────────────────────────────────────┘
         │
         ▼
    Final Response
```

### Key LangChain Components

| Component | Usage |
|-----------|-------|
| `ChatOpenAI` (compatible with vLLM) | LLM call with system prompts |
| `ChatPromptTemplate` | Structured agent instructions |
| `Chroma` vectorstore | Semantic search over knowledge |
| `RecursiveCharacterTextSplitter` | Document chunking for RAG |
| `ConversationBufferMemory` | Chat history context |

### Agent Prompts (System)

Each agent has a specialized system prompt covering:
- Domain-specific knowledge (credit, agroecology, market, etc.)
- Brazilian Portuguese with regional awareness
- Practical, actionable advice
- Fallback to local EMATER recommendations

---

## 3. Voice Interface - Whisper

### Architecture

```
Microphone Input
      │
      ▼
Web Speech API (MediaRecorder)
      │
      ▼
Base64 Audio
      │
      ▼
FastAPI /chat endpoint
      │
      ▼
Whisper (openai-whisper)
      │
      ▼
Transcribed Text
      │
      ▼
Intent Detection + Agent
```

### Whisper Models

| Model | Size | Languages | Use Case |
|-------|------|-----------|---------|
| `base` | 74M params | 99 languages | Fast, local (recommended for demo) |
| `small` | 244M params | 99 languages | Better accuracy |
| `medium` | 769M params | 99 languages | Best accuracy, slower |

### Code

```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.webm", language="pt")
print(result["text"])
```

---

## 4. RAG - ChromaDB + Sentence-Transformers

### Pipeline

```
Knowledge Docs (.txt/.md)
        │
        ▼
RecursiveCharacterTextSplitter
  - chunk_size: 500
  - chunk_overlap: 50
        │
        ▼
sentence-transformers/
paraphrase-multilingual-MiniLM-L12-v2
        │
        ▼
ChromaDB Vector Store
        │
        ▼
User Query → Embedding → Similarity Search
```

### Multilingual Embeddings

We use `paraphrase-multilingual-MiniLM-L12-v2` because:

- Trained on 50+ languages including Portuguese
- 384-dimensional embeddings
- 4x faster than multilingual-e5-large
- Optimal for Brazilian Portuguese agricultural text

### Knowledge Categories

| Category | Content |
|----------|---------|
| `sintropia/` | SAFs, succession, stratification, pruning |
| `biodinamica/` | BD preparations, lunar calendar, rhythms |
| `organica/` | Certification, allowed inputs, transition |
| `natural/` | Fukuoka principles, no-till, seed selection |
| `politicas/` | PRONAF, CAF, PAA, PNAE, legislation |

---

## 5. Memory - Redis

### Conversation Memory

Each user session maintains conversation history in Redis:

- **Key format**: `agrofam:conv:{user_id}`
- **Max history**: 20 messages
- **TTL**: 30 days
- **Structure**: JSON `{"role", "content", "agent"}`

### Usage in Agents

```python
history = await memory.get_history(user_id)
context = "\n".join([f"{m['role']}: {m['content']}" for m in history])
```

---

## 6. External APIs

### INMET (Weather)

```
GET https://apihm.inmet.gov.br/previsao/{city_code}
GET https://apihm.inmet.gov.br/estacao/{state}
```

Provides 5-day forecasts, temperature, humidity, rainfall.

### CEPEA (Prices)

```
GET https://www.cepea.esalq.usp.br/api/v1/product/{product}
GET https://www.cepea.esalq.usp.br/api/v1/cesta/familia
```

Provides commodity prices: corn, soybean, coffee, rice, cattle, milk.

### CONAB (Markets)

```
GET https://portaldeinformacoes.conab.gov.br/api/precos
GET https://portaldeinformacoes.conab.gov.br/api/paa/chamadas
```

Provides PAA calls, reference prices by municipality.

---

## 7. Channels

### WhatsApp (Twilio)

```
WhatsApp User
      │
      ▼
Twilio Cloud (webhook)
      │
      ▼
Flask /webhook/whatsapp
      │
      ▼
FastAPI /chat
      │
      ▼
Twilio reply (SMS)
```

### Telegram

```
Telegram User
      │
      ▼
Telegram Bot API
      │
      ▼
python-telegram-bot webhook
      │
      ▼
FastAPI /chat
```

### WebApp (React PWA)

- Vite + React 18 + TailwindCSS
- Service Worker for offline support
- Installable as native app (Android/iOS)
- Web Speech API for voice input

---

## 8. Dashboard - Streamlit

Manager dashboard showing:

- Total interactions per agent
- Average user rating
- Geographic distribution
- Most asked topics

Built with `streamlit`, `pandas`, `plotly`.

---

## 9. Infrastructure - AMD Developer Cloud

### Getting Started

1. **Register** at [amd.com/en/developer/ai-dev-program.html](https://www.amd.com/en/developer/ai-dev-program.html)
2. **Receive $100 credits** via email
3. **Access** [developer.amd.com/cloud](https://developer.amd.com/cloud/)
4. **Spin up** MI300X instance with ROCm 6.0

### Instance Configuration

| Resource | Recommended |
|----------|-------------|
| GPU | AMD Instinct MI300X |
| vCPUs | 64 |
| RAM | 512GB |
| Storage | 500GB NVMe |
| OS | Ubuntu 22.04 LTS |
| ROCm | 6.0+ |

### ROCm Setup

```bash
# Install ROCm (if not pre-installed)
wget https://repo.radeon.com/rocm/rocm-install.sh
sudo sh rocm-install.sh --install
# Reboot, verify with:
rocm-smi
```

---

## 10. Docker Deployment

```yaml
# docker-compose.yml (key sections)
services:
  backend:
    build: .
    ports: ["8000:8000"]
    environment:
      - AMD_API_ENDPOINT=http://vllm:8001
    deploy:
      resources:
        reservations:
          devices:
            - driver: amd.com
              count: all
              capabilities: [gpu]

  vllm:
    image: vllm/vllm-openai:latest
    ports: ["8001:8000"]
    command: >
      --model meta-llama/Llama-3.1-70B-Instruct
      --gpu-memory-utilization 0.90
    deploy:
      resources:
        reservations:
          devices:
            - driver: amd.com
              count: 1
              capabilities: [gpu]
```

---

## Version Matrix

| Component | Version | Notes |
|-----------|---------|-------|
| Python | 3.11+ | |
| FastAPI | 0.115+ | |
| LangChain | 0.3+ | |
| CrewAI | 0.61+ | |
| ChromaDB | 0.5+ | |
| vLLM | 0.6.6+ | AMD MI300X optimized |
| Whisper | 1.0+ | openai-whisper |
| Redis | 7+ | |
| React | 18.3+ | |
| Vite | 5.4+ | |
| TailwindCSS | 3.4+ | |
| ROCm | 6.0+ | AMD MI300X |