import os
from typing import Dict
import asyncio


class DocsAgent:
    def __init__(self):
        pass

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        await asyncio.sleep(0.05)
        text_lower = user_input.lower()

        if any(kw in text_lower for kw in ["carteira", "produtor rural", "nota fiscal"]):
            response = """📄 **Carteira de Produtor Rural**

A Carteira de Produtor Rural é essencial para comercialização e emissão de notas fiscais.

**Documentos necessários:**
- Documento de identidade (RG)
- CPF
- Comprovante de residência
- Documento que comprove posse da terra (matrícula, contrato de arrendamento, etc.)
- Para renovação: Nota Fiscal de Produtor Rural dos últimos períodos

**Onde solicitar:**
- Secretaria da Fazenda do seu estado
- Prefeitura Municipal (setor de agricultura/tributação)

**Validade:** 1 a 3 anos (varia por estado)

**Vantagens:**
- Emissão de Nota Fiscal de Produtor Rural
- Isenção de ICMS em muitos estados
- Comprovação da condição de produtor rural
- Acesso a programas de comercialização

📚 Referência: Secretarias da Fazenda estaduais"""
        elif any(kw in text_lower for kw in ["cnpj", "mei rural", "empresa"]):
            response = """🏢 **CNPJ Rural / MEI Rural**

Para agricultores que precisam de CNPJ (processamento, exportação, mercados formais):

**MEI Rural:**
- Receita Federal: www.gov.br/receitafederal
- Receita bruta até R$ 360.000/ano
- Custo mensal: R$ 0 (isenção de DAS)
- Emissão de notas fiscais eletrônicas
- Acesso a mercados formais

**CNPJ Normal (Rural):**
- Para operações maiores ou agroindústria
- Pode ter sócios
- Obrigações contábeis mais complexas

**Como fazer MEI Rural:**
1. Acesse www.gov.br/receitafederal
2. Vá para "CNPJ" → "Abra seu CNPJ"
3. Escolha "Microempreendedor Individual"
4. Atividade: "Agricultor familiar"
5. Apresente CAF ou DAP

📚 Referência: Receita Federal do Brasil"""
        elif any(kw in text_lower for kw in ["orgânic", "certific", "ibd", "ecocert"]):
            response = """🌿 **Certificação Orgânica**

A **Lei 10.831/2003** regulamenta a agricultura orgânica no Brasil.

**Caminhos de Certificação:**

**1. OCS - Organismo de Controle Social (para venda direta)**
- Até 20 produtores organizados
- Sem certificação de terceira parte
- Controle por lista de associados
- Para venda direta ao consumidor final
- Custo: inexistente (autogestão)
- Exemplo:feiras de produtos orgânicos sem certificação formal

**2. Certificação por Terceira Parte (para mercados formais)**
- **IBD Certificadora**: www.ibd.com.br
- **Ecocert Brasil**: www.ecocert.com.br
- **IMO**: www.imo.ch
- **Pro-Cert**: www.pro-cert.com.br

**Período de Transição:**
- Mínimo 12 meses (culturas anuais)
- 18 meses (semi-perenes)
- 36 meses (culturas perenes)

**SISORG (MAPA):**
- Sistema de rastreabilidade
- Obrigatório para exportadores
- Registro no MAPA

📚 Referência: MAPA - Agricultura Orgânica (Lei 10.831/2003, IN 46/2011)"""
        elif any(kw in text_lower for kw in ["sim", "sie", "sif", "inspeção", "carne", "leite"]):
            response = """🔍 **Inspeção Sanitária - SIM/SIE/SIF**

Para comercialização de produtos de origem animal (carne, leite, ovos, mel):

**SIM - Serviço de Inspeção Municipal**
- Venda dentro do município
- Requisitos definidos pela prefeitura
- Mais acessível para pequenos produtores

**SIE - Serviço de Inspeção Estadual**
- Venda dentro do estado
- Requisitos mais rigorosos
- Padrão de qualidade superior

**SIF - Serviço de Inspeção Federal (MAPA)**
- Venda interestadual ou exportação
- Requisitos muito rigorosos
- Para agroindústrias de maior porte

**Como começar:**
1. Identifique seu mercado-alvo (municipal/estadual/federal)
2. Projete a unidade conforme legislação
3. Solicite registro junto ao órgão competente
4. Obtendo licenciamento sanitário
5. Manter regularidade de operations

📚 Referência: MAPA - Inspeção de Produtos de Origem Animal"""
        else:
            response = """📋 **Agente de Documentação - AgroFamíliApp**

Posso ajudar com documentos e regularização:

**Documentos principais:**
- Carteira de Produtor Rural (Nota Fiscal)
- CAF - Cadastro Nacional da Agricultura Familiar
- CNPJ Rural / MEI Rural
- Certificação Orgânica (IBD, Ecocert, OCS)
- SIM/SIE/SIF (inspeção sanitária)

**Tente perguntas como:**
- "Como fazer a Carteira de Produtor Rural?"
- "Como tirar o MEI Rural?"
- "Como certify my organic product?"
- "Preciso de inspeção sanitária para vender queijo?"

**Dicas:**
1. Mantenha documentos sempre organizados
2. Não deixe prazos de renovação vencerem
3. Procure orientação na EMATER
4. Comece com OCS se vender direto (sem custo)

💡 **Importante**: Sem documentação em dia, você pode perder acesso a políticas públicas e mercados!

📚 Referência: MAPA e Receita Federal"""

        return {
            "text": response,
            "confidence": 0.87,
            "context": {"agent": "docs", "mode": "knowledge_base"},
            "suggested_actions": [
                "Procure EMATER para orientação sobre CAF",
                "Verifique documentos necessários com antecedência"
            ]
        }