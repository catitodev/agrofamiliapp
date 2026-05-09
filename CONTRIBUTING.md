# Como contribuir com o AgroFamíliApp

Obrigada por querer contribuir! Este projeto é um bem público digital,
construído coletivamente para servir agricultores familiares brasileiros.
Toda contribuição é bem-vinda — código, conteúdo agroecológico, traduções,
correções, relatos de uso real no campo.

## Princípios que guiam este projeto

- Agroecologia como base epistêmica, não apenas técnica
- Linguagem acessível ao agricultor, não ao desenvolvedor
- Gratuito para sempre, para todos, sem exceção
- Conhecimento tradicional tem o mesmo peso que conhecimento acadêmico
- Decisões coletivas, crédito coletivo

## O que você pode contribuir

### Conteúdo e conhecimento
- Textos sobre agricultura sintrópica, biodinâmica, orgânica e natural
- Correções de nomenclatura (ex: DAP foi substituída pela CAF em 2023)
- Informações sobre políticas públicas atualizadas (Pronaf, PAA, PNAE, etc.)
- Saberes tradicionais e práticas regionais documentadas com consentimento
- Revisão de respostas do agente que estejam imprecisas ou desatualizadas

### Código
- Novos agentes especializados
- Integrações com APIs públicas (INMET, CONAB, CEPEA, MAPA, IBGE)
- Melhorias nos canais (WhatsApp, Telegram, WebApp)
- Otimizações de performance na inferência (AMD ROCm / vLLM)
- Testes automatizados
- Acessibilidade e suporte a baixa conectividade

### Comunidade
- Relatos de uso real — o que funcionou, o que não funcionou
- Tradução para línguas indígenas ou crioulas faladas em comunidades rurais
- Documentação em linguagem simples
- Divulgação em cooperativas, sindicatos rurais, escolas do campo

## Como submeter uma contribuição

### Para contribuições de conteúdo/conhecimento
1. Abra uma **Issue** com o rótulo `conhecimento`
2. Descreva a informação, cite a fonte se houver
3. Indique a região/contexto de aplicabilidade
4. Um mantenedor vai revisar e incorporar à base RAG

### Para contribuições de código
1. Faça um **fork** do repositório
2. Crie um branch com nome descritivo:
   `git checkout -b feat/agente-clima-nordeste`
3. Faça commits pequenos e descritivos em português:
   `git commit -m "adiciona previsão de seca para região semiárida"`
4. Abra um **Pull Request** descrevendo o que muda e por quê
5. Aguarde revisão — respondemos em até 7 dias

### Para reportar problemas
- Abra uma **Issue** com o rótulo `bug` ou `conteúdo incorreto`
- Se for uma resposta errada do agente, cole o exemplo da conversa
- Se for dado desatualizado, indique a fonte correta

## Padrões de código

- Python 3.11+
- Formatação: `black` + `isort`
- Docstrings em português
- Nomes de variáveis em português ou inglês — seja consistente dentro do módulo
- Testes com `pytest`
- Nenhuma dependência proprietária — apenas bibliotecas compatíveis com AGPL

## Padrões de conteúdo

- Português brasileiro, linguagem simples
- Evitar jargão técnico sem explicação
- Sempre indicar se uma informação é regional (não generalize o Brasil)
- Políticas públicas: sempre incluir data de referência da informação
- Não incluir conteúdo de fontes que proíbam redistribuição

## Créditos

Toda contribuição aceita é registrada no arquivo `CONTRIBUTORS.md`.
Contribuições de conhecimento tradicional são atribuídas à comunidade
ou pessoa indicada — nunca anonimizadas sem consentimento explícito.

## Dúvidas

Abra uma Issue com o rótulo `pergunta` ou entre em contato pelo canal
oficial do projeto. Não existe pergunta boba aqui.
