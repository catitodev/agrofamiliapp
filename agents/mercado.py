import os
from typing import Dict
import asyncio


class MercadoAgent:
    def __init__(self):
        pass

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        await asyncio.sleep(0.05)
        text_lower = user_input.lower()

        if any(kw in text_lower for kw in ["paa", "aquisição", "doação"]):
            response = """📦 **PAA - Programa de Aquisição de Alimentos**

O PAA compra alimentos diretamente de agricultores familiares para donation a pessoas em insegurança alimentar.

**Modalidades:**
1. **Compra com Doação Simultânea**: alimentos adquiridos e doados para entidades sociais
2. **Compra Direta**: aquisição de produtos específicos para sustentar preços
3. **Formação de Estoques**: apoio à constituição de estoques por organizações
4. **Compra Institucional**: órgãos públicos compram para suas refeições
5. **PAA Leite**: aquisição de leite de agricultores familiares

**Limites (2023):**
- R$ 15.000/família/ano (exceto organizações)
- R$ 8.000/membro/ano para OAF (Organização da Agricultura Familiar)

**Como participar:**
1. Tenha CAF ativa
2. Organize-se em associação ou cooperativa
3. Contact CONAB or state organizations
4. Cadastre-se nos editais

📚 Referência: CONAB - Programa de Aquisição de Alimentos"""
        elif any(kw in text_lower for kw in ["pnae", "escola", "merenda", "alimentação escolar"]):
            response = """🏫 **PNAE - Programa Nacional de Alimentação Escolar**

O PNAE determina que **no mínimo 30%** dos recursos do FNDE sejam usados para comprar alimentos da agricultura familiar.

**Características:**
- Venda direta para escolas públicas
- Prioridade para produtos locais e da safra
- Prioridade para alimentos orgânicos/agroecológicos
- Valorização da produção regional

**Limites:**
- R$ 20.000/familiar/ano por ano letivo
- Máximo por fornecedor por chamada pública: R$ 40.000

**Como participar:**
1. Acompanhe chamadas públicas da prefeitura
2. Organize documentação (CAF, projeto de venda)
3. Apresent proposta na chamada pública
4. Entregue produtos conforme cronograma escolar

**Documentos necessários:**
- CAF ativa
- Projeto de venda
- Declaração de produção própria
- Documentação sanitária conforme produto

📚 Referência: FNDE - Programa Nacional de Alimentação Escolar (Lei 11.947/2009)"""
        elif any(kw in text_lower for kw in ["feira", "direta", "vender", "consumidor"]):
            response = """🏪 **Vendas Diretas e Feiras**

**Tipos de Comercialização:**

**Feiras da Agricultura Familiar:**
- Organizadas por prefeituras ou associações
- Espaço garantido para agricultores familiares
- Taxa de occupation usually low

**Feiras Agroecológicas:**
- Comercialização de produtos orgânicos certificados
- Preços mais altos, cliente comprometido
- Mercado em crescimento

**Venda na Propriedade:**
- Comercialização direta ao consumidor
- Reduz intermediários = maior renda
- Requer autorização da vigilância sanitária

**Redes e Circuitos Curtos:**
- **CSA** (Comunidades que Sustentam a Agricultura): consumidores pagam antecipado
- Grupos de consumo responsável
- WhatsApp e Instagram para divulgação

**Dicas para vender melhor:**
1. Invista na apresentação dos produtos
2. Desenvolva relação de confiança com clientes
3. Estabeleça preços justos e competitivos
4. Use redes sociais para divulgação
5. Mantenha regularidade no fornecimento

📚 Referência: MDA - Comercialização da Agricultura Familiar"""
        elif any(kw in text_lower for kw in ["preço", "cotação", "cepea", "conab"]):
            response = """📈 **Preços e Comercialização**

**Onde acompanhar preços:**

**CEPEA/ESALQ (USP):**
- www.cepea.esalq.usp.br
- Cesta de produtos da agricultura familiar
- Commodities: milho, soja, café, arroz, bois, leite
- Reference prices updated daily

**CONAB:**
- www.conab.gov.br
- Preços mínimos do governo
- Cotações regionais por município
- Calendário de mercados

**Dicas de Comercialização:**
- Não venda no auge da colheita (preços baixos)
- Observe tendências de mercado
- Consorcie venda direta com mercados institucionais
- Agregue valor (processamento mínimo)
- Organize-se em cooperativas

📚 Referência: CEPEA/ESALQ e CONAB"""
        else:
            response = """📦 **Agente de Mercado - AgroFamíliApp**

Posso ajudar com comercialização e acesso a mercados:

**Programas Governamentais:**
- **PAA**: Compra de alimentos para doação (até R$ 15.000/família)
- **PNAE**: Venda para escolas (30% mínimo da merenda)

**Vendas Diretas:**
- Feiras da Agricultura Familiar
- Feiras Agroecológicas
- Venda na propriedade
- CSA e grupos de consumo

**Tente perguntas como:**
- "Como vender para a merenda escolar?"
- "Como participar do PAA?"
- "Onde vender minha produção?"
- "Qual o preço do milho hoje?"

💡 **Dica**: Organize-se em associações ou cooperativas para ganhar escala!

📚 Referência: CONAB e MDA"""

        return {
            "text": response,
            "confidence": 0.88,
            "context": {"agent": "mercado", "mode": "knowledge_base"},
            "suggested_actions": [
                "Acompanhe chamadas públicas da prefeitura para PNAE",
                "Consulte CONAB para preços de referência do PAA"
            ]
        }