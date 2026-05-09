import os
from typing import Dict
import asyncio


class TerritorioAgent:
    def __init__(self):
        pass

    async def generate(self, user_input: str, user_id: str = "") -> Dict:
        await asyncio.sleep(0.05)
        text_lower = user_input.lower()

        if any(kw in text_lower for kw in ["emater", "ater", "assistência técnica"]):
            response = """🏛️ **EMATER - Empresa de Assistência Técnica e Extensão Rural**

A EMATER é o principal serviço público de ATER do Brasil, presente em quase todos os municípios.

**O que faz a EMATER:**
- Assistência técnica gratuita para agricultores familiares
- Elaboração de projetos para PRONAF
- Emissão de CAF (Cadastro da Agricultura Familiar)
- Capacitação e capacitação técnica
- Orientação sobre políticas públicas

**EMATER por Estado:**
| Estado | EMATER |
|--------|--------|
| Minas Gerais | EMATER-MG (www.emater.mg.gov.br) |
| Rio de Janeiro | EMATER-RJ (www.emater.rj.gov.br) |
| Rio Grande do Sul | EMATER-RS (www.emater.rs.gov.br) |
| Ceará | EMATER-CE (www.emater.ce.gov.br) |
| Pernambuco | IPA (www.ipa.pm) |
| Bahia | BAHIA (www.bahiater.com.br) |
| Paraná | INSTITUTO RURAL (www.rural.pr.gov.br) |
| Mato Grosso | EMPAER-MT (www.empaer.mt.gov.br) |

**Como acessar:**
1. Vá pessoalmente ao escritório da EMATER do seu município
2. Leve seus documentos (identidade, CAF se tiver)
3. Agende reunião técnica
4. Receba orientação personalizada

💡 **Dica**: A EMATER é gratuita e existe para ajudá-lo. Use esse serviço!

📚 Referência: ANATER - Agência Nacional de Assistência Técnica e Extensão Rural"""
        elif any(kw in text_lower for kw in ["embrapa", "pesquisa", "tecnologia"]):
            response = """🔬 **EMBRAPA - Empresa Brasileira de Pesquisa Agropecuária**

A EMBRAPA é o principal órgão de pesquisa agrícola do Brasil.

**O que faz:**
- Desenvolve tecnologias para a agricultura brasileira
- Adapta práticas às diferentes regiões
- Disponibiliza cultivares melhoradas
- Capacita técnicos e agricultores

**Unidades de Referência para Agricultura Familiar:**

| Unidade | Especialidade | Região |
|---------|--------------|-------|
| Embrapa Semiárido | Caatinga, irrigação | Nordeste |
| Embrapa Amazônia Oriental | Farming system, mandioca | Amazônia |
| Embrapa华南 | Vegetables, agroecology | Brasil |
| Embrapa Alimentos e Territórios | Agroindústria, mercados | Nacional |
| Embrapa Florestas | SAFs, manejo florestal | Sul, Sudeste |

**Acesso:**
- www.embrapa.br
- Central de Atendimento: 0800-649-9000
- Unidades regionais oferecem días de campo e capacitações

📚 Referência: EMBRAPA - Empresa Brasileira de Pesquisa Agropecuária"""
        elif any(kw in text_lower for kw in ["senar", "curso", "capacitação", "formação"]):
            response = """🎓 **SENAR - Serviço Nacional de Aprendizagem Rural**

O SENAR oferece cursos gratuitos de capacitação para trabalhadores rurais.

**O que oferece:**
- Cursos técnicos de curta duração (16-40 horas)
- Programas de Formação de Jovens Rurais
- Capacitação em empreendedorismo
- Formação em cooperativismo

**Como participar:**
1. Access www.senar.org.br
2. Check available courses for your region
3. Contact the syndicate of rural workers
4. Inscreva-se nos cursos de interesse

**Programas em destaque:**
- **Formação Técnica Rural**: cursos profissionalizantes
- **Programa Jovem Agricultor**: capacitação de jovens do campo
- **Saúde e Segurança no Trabalho Rural**: prevenção de acidentes

📚 Referência: SENAR - Serviço Nacional de Aprendizagem Rural"""
        elif any(kw in text_lower for kw in ["cooperativa", "associação", "contag", "fetraf"]):
            response = """🤝 **Cooperativas e Associações**

Organizações coletivas fortalecem os agricultores familiares.

**Principais organizações:**

**CONTAG** (Confederação Nacional dos Trabalhadores na Agricultura)
- Maior organização de agricultores familiares do Brasil
- Presente em todos os estados
- www.contag.org.br

**FETRAF** (Federação dos Trabalhadores na Agricultura Familiar)
- Sindicalismo de base dos agricultores familiares
- www.fetraf.org.br

**Cooperativas por região:**
- COOPAVEL (Paraná)
- COTRIJUI (Rio Grande do Sul)
- COOPERALIANÇA (Bahia)
- etc.

**Benefícios de se organizar:**
1. **Escala**: compras coletivas, preços melhores
2. **Comercialização**: acesso a mercados maiores
3. **Processamento**: agroindústria compartilhada
4. **Political representation**: united voice for rights
5. **Capacitação**: treinamentos em grupo

**Como participar:**
1. Identifique cooperativas ou associações do seu setor
2. Visit the organization and learn about membership
3. Attend meetings and participate in decisions
4. Benefits will come with time and engagement

📚 Referência: MDA - Organização dos Agricultores Familiares"""
        else:
            response = """🗺️ **Agente de Território - AgroFamíliApp**

Posso ajudar a encontrar serviços e organizações na sua região:

**Serviços disponíveis:**
- **EMATER**: Assistência técnica gratuita
- **EMBRAPA**: Pesquisa e tecnologias
- **SENAR**: Cursos e capacitação
- **Cooperativas**: Organização coletiva
- **Sindicatos**: Representação política

**Tente perguntas como:**
- "Onde fica a EMATER de Juazeiro?"
- "Como participar de cooperativas de café?"
- "Tem cursos do SENAR na minha região?"
- "Qual é o sindicato dos trabalhadores rurais mais perto?"

**Dica**: Vá pessoalmente ou ligue para os escritórios - eles existem para ajudá-lo!

📚 Referência: MDA e ANATER"""

        return {
            "text": response,
            "confidence": 0.82,
            "context": {"agent": "territorio", "mode": "knowledge_base"},
            "suggested_actions": [
                "Procure escritório da EMATER do seu município",
                "Entre em contato com o sindicato de trabalhadores rurais local"
            ]
        }