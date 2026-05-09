# AgroFamíliApp

## AI-Powered Agroecological Assistant for Brazilian Family Farmers

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-green.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Project Type: Public Good](https://img.shields.io/badge/type-public%20good-brightgreen)](https://github.com/catitodev/agrofamiliapp)
[![Status](https://img.shields.io/badge/status-active%20development-blue)](https://github.com/catitodev/agrofamiliapp)
[![AMD MI300X](https://img.shields.io/badge/AMD-MI300X-ED1C24?logo=amd)](https://www.amd.com/en/accelerators/instinct/mi300x)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com/)

---

## What is AgroFamíliApp?

AgroFamíliApp is a **free, open-source, multilingual AI conversational agent** (voice and text) designed specifically for **Brazilian family farmers**. It provides real-time agricultural assistance through WhatsApp, Telegram, and a WebApp — accessible even in low-connectivity rural areas.

The system connects farmers to real data: weather forecasts, market prices, rural credit programs, organic certification pathways, and agroecological technical knowledge. Every interaction makes the system smarter — collectively.

> *"The more farmers use it, the better it becomes — data belongs to the community, never to corporations."*

---

## The Problem

Brazil has **3.9 million family farming establishments** (IBGE 2017 Census[^1]), responsible for **70% of the food on Brazilian tables**[^2]. Yet these farmers face:

- **Insufficient public ATER** (Technical Assistance and Rural Extension) — only 20% have regular access[^3]
- **Geographic concentration** — extension services are unavailable in remote areas
- **Information asymmetry** — decisions on planting, credit, and markets rely on oral tradition
- **Bureaucratic complexity** — navigating CAF, PRONAF, PAA, PNAE is overwhelming
- **Limited connectivity** — many rural areas lack reliable internet for video/calls

This leads to:
- Crops planted at wrong times due to lack of climate data
- Missed credit opportunities from lack of guidance
- Produce lost to lack of market access information
- Certification abandoned due to complex procedures

[^1]: IBGE, **Censo Agropecuário 2017**, Table 1: Agricultural establishments by category.
[^2]: MDA/PRONAF, **Portal da Agricultura Familiar**, 2023 — "A agricultura familiar é responsável por 70% dos alimentos consumed no Brasil."
[^3]: MAPA, **Plano ATER Brasil 2023-2030**, p.12 — "Apenas 20% dos agricultores familiares têm accesso regular a serviços de ATER."

---

## The Solution

An **AI conversational agent** that speaks the farmer's language — literally. Built on **AMD Instinct MI300X GPUs** via the AMD Developer Cloud, running open-source models (Llama 3.1 70B via vLLM), AgroFamíliApp provides:

```
┌─────────────────────────────────────────────────────────────┐
│                    AGROFAMÍLIAPP                             │
│                                                             │
│   📱 WhatsApp / Telegram / WebApp                           │
│                                                             │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│   │  Voice  │  │  Text   │  │   RAG   │  │ Intent  │        │
│   │(Whisper)│  │Parsing  │  │Knowledge│  │Routing  │        │
│   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│        │            │            │            │              │
│        └────────────┼────────────┼────────────┘              │
│                     ▼                                      │
│          ┌─────────────────────┐                            │
│          │   FastAPI Gateway   │                            │
│          │   (LangChain/LangGraph)│                          │
│          └──────────┬──────────┘                            │
│                     ▼                                      │
│   ┌──────────────────────────────────────────┐             │
│   │         AMD MI300X + vLLM                │             │
│   │   Llama 3.1 70B / Qwen2.5 + ChromaDB     │             │
│   └──────────────────────────────────────────┘             │
│                                                             │
│   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│   │ ATER │ │CRÉDITO│ │MERCADO│ │CLIMA │ │ DOCS │ │TERRI.│   │
│   └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
│                                                             │
│   External APIs: INMET, CEPEA, CONAB, IBGE, MAPA           │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Features

### 🤖 6 Specialized AI Agents

| Agent | Capability | Sample Query |
|-------|-----------|-------------|
| **ATER** | Agroecological technical assistance (sintropic, biodynamic, organic, natural) | *"Como plantar SAF de cacau no Sul da Bahia?"* |
| **CRÉDITO** | Rural credit: PRONAF, CAF, PNCF, Garantia-Safra, SEAF | *"Como conseguir R$ 50 mil do PRONAF?"* |
| **MERCADO** | Market access: PAA, PNAE, direct sales, prices | *"Como vender para a merenda escolar da minha cidade?"* |
| **CLIMA** | Weather forecasts, planting calendars, climate alerts | *"Vai chover essa semana em Petrolina?"* |
| **DOCS** | Documentation: CAF, CNPJ Rural, organic certification, SIM | *"Como obter certificação orgânica para meu café?"* |
| **TERRITÓRIO** | Rural services map: EMATER, cooperatives, markets | *"Onde fica a EMATER mais perto de Juazeiro?"* |

### 🎤 Voice & Text Interface
- **Voice input** via Web Speech API + Whisper transcription
- Works in **Brazilian Portuguese with regional accents** (Northeast, South, Southeast, etc.)
- Accessible to farmers with low literacy

### 🌐 Multi-Channel
- WhatsApp (via Twilio/Z-API webhook)
- Telegram bot
- WebApp (React PWA, installable)

### 🧠 RAG Knowledge Base
- Vectorized agricultural knowledge from EMBRAPA, MAPA, MDA, INMET
- Covers all four agroecological approaches
- Updated via community contributions

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM Inference** | **vLLM** + Llama 3.1 70B | High-throughput inference on AMD MI300X |
| **GPU** | **AMD Instinct MI300X** (192GB VRAM) | Training and serving large models |
| **Agent Orchestration** | **LangChain** + LangGraph | Multi-agent routing, tool use |
| **Voice STT** | **Whisper** (open-source) | Speech-to-text for voice queries |
| **Vector Store** | **ChromaDB** + sentence-transformers | RAG semantic search |
| **Backend** | **FastAPI** (Python 3.11+) | REST API + WebSocket |
| **WebApp** | **React 18** + Vite + TailwindCSS | PWA installer |
| **Channels** | Twilio, python-telegram-bot | WhatsApp & Telegram bots |
| **Data Sources** | INMET, CEPEA, CONAB, IBGE, MAPA | Real-time agricultural data |
| **Dashboard** | **Streamlit** | Public policy manager panel |
| **Infrastructure** | **AMD Developer Cloud** | Cloud GPU access |
| **License** | **GNU AGPL v3** | Open-source public good |

---

## Architecture

```
agrofamiliapp/
├── core/                    # Core infrastructure
│   ├── gateway.py          # FastAPI entry point + intent routing
│   ├── config.py           # Environment configuration
│   ├── memory.py           # Redis-backed conversation memory
│   ├── feedback.py         # Anonymous feedback collection
│   └── stt.py             # Whisper speech-to-text engine
│
├── agents/                  # AI specialist agents (LangChain)
│   ├── ater.py             # Agroecological technical assistance
│   ├── credito.py          # Rural credit and public policies
│   ├── mercado.py          # Market access and commercialization
│   ├── clima.py            # Weather and crop planning
│   ├── docs.py             # Documentation and legal compliance
│   └── territorio.py       # Rural services and territory
│
├── knowledge/               # RAG knowledge base
│   ├── sintropia/          # Syntropic agriculture docs
│   ├── biodinamica/        # Biodynamic agriculture docs
│   ├── organica/           # Organic certification docs
│   ├── natural/            # Natural farming docs
│   ├── politicas/          # Public policies docs
│   └── base.py             # ChromaDB + embedding pipeline
│
├── channels/                # Multi-channel interface
│   ├── telegram_bot.py     # Telegram bot (python-telegram-bot)
│   ├── whatsapp_webhook.py # WhatsApp webhook (Flask/Twilio)
│   └── webapp/             # React PWA frontend
│
├── data/                    # External API integrations
│   ├── inmet.py            # INMET weather API
│   ├── cepea.py            # CEPEA price API
│   ├── conab.py            # CONAB price/market API
│   └── mapa_sda.py         # MAPA/SISORG API
│
├── dashboard/               # Public manager dashboard
│   └── app.py             # Streamlit dashboard
│
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Full stack deployment
└── .env.example             # Environment variables template
```

---

## Deployment on AMD Developer Cloud

### Prerequisites
1. Join the [AMD AI Developer Program](https://www.amd.com/en/developer/ai-dev-program.html)[^4] to receive **$100 in credits**
2. Access [AMD Developer Cloud](https://developer.amd.com/cloud/)[^5]
3. Spin up a node with **AMD Instinct MI300X** (192GB VRAM)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/catitodev/agrofamiliapp.git
cd agrofamiliapp

# Configure environment
cp .env.example .env
# Edit .env with your AMD Developer Cloud endpoint and API keys

# Install Python dependencies
pip install -r requirements.txt

# Start infrastructure (Redis + ChromaDB)
docker-compose up -d redis chromadb

# Start vLLM server with Llama 3.1 70B
# Run this on AMD MI300X node:
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-70B-Instruct \
    --host 0.0.0.0 --port 8001 \
    --tensor-parallel-size 2 \
    --trust-remote-code

# Start the API gateway
uvicorn core.gateway:app --host 0.0.0.0 --port 8000 --reload

# Start the React WebApp (separate terminal)
cd channels/webapp
npm install && npm run dev
```

### Docker Deployment

```bash
# Full stack deployment
docker-compose up -d
```

> **Note**: vLLM requires ROCm 6.0+ on AMD GPUs. The Docker image is pre-configured with ROCm support.

---

## External Data Sources

AgroFamíliApp integrates with:

| Source | API | Data Provided |
|--------|-----|---------------|
| **INMET** | `apihm.inmet.gov.br` | Weather forecasts, station data |
| **CEPEA/ESALQ** | `cepea.esalq.usp.br` | Commodity prices (corn, soybean, coffee, etc.) |
| **CONAB** | `portaldeinformacoes.conab.gov.br` | PAA calls, reference prices |
| **IBGE** | `sidra.ibge.gov.br` | Municipal data, agricultural census |
| **MAPA** | `gov.br/agricultura` | Organic certification, SISORG |

---

## Contributing

AgroFamíliApp is a **public good**. Contributions are welcome.

### Priority Areas
- Agroecological technical content in `knowledge/` (especially regional practices)
- New channel integrations (SMS, USSD for low-connectivity areas)
- Indigenous and regional language support
- Real-time data API integrations
- Agronomic validation of content

### How to Contribute
1. Fork the repository
2. Create a branch: `git checkout -b feature/your-contribution`
3. Make changes with tests
4. Open a PR with a clear description

**Code of Conduct**: This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

---

## UN SDG Alignment

| SDG | Target | How AgroFamíliApp Contributes |
|-----|--------|-------------------------------|
| **1** | No Poverty | Increasing family farmer income via market access + credit |
| **2** | Zero Hunger | Strengthening food production by 70% of Brazilian food supply |
| **8** | Decent Work | Improving rural worker income and conditions |
| **10** | Reduced Inequalities | Democratizing access to technical knowledge |
| **12** | Responsible Consumption | Promoting agroecological and organic production |
| **13** | Climate Action | Adapting to climate change via agroecological practices |
| **15** | Life on Land | SAFs, regeneration, biodiversity preservation |

---

## License

**GNU Affero General Public License v3.0 (AGPL-3.0)**

This software is and always will be a public good. Anyone can use, study, modify, and distribute it for free. Any modified version — including when served via web or API — must have its source code published under the same license. No one may commercialize closed versions. User-generated data belongs to the community, never to private companies.

See [LICENSE](./LICENSE) for the full text.

---

## References & Data Sources

[^1]: IBGE. *Censo Agropecuário 2017*. Rio de Janeiro: IBGE, 2017. Available: https://censoagro2017.ibge.gov.br/

[^2]: MDA - Ministério do Desenvolvimento Agrário. *Portal da Agricultura Familiar*. Brasília, 2023. Available: https://www.gov.br/pt-br/assuntos/agricultura-familiar

[^3]: MAPA - Ministério da Agricultura, Pecuária e Abastecimento. *Plano ATER Brasil 2023-2030*. Brasília: MAPA, 2023. Available: https://www.gov.br/agricultura/pt-br/assuntos/ater

[^4]: AMD. *AMD AI Developer Program*. Available: https://www.amd.com/en/developer/ai-dev-program.html

[^5]: AMD Developer Cloud. Available: https://developer.amd.com/cloud/

- EMBRAPA. *Sistemas Agroflorestais: conceitos e aplicações*. Brasília: EMBRAPA, 2020.
- MDA/CONAB. *Plano Safra 2024/2025*. Available: https://www.gov.br/agricultura/pt-br/assuntos/planejamento-safra
- Lei 10.831/2003 - Lei da Agricultura Orgânica
- Lei 11.947/2009 - PNAE (30% minimum from family farming)
- MAPA/IN 46/2011 - Regulamento da Produção Orgânica

---

## Contact & Community

- GitHub Discussions: Technical questions and suggestions
- Issues: Bugs and feature requests
- Repository: https://github.com/catitodev/agrofamiliapp

> **Made with ❤️ for Brazilian family farmers**