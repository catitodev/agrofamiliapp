import os
from typing import Dict
import asyncio


class ClimaAgent:
    def __init__(self):
        pass

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        await asyncio.sleep(0.05)
        text_lower = user_input.lower()

        if any(kw in text_lower for kw in ["chuva", "previsao", "tempo", "semana"]):
            response = """☁️ **Previsão do Tempo e Clima**

**Fontes Oficiais:**

**INMET (Instituto Nacional de Meteorologia):**
- www.inmet.gov.br
- Previsão de 5 dias por município
- Estações meteorológicas em todo Brasil
- Alertas de tempo severo

**CPTEC/INPE:**
- www.cptec.inpe.br
- Previsão extends to 14 days
- Mapas de chuva, temperatura, umidade

**Como usar:**
1. Acesse www.inmet.gov.br
2. Busque por município
3. Consulte previsão de 5 dias
4. Confira alertas

**Dica**: Para planejamento agrícola, combine previsão de curto prazo com históricos de chuva."""
        elif any(kw in text_lower for kw in ["plantar", "calendário", "safra", "época"]):
            response = """🌾 **Calendário de Plantio**

**Culturas Principais por Região:**

**Centro-Sul (inclui SP, MG, PR, RS, SC):**
| Cultura | Época de Plantio |
|---------|-----------------|
| Milho | Agosto a Dezembro |
| Soja | Outubro a Dezembro |
| Feijão 1ª safra | Agosto a Novembro |
| Arroz | Setembro a Dezembro |
| Trigo | Abril a Agosto |

**Norte/Nordeste:**
| Cultura | Época de Plantio |
|---------|-----------------|
| Milho | Novembro a Janeiro |
| Feijão | Março a Maio |
| Arroz | Outubro a Janeiro |
| Mandioca | Ano todo |

**Fator crítico:** Plante na época certa! Errar o plantio pode significar perda total da safra.

**Influências:**
- Época de chuvas
- Temperatura do solo
- Fotoperíodo
- Risco de geada (Sul)

💡 **Dica**: Consulte a EMATER para calendário específico da sua microrregião.

📚 Referência: EMBRAPA - Calendário de Plantio por Região"""
        elif any(kw in text_lower for kw in ["geada", "seca", "estiagem", "alerta"]):
            response = """⚠️ **Alertas Climáticos**

**Seca/Estiagem:**
- Prevalente no Semiárido nordestino
- Acompanhe: ANA, INMET, Defesa Civil
- Programas: Garantia-Safra
- Mitigação: cisternas, barragens, SAFs

**Geada:**
- Risco: Sul, Sudeste, Cerrado em altitude
- Períodos críticos: inverno (junho-agosto)
- Culturas sensíveis: café, hortaliças, milho jovem
- Mitigação: cobertura do solo, quebra-vento, انتخاب de variedades

**Excesso de Chuva:**
- Problemas: erosão, doenças fúngicas, colheita impossibilitada
- Mitigação: drenagem, curva de nível, terraceamento

**Alertas Oficiais:**
- INMET: www.inmet.gov.br (alertas)
- Defesa Civil do seu estado
- EMATER local

📚 Referência: INMET e Defesa Civil Nacional"""
        else:
            response = """☁️ **Agente de Clima - AgroFamíliApp**

Posso ajudar com informações climáticas e planejamento de safra:

**Tente perguntas como:**
- "Vai chover essa semana em Petrolina?"
- "Quando planto milho no Sertão?"
- "Como me proteger de geada?"
- "Qual a previsão do tempo para minha região?"

**Fontes que uso:**
- INMET (Instituto Nacional de Meteorologia)
- CPTEC/INPE (previsão estendida)
- EMBRAPA (calendários de plantio)

**Dicas:**
1. Acompanhe previsão semanal
2. Planeje plantio según calendário regional
3. Monitore alertas de eventos extremos
4. Adapte práticas ao clima local

💡 **Importante**: Sempre verifique previsão oficial no INMET antes de decisões críticas.

📚 Referência: INMET e EMBRAPA"""

        return {
            "text": response,
            "confidence": 0.85,
            "context": {"agent": "clima", "mode": "knowledge_base"},
            "suggested_actions": [
                "Consulte INMET para previsão oficial detalhada",
                "Acompanhe alertas da Defesa Civil do seu estado"
            ]
        }