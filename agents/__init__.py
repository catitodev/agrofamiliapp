import os
from typing import Dict
import asyncio


FALLBACK_RESPONSES = {
    "ater": """🌱 **Agente ATER - Assistência Técnica Agroecológica**

O AgroFamíliApp pode ajudar com:

**Agricultura Sintrópica**
- Sistemas Agroflorestais (SAFs) com sucessão natural
- Podas e manejo de biomassa
- Estratificação de 7 camadas

**Agricultura Biodinâmica**
- Preparados BD 500 e 501
- Calendário lunar para plantio/colheita
- Ritmos cósmicos na produção

**Agricultura Orgânica**
- Certificação (Lei 10.831/2003)
- Insumos permitidos e proibidos
- Período de transição

**Agricultura Natural**
- Princípios de Fukuoka
- Sem insumos externos
- Seleção natural de sementes

💡 **Dica**: Procure a EMATER do seu município para acompanhamento técnico presencial.""",

    "credito": """💰 **Agente de Crédito Rural**

Principais programas disponíveis:

**PRONAF (Plano Safra 2024/2025)**
- Custeio: até R$ 400.000 | Juros: 3%
- Investimento: até R$ 400.000 | Juros: 3%
- Agroecologia: até R$ 100.000 | Juros: 2%
- Mais Alimentos: até R$ 200.000 | Juros: 4%
- Mulher: até R$ 100.000 | Juros: 2%
- Jovem: até R$ 40.000 | Juros: 3%

**CAF - Cadastro Nacional da Agricultura Familiar**
- Substitui a DAP desde 2023
- Válido por 2 anos
- Emissão: EMATER, sindicatos, entidades autorizadas

**Garantia-Safra**
- Para municípios do Semiárido
- R$ 850 por família em caso de perda

📋 **Como acessar**: Procure Banco do Brasil, Banco do Nordeste ou cooperativas de crédito com seu CAF em mãos.""",

    "mercado": """📦 **Agente de Mercado e Comercialização**

**PAA - Programa de Aquisição de Alimentos**
- Compra direta de alimentos da agricultura familiar
- Limite: R$ 15.000/família/ano
- Doação para programas sociais
- Via CONAB ou organizações estaduais

**PNAE - Programa Nacional de Alimentação Escolar**
- 30% mínimo para agricultura familiar (Lei 11.947/2009)
- Limite: R$ 20.000/familiar/ano por ano letivo
- Chamadas públicas das prefeituras

**Vendas Diretas**
- Feiras da Agricultura Familiar
- Feiras Agroecológicas
- Venda na propriedade
- WhatsApp e redes sociais

📈 **Preços**: Acompanhe CONAB e CEPEA para referência de preços.""",

    "clima": """☁️ **Agente de Clima e Planejamento**

**Previsão do Tempo**
- Acesse INMET: www.inmet.gov.br
- Previsão de 5 dias por município

**Calendário de Plantio (Referência)**
- Milho: Setembro a Dezembro (Centro-Sul)
- Feijão: Março-Maio ou Agosto-Setembro
- Soja: Outubro a Dezembro (Centro-Sul)
- Arroz: Setembro a Dezembro (Sul)

**Alertas**
- Seca, geada, excesso de chuva
- Acompanhe Defesa Civil do seu estado

🌾 **Dica**: O sucesso depende de plantar na época certa!""",

    "docs": """📋 **Agente de Documentação**

**Carteira de Produtor Rural**
- Emitida pela Secretaria da Fazenda do estado
- Documentos: RG, CPF, comprovante de endereço, documento da terra
- Vantagens: Nota Fiscal, isenção de ICMS

**CAF - Cadastro Nacional da Agricultura Familiar**
- Requer: documentos de todos os familiares, documento do imóvel, comprovante de renda
- Locais: EMATER, sindicatos, entidades autorizadas
- Necessário para PRONAF, PAA, PNAE

**Certificação Orgânica**
- IBD, Ecocert, OCS (venda direta sem certificação de terceira parte)
- Transição: 12 a 36 meses
- SISORG: sistema de rastreabilidade do MAPA

📄 **Dica**: Mantenha todos os documentos organizados e em dia.""",

    "territorio": """🗺️ **Agente de Território e Serviços**

**EMATER - Assistência Técnica**
- Empresa de Assistência Técnica e Extensão Rural do seu estado
- Serviços gratuitos para agricultores familiares
- EMATER-MG, EMATER-RS, EMATER-CE, etc.

**EMBRAPA**
- Pesquisa agropecuária brasileira
- Unidades regionais: Semiárido, Amazônia, etc.
- Tecnologías para agricultura familiar

**SENAR**
- Capacitação e cursos rurais
- www.senar.org.br

**Cooperativas e Associações**
- CONTAG, FETRAF, cooperativas regionais
- Fortalecem a comercialização coletiva

📍 **Dica**: Vá pessoalmente ao escritório da EMATER mais próximo para orientação completa.""",
}


class ATERAgent:
    def __init__(self):
        self._fallback = FALLBACK_RESPONSES["ater"]

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        return await self._generate_response("ater", user_input)

    async def _generate_response(self, agent_name: str, user_input: str) -> Dict:
        await asyncio.sleep(0.1)
        response_text = FALLBACK_RESPONSES.get(agent_name, self._fallback)
        return {
            "text": response_text,
            "confidence": 0.9,
            "context": {"mode": "knowledge_base", "agent": agent_name},
            "suggested_actions": [
                "Consulte EMATER local para acompanhamento",
                "Verifique calendário de plantio da sua região"
            ]
        }


class CreditoAgent:
    def __init__(self):
        self._fallback = FALLBACK_RESPONSES["credito"]

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        return await self._generate_response("credito", user_input)


class MercadoAgent:
    def __init__(self):
        self._fallback = FALLBACK_RESPONSES["mercado"]

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        return await self._generate_response("mercado", user_input)


class ClimaAgent:
    def __init__(self):
        self._fallback = FALLBACK_RESPONSES["clima"]

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        return await self._generate_response("clima", user_input)


class DocsAgent:
    def __init__(self):
        self._fallback = FALLBACK_RESPONSES["docs"]

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        return await self._generate_response("docs", user_input)


class TerritorioAgent:
    def __init__(self):
        self._fallback = FALLBACK_RESPONSES["territorio"]

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        return await self._generate_response("territorio", user_input)