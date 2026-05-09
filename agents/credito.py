import os
from typing import Dict
import asyncio


class CreditoAgent:
    def __init__(self):
        pass

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        await asyncio.sleep(0.05)
        text_lower = user_input.lower()

        if any(kw in text_lower for kw in ["pronaf", "custeio", "investimento", "mais alimento"]):
            response = """💰 **PRONAF - Programa Nacional de Fortalecimento da Agricultura Familiar**

O PRONAF é o principal programa de crédito para agricultores familiares do Brasil.

**Linhas de Crédito (Plano Safra 2024/2025):**

| Linha | Limite | Juros | Finalidade |
|-------|--------|-------|------------|
| **Custeio** | R$ 400.000 | 3% | Despesas do ciclo produtivo |
| **Investimento** | R$ 400.000 | 3% | Máquinas, equipamentos, infraestrutura |
| **Agroecologia** | R$ 100.000 | 2% | Sistemas orgânicos/agroecológicos |
| **Mais Alimentos** | R$ 200.000 | 4% | Infraestrutura produtiva |
| **Agroindústria** | R$ 200.000 | 3% | Processamento e comercialização |
| **Floresta** | R$ 50.000 | 2% | Sistemas agroflorestais |
| **Mulher** | R$ 100.000 | 2% | Mulheres agricultoras |
| **Jovem** | R$ 40.000 | 3% | Jovens agricultores |

**Requisitos Básicos:**
- ✅ CAF ou DAP ativa
- ✅ Renda bruta familiar até R$ 500.000/ano
- ✅ Mínimo 75% da renda de atividade agropecuária
- ✅ Aptidão para atividade rural

**Como Solicitar:**
1. Obtenha/atualize seu CAF (EMATER, sindicato)
2. Elabore projeto técnico com assistance
3. Procure Banco do Brasil, Banco do Nordeste ou cooperativas de crédito
4. Acompanhe prazos do Plano Safra

📚 Referência: MDA - Plano Safra 2024/2025"""
        elif any(kw in text_lower for kw in ["caf", "cadastro", "dap"]):
            response = """📋 **CAF - Cadastro Nacional da Agricultura Familiar**

O CAF substituiu a DAP desde 2023 e é obrigatório para acessar políticas públicas.

**O que é o CAF?**
- Cadastro que identifica a Unidade Familiar de Produção Agrária (UFPA)
- Substitui a DAP (Declaração de Aptidão ao Pronaf)
- Válido por **2 anos**

**Requisitos para obter o CAF:**
- Área: até 4 módulos fiscais do município
- Renda: até R$ 500.000/ano de renda bruta familiar
- Mínimo 75% da renda de atividade agropecuária

**Documentos necessários:**
- Documentos de identidade (RG) e CPF de todos os membros familiares
- Comprovante de estado civil
- Documentação do imóvel rural (matrícula, contrato, etc.)
- Comprovantes de renda bruta familiar (12 meses)

**Onde solicitar:**
- EMATER do seu estado (EMATER-MG, EMATER-RS, etc.)
- Sindicatos de Trabalhadores Rurais credenciados
- Entidades públicas autorizadas

📚 Referência: MDA - Cadastro Nacional da Agricultura Familiar"""
        elif any(kw in text_lower for kw in ["garantia", "safra", "seguro", "seaf"]):
            response = """🛡️ **Garantia-Safra e SEAF**

**Garantia-Safra**
- Para agricultores de municípios do **Semiárido**
- Proteção contra seca ou excesso de chuva
- Valor: R$ 850 por família (2023/2024)
- Requer inscrição no CAF

**SEAF - Seguro da Agricultura Familiar**
- Vinculado ao PRONAF Custeio
- Prêmio: 3% do valor financiado
- Cobertura: 70% da perda comprovada
- Eventos cobertos: seca, geada, granizo, excesso de chuva, doenças

**Como acessar:**
1. Contrate PRONAF Custeio com coverage de SEAF
2. Pague o prêmio (3% do valor)
3. Em caso de perda, solicite vistoria
4. Receive indenização se aceita

📚 Referência: MDA - Garantia-Safra / Mapa - SEAF"""
        elif any(kw in text_lower for kw in ["pnc", "fundiário", "terra", "aquisição"]):
            response = """🏡 **PNCF - Programa Nacional de Crédito Fundiário**

Para agricultores sem terra ou com pouca terra:

**Características:**
- Financing for land acquisition
- Complementary financing for infrastructure
- Requires no prior land ownership

**Requirements:**
- Family income up to R$ 30.000/year
- No land or less than 1 module fiscal
- Must be organized in groups or cooperatives

**How to access:**
1. Contact INCRA or state land institute
2. Participate in capacity formation
3. Present land purchase proposal
4. Get credit approval

📚 Referência: INCRA - Programa Nacional de Crédito Fundiário"""
        else:
            response = """💰 **Agente de Crédito Rural - AgroFamíliApp**

Posso ajudar com informações sobre crédito rural e políticas públicas:

**Tente perguntas como:**
- "Como conseguir R$ 50 mil do PRONAF?"
- "Como fazer o CAF?"
- "O que é o Garantia-Safra?"
- "Como funciona o SEAF?"
- "Posso financiar terra pelo PNCF?"

**Principais programas:**
- PRONAF (custeio, investimento, agroecologia)
- CAF (cadastro obrigatório)
- Garantia-Safra (proteção contra seca)
- SEAF (seguro da agricultura familiar)
- PNCF (crédito fundiário)

**Dica**: Sempre tenha seu CAF atualizado em primeiro lugar!

📚 Referência: MDA - Ministério do Desenvolvimento Agrário"""

        return {
            "text": response,
            "confidence": 0.90,
            "context": {"agent": "credito", "mode": "knowledge_base"},
            "suggested_actions": [
                "Procure Banco do Brasil ou Banrisul para PRONAF",
                "Verifique disponibilidade do CAF no sindicato local"
            ]
        }