# AgroFamíliApp

**Assistente agroecológico por voz e texto para agricultores familiares brasileiros.**

Agente de IA conversacional gratuito, open-source e multilíngue (português com sotaques regionais), acessível via WhatsApp, Telegram e WebApp. Quanto mais agricultores usam, melhor o sistema fica — o aprendizado é coletivo e os dados pertencem à comunidade.

[![Licença: AGPL v3](https://img.shields.io/badge/Licen%C3%A7a-AGPL%20v3-green.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Public Good](https://img.shields.io/badge/tipo-bem%20p%C3%BAblico-brightgreen)](https://github.com/catitodev/agrofamiliapp)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento%20ativo-blue)](https://github.com/catitodev/agrofamiliapp)

---

## O problema

Mais de 3,9 milhões de estabelecimentos de agricultura familiar no Brasil respondem por 70% dos alimentos que chegam à mesa dos brasileiros. Mas o agricultor familiar não tem acesso a consultoria técnica agroecológica de qualidade — a ATER (Assistência Técnica e Extensão Rural) pública é insuficiente, descontinuada e geograficamente concentrada. O resultado: decisões de plantio baseadas em tradição oral, sem acesso a dados de clima, preço, crédito ou certificação.

## A solução

O AgroFamíliApp é um agente de IA conversacional especializado em agroecologia — gratuito, por voz ou texto, via WhatsApp, Telegram ou navegador. O agricultor pergunta em linguagem natural ("quando planto meu milho aqui no Sertão?"), o agente responde com base em dados reais de clima, preço, crédito e conhecimento técnico agroecológico.

O diferencial central: o sistema aprende com cada conversa. Perguntas reais de agricultores reais alimentam um ciclo de melhoria contínua — sem expor dados individuais, sem custos para ninguém.

---

## Funcionalidades

### Agente ATER (Assistência Técnica e Extensão Rural)
Orientação técnica baseada nas quatro vertentes da agroecologia:
- Agricultura Sintrópica (sucessão natural, Sistemas Agroflorestais)
- Agricultura Biodinâmica (ritmos lunares, preparados biodinâmicos)
- Agricultura Orgânica (certificação, insumos permitidos, transição)
- Agricultura Natural (sem insumos externos, manejo ecológico)

### Agente de crédito e políticas públicas
- Pronaf (todas as linhas: Custeio, Investimento, Agroindústria, Mulher, Jovem, Eco, Floresta, Semiárido)
- CAF — Cadastro Nacional da Agricultura Familiar (substituto do DAP desde 2023)
- PNCF — Programa Nacional de Crédito Fundiário
- Garantia-Safra
- Seguro da Agricultura Familiar (SEAF)

### Agente de mercado e comercialização
- PAA — Programa de Aquisição de Alimentos
- PNAE — Programa Nacional de Alimentação Escolar (30% obrigatório da AF)
- Preços em tempo real: CONAB, CEPEA
- Feiras, cooperativas e grupos de comercialização por região

### Agente de clima e planejamento de safra
- Previsão climática integrada ao INMET por município
- Calendário de plantio regional
- Alertas de seca, geada e eventos extremos

### Agente de documentação e regularização
- CAF (Cadastro da Agricultura Familiar) — como obter e renovar
- CNPJ MEI Rural
- Certificação orgânica (IBD, Ecocert, OCS — Organismo de Controle Social)
- SISORG — Sistema de Rastreabilidade Orgânica

### Agente de território e serviços
- Mapa de serviços por município: ATER, cooperativas, feiras, bancos, saúde rural
- Emater, Embrapa, escritórios Pronaf
- Territórios da Cidadania

### Aprendizado contínuo (flywheel comunitário)
Cada conversa gera dados anonimizados que alimentam o ciclo de fine-tuning periódico do modelo. Mais usuários = modelo mais específico para a realidade do campo brasileiro. Os dados pertencem à comunidade, nunca a empresas.

---

## Tecnologia

| Componente | Tecnologia |
|---|---|
| Inferência LLM | vLLM + Llama 3.1 70B / Qwen2.5 rodando no AMD Instinct MI300X |
| Orquestração de agentes | LangChain + CrewAI |
| Transcrição de voz | Whisper (open-source, rodando localmente) |
| Base de conhecimento | RAG com ChromaDB + embeddings multilíngues |
| Backend | FastAPI (Python 3.11+) |
| WebApp | React + Vite (PWA instalável) |
| Canal WhatsApp | Twilio ou Z-API (webhook) |
| Canal Telegram | python-telegram-bot |
| Dados externos | APIs públicas: INMET, CEPEA, CONAB, SNCR, IBGE |
| Painel gestor | Streamlit |
| Infraestrutura | AMD Developer Cloud (GPU MI300X, 192GB VRAM) |
| Licença | GNU Affero General Public License v3 (AGPL-3.0) |

---

## Arquitetura modular

agrofamiliapp/
├── LICENSE
├── README.md
├── docker-compose.yml
├── requirements.txt
│
├── core/
│   ├── gateway.py        # roteamento, autenticação, Whisper STR
│   ├── memory.py         # contexto de conversa por usuário (Redis)
│   └── feedback.py       # coleta anônima para RLHF-light
│
├── agents/
│   ├── ater.py           # assistência técnica agroecológica
│   ├── credito.py        # Pronaf, CAF, crédito rural
│   ├── mercado.py        # PAA, PNAE, preços, comercialização
│   ├── clima.py          # INMET, previsão, calendário de plantio
│   ├── docs.py           # documentação, regularização, certificação
│   └── territorio.py     # mapa de serviços por município
│
├── knowledge/
│   ├── sintropia/        # conteúdo técnico: SAFs, sucessão
│   ├── biodinamica/      # preparados, calendário biodinâmico
│   ├── organica/         # certificação, normas, transição
│   ├── natural/          # manejo ecológico sem insumos externos
│   └── politicas/        # CAF, Pronaf, PAA, PNAE, legislação atualizada
│
├── channels/
│   ├── whatsapp.py       # webhook Twilio/Z-API
│   ├── telegram.py       # bot Telegram
│   └── webapp/           # React PWA
│
├── data/
│   ├── inmet.py          # clima e previsão
│   ├── cepea.py          # preços agropecuários
│   ├── conab.py          # preços e abastecimento
│   └── mapa_sda.py       # MAPA, SISORG, registros
│
└── dashboard/
└── app.py            # painel Streamlit para gestores públicos

---

## Como usar localmente

```bash
# clone o repositório
git clone https://github.com/catitodev/agrofamiliapp.git
cd agrofamiliapp

# instale as dependências
pip install -r requirements.txt

# configure as variáveis de ambiente
cp .env.example .env
# edite o .env com suas chaves

# inicie os serviços
docker-compose up -d

# inicie o backend
uvicorn core.gateway:app --reload

# inicie o WebApp (em outro terminal)
cd channels/webapp
npm install && npm run dev
```

---

## Variáveis de ambiente necessárias

AMD_API_ENDPOINT=         # endpoint vLLM no AMD Developer Cloud
INMET_API_KEY=            # API pública do INMET (gratuita)
TELEGRAM_BOT_TOKEN=       # token do bot no BotFather
TWILIO_ACCOUNT_SID=       # para canal WhatsApp
TWILIO_AUTH_TOKEN=
REDIS_URL=redis://localhost:6379
CHROMA_PERSIST_DIR=./knowledge/vectorstore

---

## Contribuindo

Este projeto é um bem público. Contribuições são muito bem-vindas.

**Como contribuir:**
1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nome-da-contribuicao`
3. Faça suas alterações com testes
4. Abra um Pull Request com descrição clara do que muda e por quê

**Áreas prioritárias para contribuição:**
- Conteúdo técnico agroecológico em `knowledge/` (especialmente saberes regionais)
- Integração com novos canais (SMS, USSD para áreas sem internet)
- Tradução para línguas indígenas e regionais
- Dados e APIs de novas regiões
- Testes e validação agronômica do conteúdo

**Código de Conduta:** Este projeto segue o [Código de Conduta da Contributor Covenant](https://www.contributor-covenant.org/pt-br/version/2/1/code_of_conduct/).

---

## Alinhamento com ODS da ONU

- ODS 1: Erradicação da pobreza — geração de renda para agricultores familiares
- ODS 2: Fome zero — fortalecimento da produção de alimentos saudáveis
- ODS 8: Trabalho decente — melhoria da renda no campo
- ODS 10: Redução das desigualdades — acesso democrático à informação técnica
- ODS 12: Consumo responsável — agroecologia e produção sustentável
- ODS 13: Ação climática — adaptação e mitigação via manejo agroecológico
- ODS 15: Vida terrestre — SAFs, regeneração, biodiversidade

---

## Licença

**GNU Affero General Public License v3.0 (AGPL-3.0)**

Este software é e sempre será um bem público. Qualquer pessoa pode usar, estudar, modificar e distribuir gratuitamente. Qualquer versão modificada — inclusive quando disponibilizada via web ou API — deve ter seu código-fonte publicado sob a mesma licença. Ninguém pode comercializar versões fechadas deste software. Os dados gerados pelos usuários pertencem à comunidade, nunca a empresas privadas.

Ver arquivo [LICENSE](./LICENSE) para o texto completo.

---

## Histórico

O AgroFamíliApp nasceu como proposta de portal HTML estático para agricultores familiares e agroecológicos. Em maio de 2025, foi relançado como agente de IA conversacional open-source, com foco em agroecologia e aprendizado coletivo, no contexto do AMD Developer Hackathon (lablab.ai).

---

## Contato e comunidade

- GitHub Discussions: para dúvidas técnicas e sugestões
- Issues: para bugs e solicitações de funcionalidade
- Repositório: https://github.com/catitodev/agrofamiliapp


