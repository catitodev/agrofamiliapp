import os
from typing import Dict
import asyncio

SYSTEM_PROMPT_ATER = """Você é um especialista em ATER (Assistência Técnica e Extensão Rural) do AgroFamíliApp. Você fornece orientação técnica agroecológica para agricultores familiares brasileiros, cobrindo quatro vertentes:

1. **Agricultura Sintrópica** (Ernst Götsch): sucessão natural, SAFs, estratificação, podas
2. **Agricultura Biodinâmica** (Rudolf Steiner): preparados BD 500-508, calendário lunar, ritmos cósmicos
3. **Agricultura Orgânica** (Lei 10.831/2003): insumos permitidos, certificação MAPA, período de transição
4. **Agricultura Natural** (Masanobu Fukuoka): sem insumos externos, seleção natural de sementes

Sempre responda em português do Brasil. Seja prático e direto. Recomende consultar a EMATER local quando apropriado."""


class ATERAgent:
    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT_ATER

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        await asyncio.sleep(0.05)

        text_lower = user_input.lower()

        if any(kw in text_lower for kw in ["sintrop", "saf", "sucessão", "estratif", "podas", "götsch"]):
            response = """🌱 **Agricultura Sintrópica**

A Agricultura Sintrópica, desenvolvida por **Ernst Götsch**, baseia-se na sucessão natural de vegetação:

**Princípios Fundamentais:**
1. **Sucessão Natural**: 3 fases - Pioneira → Secundária → Climática
2. **Estratificação**: até 7 camadas de vegetação (do solo ao emergente)
3. **Podas**: carbono para o solo, ritmo quinzenal a mensal

**Exemplo de SAF com Cacau (Sul da Bahia):**
- Camada 1 (solo): herbáceas e cobertura
- Camada 2 (arbustiva): bananeira, heliconia
- Camada 3 (média): cacau, açaí
- Camada 4 (alta): castanha, andiroba
- Emergentes: mogno, ipê

**Como começar:**
1. Observe a sucessão natural local
2. Plante espécies pioneiras (leguminosas)
3. Insira espécies de interesse econômico
4. Faça podas regulares para alimentar o solo

📚 Referência: EMBRAPA - Sistemas Agroflorestais para a Agricultura Familiar"""
        elif any(kw in text_lower for kw in ["biodin", "lunar", "preparado", "500", "501", "steiner", "calendário"]):
            response = """🌙 **Agricultura Biodinâmica**

Baseada nas palestras de **Rudolf Steiner (1924)**, a agricultura biodinâmica vê a propriedade como um organismo completo.

**Preparados Biodinâmicos Essenciais:**
- **BD 500**: Stercus de vaca em chifre enterrado (50g/100L) → ativação do solo
- **BD 501**: Sílica cristalina em chifre (2,5g/100L) → desenvolvimento foliar
- Dinamização: 1 hora em água, aplicar conformelua

**Calendário Biodinâmico:**
- 🌱 **Dias de Raiz** (terras): favorece raízes e tubérculos
- 🍃 **Dias de Folha** (águas): favorece folhas e hortaliças
- 🍊 **Dias de Fruto** (arnes): favorece frutos e grãos
- 🌸 **Dias de Flor** (ares): favorece flores e reprodução

**Ritmo Lunar:**
- 🌒 Lua crescente: favorece desenvolvimento aéreo
- 🌘 Lua minguante: favorece raízes, poda, colheita de raízes

📚 Referência: SECAAF - Sociedade para Desenvolvimento da Agricultura Biodinâmica"""
        elif any(kw in text_lower for kw in ["orgânic", "certific", "ibd", "transição", "insumo"]):
            response = """🌿 **Agricultura Orgânica**

Regida pela **Lei 10.831/2003**, a agricultura orgânica no Brasil requer:

**Insumos Permitidos:**
- Adubos orgânicos (composto, vermicomposto, bokashi)
- Biofertilizantes, manipueira, cinza, calcário, fosfato natural
- Calda bordalesa, calda sulfocálcica
- Baculovirus, Beauveria, Metarhizium (controle biológico)
- Trichograma, Bacillus thuringiensis

**Insumos PROIBIDOS:**
- Fertilizantes sintéticos
- Agrotóxicos químicos
- Hormônios de crescimento
- Antibióticos profiláticos
- OGM (organismos geneticamente modificados)

**Caminhos de Certificação:**
1. **OCS (Organismo de Controle Social)**: para venda direta, até 20 produtores, sem custo
2. **Certificação por Terceira Parte**: IBD, Ecocert, IMO (para mercados formais)

**Prazo de Transição:**
- Mínimo 12 meses (culturas anuais)
- 18 meses (semi-perenes)
- 36 meses (perenes)

📚 Referência: MAPA - Regulamento da Produção Orgânica (IN 46/2011)"""
        elif any(kw in text_lower for kw in ["natural", "fukuoka", "sem insumo", "no-till"]):
            response = """🌾 **Agricultura Natural**

Baseada nos princípios de **Masanobu Fukuoka** (1913-2008):

**4 Princípios Fundamentais:**
1. **Não revolver o solo** - cultivar sem aração ou gradagem
2. **Não usar adubos químicos** - a biomassa natural alimenta o solo
3. **Não capinar** - cobertura do solo impede plantas daninhas
4. **Não usar pesticidas** - a natureza encontra equilíbrio

**Técnicas Principais:**
- **Sementes de bola**: sementes cobertas com argila e sementes
- **Cobertura do solo**: biomassa morta como "mulching"
- **Diversificação**: polyculture, consórcios
- **Sucessão natural**: trabalhar com, não contra a natureza

**Aplicação Prática:**
- Inicie com adubos verdes (aveia, tremoço, mucuna)
- Não mate ervas - deixe-as participar do sistema
- Observe por 1-2 anos antes de intervir

📚 Referência: Fukuoka - "A Revolução da Palha" (The One-Straw Revolution)"""
        else:
            response = """🌱 **Agente ATER - AgroFamíliApp**

Posso ajudar com orientação técnica agroecológica:

**Especialidades:**
- 🌿 Agricultura Sintrópica (SAFs, sucessão natural)
- 🌙 Agricultura Biodinâmica (calendário lunar, preparados)
- 🍃 Agricultura Orgânica (certificação, insumos)
- 🌾 Agricultura Natural (sem insumos externos)

**Como posso ajudar?**
Tente perguntas como:
- "Como fazer um SAF com cacau?"
- "Quando podar no calendário biodinâmico?"
- "Como obter certificação orgânica?"
- "Como plantar sem usar adubo químico?"

💡 **Dica**: Para orientação personalizada, consulte a EMATER do seu município."""

        return {
            "text": response,
            "confidence": 0.92,
            "context": {"agent": "ater", "mode": "knowledge_base"},
            "suggested_actions": [
                "Consulte EMATER local para acompanhamento técnico",
                "Verifique calendário de plantio da sua região"
            ]
        }