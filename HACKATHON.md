# AgroFamíliApp - AMD Developer Hackathon

**May 9-10, 2026 | San Francisco, CA**

AI conversational agent for Brazilian family farmers, powered by AMD Instinct MI300X.

## Quick Start

### Prerequisites
- AMD AI Developer Program membership
- AMD Developer Cloud access with MI300X instance

### Deployment

```bash
# Clone
git clone https://github.com/catitodev/agrofamiliapp.git
cd agrofamiliapp

# Configure
cp .env.example .env

# Start infrastructure
docker-compose up -d redis chromadb

# Start vLLM (on MI300X)
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-70B-Instruct \
    --host 0.0.0.0 --port 8001

# Start API
uvicorn core.gateway:app --host 0.0.0.0 --port 8000
```

## Architecture

```
AMD MI300X (vLLM + Llama 3.1 70B)
        │
        ▼
FastAPI Gateway (LangChain agents)
        │
        ├── ATER (agroecological assistance)
        ├── Crédito (PRONAF, CAF)
        ├── Mercado (PAA, PNAE)
        ├── Clima (INMET weather)
        ├── Docs (certification)
        └── Território (EMATER, cooperatives)

Channels: WhatsApp | Telegram | React WebApp
```

## Demo

Access at: http://localhost:8000
API: http://localhost:8000/chat

## Team

Built with ❤️ for Brazilian family farmers by the AgroFamíliApp team.

## License

GNU AGPL v3 - Public Good