# AgroFamíliApp - AMD Developer Cloud Deployment Guide

This guide provides step-by-step instructions for deploying AgroFamíliApp on the AMD Developer Cloud using the AMD Instinct MI300X GPU.

---

## Prerequisites

1. **AMD AI Developer Program membership** (free)
   - Register: https://www.amd.com/en/developer/ai-dev-program.html
   - Receive **$100 in cloud credits** via email

2. **AMD Developer Cloud access**
   - Portal: https://developer.amd.com/cloud/
   - SSH key configured

3. **Basic familiarity** with:
   - Linux command line
   - Docker and containerization
   - Python and FastAPI

---

## Step 1: Access AMD Developer Cloud

### 1.1 Log in to the Dashboard

```
1. Go to: https://developer.amd.com/cloud/
2. Click "Sign In" → Use your AMD developer account
3. Navigate to "Instances" or "Launch Instance"
```

### 1.2 Select Instance Type

For AgroFamíliApp (Llama 3.1 70B inference):

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| GPU | AMD Instinct MI300X (1x) | AMD Instinct MI300X (1x) |
| vCPUs | 32 | 64 |
| RAM | 256GB | 512GB |
| Storage | 200GB NVMe | 500GB NVMe |
| OS | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |

> **Note**: Llama 3.1 70B fits in a single MI300X (192GB VRAM) at FP16, no tensor-parallelism needed.

### 1.3 Launch Instance

```bash
# SSH into your instance
ssh ubuntu@<your-instance-ip>
```

---

## Step 2: Install ROCm (if not pre-installed)

The AMD Developer Cloud typically has ROCm pre-installed. Verify:

```bash
# Check ROCm version
rocm-smi

# Should output GPU info:
# GPU[0]: AMD Instinct MI300X
# Memory: 192 GB
```

If ROCm is not installed:

```bash
# Install ROCm 6.0
wget https://repo.radeon.com/rocm/rocm-install.sh
chmod +x rocm-install.sh
sudo ./rocm-install.sh --install

# Add ROCm to PATH
echo 'export PATH=/opt/rocm/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Verify
rocm-smi
```

---

## Step 3: Clone Repository

```bash
# Clone AgroFamíliApp
git clone https://github.com/catitodev/agrofamiliapp.git
cd agrofamiliapp

# Create Python virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

Key variables:

```bash
# AMD Developer Cloud vLLM endpoint
# Usually the internal IP of your vLLM container
AMD_API_ENDPOINT=http://localhost:8001/v1
AMD_API_KEY=EMPTY  # vLLM may not require key

# Optional: External APIs
INMET_API_KEY=your-key-here
TELEGRAM_BOT_TOKEN=your-telegram-token

# Infrastructure
REDIS_URL=redis://localhost:6379
CHROMA_PERSIST_DIR=./knowledge/vectorstore
```

---

## Step 5: Start vLLM Server (Llama 3.1 70B)

This is the LLM inference server running on the MI300X GPU.

```bash
# Create a startup script
cat > start_vllm.sh << 'EOF'
#!/bin/bash
export ROCM_PATH=/opt/rocm
export HSA_OVERRIDE_GFX_VERSION=11.0.0

python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-70B-Instruct \
    --host 0.0.0.0 \
    --port 8001 \
    --gpu-memory-utilization 0.90 \
    --max-model-len 8192 \
    --trust-remote-code \
    --dtype half \
    --enforce-eager
EOF

chmod +x start_vllm.sh

# Run vLLM (will download model on first run ~140GB)
./start_vllm.sh
```

> **First run**: Downloads Llama 3.1 70B model (~140GB). Takes 15-30 minutes depending on bandwidth.
> **Subsequent runs**: Uses cached model.

To verify vLLM is running:

```bash
# Test API
curl http://localhost:8001/v1/models

# Should return:
# {"object":"list","data":[{"id":"meta-llama/Llama-3.1-70B-Instruct",...}]}
```

### Alternative: Using a GGUF Model (Q5_K_M)

For faster startup and lower memory:

```bash
# Use a quantized GGUF model with llama.cpp
# Download from HuggingFace: TheBloke/Llama-3.1-70B-Instruct-GGUF

# Use vLLM with GGUF:
python -m vllm.entrypoints.openai.api_server \
    --model ./models/Llama-3.1-70B-Instruct-Q5_K_M.gguf \
    --tokenizer hf-internal-testing/llama-tokenizer \
    --gpu-memory-utilization 0.90
```

---

## Step 6: Start Redis (Conversation Memory)

```bash
# Start Redis (if Docker is available)
docker run -d \
  --name agrofam-redis \
  -p 6379:6379 \
  redis:7-alpine

# Or install and run directly
sudo apt install redis-server
sudo systemctl start redis
```

Verify:
```bash
redis-cli ping
# Should output: PONG
```

---

## Step 7: Start ChromaDB (Vector Store)

```bash
# Start ChromaDB
docker run -d \
  --name agrofam-chroma \
  -p 8000:8000 \
  -v chroma-data:/data \
  chromadb/chroma:latest

# Or run via Python
pip install chromadb
chromadb --host 0.0.0.0 --port 8000
```

---

## Step 8: Build and Run FastAPI Backend

```bash
# Ensure vLLM is running on port 8001
# Ensure Redis is running on port 6379
# Ensure ChromaDB is running on port 8000

# Build knowledge base (optional - creates vector store)
python -c "
from knowledge.base import kb
kb.load_documents('./knowledge')
print('Knowledge base ready!')
"

# Start the FastAPI gateway
uvicorn core.gateway:app --host 0.0.0.0 --port 8000 --reload
```

Test the API:

```bash
# Health check
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Como planto milho no Sertão?", "user_id": "test-user"}'

# Should return JSON with agent response
```

---

## Step 9: Deploy with Docker Compose (Recommended)

For a production-ready deployment:

```bash
# Create a production docker-compose file
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  vllm:
    image: vllm/vllm-openai:latest
    container_name: agrofam-vllm
    ports:
      - "8001:8000"
    environment:
      - ROCCH_PATH=/opt/rocm
    volumes:
      - ./models:/models
    command: >
      --model meta-llama/Llama-3.1-70B-Instruct
      --host 0.0.0.0
      --port 8000
      --gpu-memory-utilization 0.90
      --max-model-len 8192
      --trust-remote-code
    deploy:
      resources:
        reservations:
          devices:
            - driver: amd.com
              count: 1
              capabilities: [gpu]

  redis:
    image: redis:7-alpine
    container_name: agrofam-redis
    ports:
      - "6379:6379"

  backend:
    build: .
    container_name: agrofam-backend
    ports:
      - "8000:8000"
    environment:
      - AMD_API_ENDPOINT=http://vllm:8000/v1
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
      - vllm
    command: uvicorn core.gateway:app --host 0.0.0.0 --port 8000

networks:
  default:
    driver: bridge
EOF

# Start everything
docker-compose -f docker-compose.prod.yml up -d
```

---

## Step 10: Run the React WebApp

On a separate machine or in a separate terminal:

```bash
cd channels/webapp
npm install
npm run dev
# Runs on http://localhost:3000
```

For production:

```bash
npm run build
# Serve dist/ with nginx or any static file server
```

---

## Step 11: Configure Telegram Bot (Optional)

1. Open Telegram → Search @BotFather
2. Send `/newbot`
3. Follow prompts → Get your **bot token**
4. Add to `.env`: `TELEGRAM_BOT_TOKEN=your-token-here`
5. Run bot:

```bash
python channels/telegram_bot.py
```

6. Set webhook:
```bash
# Replace YOUR_TOKEN and YOUR_DOMAIN
curl -X POST https://api.telegram.org/botYOUR_TOKEN/setwebhook \
  -d "url=https://your-domain.com/webhook/telegram"
```

---

## Step 12: Configure WhatsApp (Optional)

1. Set up Twilio account: https://www.twilio.com/whatsapp
2. Get your Account SID and Auth Token
3. Add to `.env`:
```bash
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
```
4. Run webhook server:

```bash
python channels/whatsapp_webhook.py
```

5. Configure Twilio webhook URL in Twilio console

---

## Quick Test Checklist

- [ ] AMD MI300X accessible via `rocm-smi`
- [ ] vLLM running on port 8001: `curl http://localhost:8001/v1/models`
- [ ] Redis on port 6379: `redis-cli ping` → PONG
- [ ] ChromaDB on port 8000
- [ ] FastAPI on port 8000: `curl http://localhost:8000/health`
- [ ] Chat works: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"text": "Oi", "user_id": "test"}'`

---

## Performance Benchmarking

On AMD MI300X (single GPU, Llama 3.1 70B):

| Metric | Value |
|--------|-------|
| Throughput | ~24,000 tokens/sec |
| Time to First Token | ~200ms |
| Memory Usage | ~160GB (83% of 192GB) |
| Concurrent Users | ~100+ at good latency |
| Cold Start (model load) | ~3-5 minutes |

Run benchmark:

```bash
# With wrk or locust
pip install locust
locust -f locustfile.py --host=http://localhost:8000
```

---

## Troubleshooting

### GPU Not Detected

```bash
# Check ROCm installation
ls /opt/rocm/
rocm-smi

# If empty, reinstall ROCm
./rocm-install.sh --install
```

### vLLM Fails with OOM

```bash
# Reduce memory utilization
--gpu-memory-utilization 0.75

# Or use smaller model
--model TheBloke/Llama-3.1-70B-Instruct-GGUF
```

### Model Download Fails

```bash
# Use HuggingFace CLI
huggingface-cli download meta-llama/Llama-3.1-70B-Instruct \
  --local-dir ./models/Llama-3.1-70B-Instruct

# Or set HF token
export HF_TOKEN=your-hf-token
```

### Connection Refused (vLLM)

```bash
# Check vLLM is listening
netstat -tlnp | grep 8001

# Check logs
docker logs agrofam-vllm
```

---

## Cost Estimation

Using AMD Developer Cloud pricing (approx.):

| Component | Cost/hour | Notes |
|-----------|-----------|-------|
| MI300X instance | ~$3-5/hour | Main cost |
| Storage | ~$0.1/hour | Minimal |
| Data transfer | ~$0.05/GB | Low usage |

**Estimated daily cost**: ~$50-80/day for full stack
**$100 credits**: ~1.5-2 days of full operation

> **Tip**: Use autoscaling to stop instances when not in use.

---

## Next Steps After Demo

1. **Fine-tune the model** with agricultural Brazilian Portuguese data
2. **Expand RAG knowledge base** with regional content
3. **Add TTS** for voice responses
4. **Deploy multi-region** for lower latency
5. **Add monitoring** with Grafana + Prometheus