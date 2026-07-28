# Metodologia de Extração de Dados Nacionais sobre a Política Nacional de Saúde Bucal

## Resumo

Este documento descreve a estratégia metodológica para identificação, extração e consolidação de dados normativos em nível nacional sobre a Política Nacional de Saúde Bucal (PNSB) no Brasil, cobrindo o período de 2004 a 2026. A abordagem utiliza múltiplas bases de dados federais normativas complementares, com protocolos de busca padronizados e critérios explícitos de inclusão/exclusão, garantindo reprodutibilidade e cobertura abrangente.

**Palavras-chave:** Política Nacional de Saúde Bucal; PNSB; Brasil Sorridente; metodologia de pesquisa; fontes de dados; governo eletrônico.

---

## 1. Introdução

### 1.1 Contexto

A Política Nacional de Saúde Bucal (PNSB), lançada em 2004 sob o programa **Brasil Sorridente**, representa uma das maiores expansões de cobertura em saúde bucal pública do mundo. Sua análise requer a recuperação de documentos normativos produzidos por múltiplos atores institucionais ao longo de mais de duas décadas.

### 1.2 Problema

Não existe uma base de dados unificada que concentre toda a produção normativa federal sobre saúde bucal. Os documentos estão dispersos em:
- Portal da Legislação (LexML/Planalto)
- Diário Oficial da União (DOU)
- Sistemas de informação legislativa

### 1.3 Objetivo

Desenvolver e documentar uma estratégia de busca multi-fonte que:
1. Identifique **toda** a produção normativa federal sobre PNSB (2004–2026)
2. Permita análise temporal por períodos de governo
3. Garanta reprodutibilidade
4. Integre dados normativos de fontes complementares

---

## 2. Desenho do Estudo

### 2.1 Tipo de estudo

Pesquisa documental com abordagem sistemática de múltiplas fontes de dados governamentais.

### 2.2 Escopo temporal

| Período | Governo | Relevância |
|---------|---------|------------|
| 2004–2006 | Lula I | Lançamento do Brasil Sorridente / PNSB |
| 2007–2010 | Lula II | Expansão dos CEO e laboratórios regionais |
| 2011–2014 | Dilma I | Reorganização da rede (Portaria 182/2014) |
| 2015–2016 | Dilma II | Crise orçamentária |
| 2017–2018 | Temer | Revisão da PNSB (Portaria 3.528/2017) |
| 2019–2022 | Bolsonaro I+II | Desmonte parcial / Novo programa |
| 2023–2026 | Lula III | Relançamento / Reestruturação |

### 2.3 Escopo geográfico

**Nacional** — apenas documentos de âmbito federal. Excluem-se:
- Legislação estadual
- Legislação municipal
- Normas de consórcios intermunicipais

### 2.4 Tipo de documento incluído

| Categoria | Exemplos |
|-----------|----------|
| Leis | Lei 14.572/2023 (PNSB) |
| Decretos | Decretos de regulamentação |
| Portarias ministeriais | Portarias do MS/GM |
| Resoluções | CNS, ANS, CIB |
| Normas Operacionais | NOB, NOAS (componente bucal) |
| Planos nacionais | PPA, PNSB textual |
| Proposições legislativas | PL, PLS relacionados |
| Jurisprudência federal | Decisões do STJ, STF |

---

## 3. Fontes de Dados

### 3.1 Visão geral

A estratégia utiliza **3 fontes primárias** organizadas em camadas de complementaridade:

```
CAMADA 1 — Normativa (obrigatória)
├── LexML Brasil ...................... Agregador legislativo (prioridade)
├── Imprensa Nacional (DOU) ........... Fonte oficial primária
└── Base dos Dados (DOU) .............. DOU estruturado (2019–2024)

CAMADA 2 — Jurisprudência (contextual)
└── LexML (jurisprudência) ............ Decisões federais
```

### 3.2 Fonte 1: LexML Brasil

- **URL:** https://www.lexml.gov.br
- **API:** OAI-PMH (Open Archives Initiative)
- **Período:** Variável por tipo documental
- **Formato:** XML estruturado com metadados
- **Cobertura:** Legislação + Jurisprudência + Proposições
- **Vantagem:** Metadados ricos (URN, ementa, assunto), busca facetada
- **Limitação:** Não inclui portarias corriqueiras do MS

### 3.3 Fonte 2: Imprensa Nacional (DOU)

- **URL:** https://www.in.gov.br/consulta
- **API:** https://github.com/Imprensa-Nacional/inlabs (requer cadastro)
- **Período:** 2001–presente (digital)
- **Formato:** PDF + XML (via inlabs)
- **Cobertura:** 100% das publicações federais
- **Vantagem:** Fonte primária oficial, inclui portarias
- **Limitação:** Requer processamento de PDF/XML; cadastro para API

### 3.4 Fonte 3: Base dos Dados (DOU)

- **URL:** https://basedosdados.org/dataset/0bd844d9-454a-4c47-83e2-fc15df4f5ed7
- **API:** BigQuery (SQL)
- **Período:** 2019–2024
- **Formato:** Tabela estruturada (texto + metadados)
- **Cobertura:** DOU Seções 1, 2, 3
- **Vantagem:** Dados tabulares, busca SQL
- **Limitação:** Período restrito; IN suspendeu alimentação em 2024

---

## 4. Estratégia de Busca

### 4.1 Termos de busca

**Termos primários (obrigatórios):**
```
1. "Política Nacional de Saúde Bucal"
2. "PNSB"
3. "Brasil Sorridente"
4. "saúde bucal" AND "SUS"
5. "saúde bucal" AND "atenção básica"
```

**Termos secundários (complementares):**
```
6. "Centro de Especialidades Odontológicas" OR "CEO"
7. "Laboratório Regional de Prótese Dentária" OR "LRPD"
8. "Programa Brasil Sorridente"
9. "Cirurgião-Dentista" AND "ESF" OR "Equipe de Saúde Bucal"
10. "fluoretação" AND "água" AND "SUS"
```

### 4.2 Protocolo de busca por fonte

#### 4.2.1 LexML Brasil

```
URL: https://www.lexml.gov.br/busca
Termo: "Política Nacional de Saúde Bucal"
Filtros:
  - Autoridade: Federal
  - Data: 2004-01-01 até 2026-12-31
```

#### 4.2.2 Imprensa Nacional (DOU via inlabs)

```python
# Estratégia: Download diário via API inlabs → filtragem por termos
# Requer cadastro em https://inlabs.in.gov.br
# Passo 1: Configurar credenciais
# Passo 2: Download de XMLs por período
# Passo 3: Extração de texto dos XMLs
# Passo 4: Busca booleana com os termos definidos
# Passo 5: Classificação por tipo documental
```

#### 4.2.3 Base dos Dados (BigQuery)

```sql
SELECT data_publicacao, titulo, ementa, texto_completo
FROM `basedosdados.br_imprensa_nacional_dou.secao_1`
WHERE data_publicacao BETWEEN '2019-01-01' AND '2024-12-31'
  AND (
    LOWER(texto_completo) LIKE '%política nacional de saúde bucal%'
    OR LOWER(texto_completo) LIKE '%brasil sorridente%'
    OR LOWER(ementa) LIKE '%saúde bucal%'
  )
ORDER BY data_publicacao ASC
```

---

## 5. Critérios de Inclusão e Exclusão

### 5.1 Inclusão

| Critério | Descrição |
|----------|-----------|
| Escopo | Documento de âmbito **federal** |
| Tema | Conteúdo relacionado à PNSB ou saúde bucal no SUS |
| Período | Publicado entre 01/01/2004 e 31/12/2026 |
| Tipo | Lei, decreto, portaria, resolução, norma operacional, plano, proposição |
| Fonte | Uma das 3 fontes primárias |

### 5.2 Exclusão

| Critério | Descrição |
|----------|-----------|
| Escopo | Documentos estaduais ou municipais |
| Tema | Saúde bucal sem vínculo com política nacional |
| Tipo | Pareceres técnicos internos, memorandos |
| Duplicata | Mesmo documento em múltiplas fontes |

---

## 6. Processo de Extração e Consolidação

### 6.1 Fluxograma

```
┌─────────────────────────────────────────────────────────────┐
│                    FONTES DE DADOS                           │
├──────────┬──────────┬──────────────────────────────────────┤
│ LexML    │ DOU      │ Base dos Dados (DOU)                 │
│ (OAI/web)│ (inlabs) │ (BigQuery)                           │
└────┬─────┴────┬─────┴───────────┬──────────────────────────┘
     │          │                 │
     ▼          ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│              EXTRAÇÃO PADRONIZADA                            │
│  (Python: requests, BeautifulSoup, pandas)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              DEDUPLICAÇÃO E LIMPEZA                          │
│  - Identificação por URN/título/data                        │
│  - Normalização de campos                                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              CLASSIFICAÇÃO                                   │
│  - Tipo documental (lei, portaria, resolução...)            │
│  - Tema (PNSB, CEO, LRPD, ESB, fluoretação...)             │
│  - Período de governo                                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              BASE CONSOLIDADA                                │
│  - Formato: CSV + JSON + SQLite                             │
│  - Repositório: GitHub (este repositório)                   │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Variáveis extraídas

| Variável | Tipo | Descrição | Fonte |
|----------|------|-----------|-------|
| `id_documento` | string | Identificador único (hash) | Todas |
| `titulo` | string | Título do documento | Todas |
| `ementa` | text | Ementa/resumo | LexML, DOU |
| `tipo_documento` | categorical | Lei/Decreto/Portaria/Resolução/PL | Todas |
| `orgao_emissor` | string | Órgão responsável | Todas |
| `data_publicacao` | date | Data de publicação | Todas |
| `periodo_governo` | categorical | Governo de referência | Derivada |
| `tema_principal` | categorical | Classificação temática | Derivada |
| `urn` | string | URN LexML (quando disponível) | LexML |
| `fonte_primaria` | string | Fonte de origem | Todas |
| `url_acesso` | string | URL permanente | Todas |

---

## 7. Análise de Dados

### 7.1 Análises previstas

1. **Temporal:** Distribuição de publicações por ano e por governo
2. **Tipológica:** Frequência de tipos documentais
3. **Temática:** Evolução dos temas ao longo do tempo
4. **Rede:** Relações entre documentos (citações, referências, revogações)

### 7.2 Framework analítico

Os dados serão analisados à luz de frameworks de **ciência de políticas públicas**:
- **CFIR** (Consolidated Framework for Implementation Research)
- **RE-AIM** (Reach, Effectiveness, Adoption, Implementation, Maintenance)

---

## 8. Reprodutibilidade

### 8.1 Versionamento

- Todos os scripts estão no GitHub com versionamento Git
- Dados brutos e processados são versionados no repositório
- Ambiente reproduzível via `requirements.txt`

### 8.2 Registro de execução

Cada execução de extração registra:
- Data/hora de execução
- Versão dos scripts (commit hash)
- Parâmetros de busca utilizados
- Número de resultados por fonte

---

## 9. Limitações

| Limitação | Mitigação |
|-----------|----------|
| LexML não indexa todas as portarias | Complementar com DOU direto (inlabs) |
| Base dos Dados DOU limitada a 2019–2024 | Complementar com inlabs (2001+) |
| inlabs requer cadastro | Cadastro gratuito disponível |
| PDFs antigos podem ter OCR imperfeito | Validação manual amostral |
| Termos de busca podem perder documentos | Revisão iterativa + busca por referência cruzada |

---

## 10. Cronograma

| Fase | Atividade | Duração |
|------|-----------|--------|
| 1 | Configuração de APIs e ambiente | 1 semana |
| 2 | Extração LexML | 1 semana |
| 3 | Extração DOU (inlabs) | 2 semanas |
| 4 | Extração Base dos Dados | 1 semana |
| 5 | Consolidação e deduplicação | 1 semana |
| 6 | Classificação e validação | 2 semanas |
| 7 | Análise exploratória | 1 semana |
| **Total** | | **~9 semanas** |

---

## 11. Referências

1. Brasil. Ministério da Saúde. **Política Nacional de Saúde Bucal**. Brasília: MS; 2004.
2. Brasil. Lei nº 14.572, de 8 de maio de 2023. Institui a Política Nacional de Saúde Bucal no âmbito do SUS.
3. Lobczowska NG. Using the Consolidated Framework for Implementation Research (CFIR) to identify factors influencing the implementation of oral health policies in Brazil [Tese]. 2022.
4. Imprensa Nacional. **API inlabs**. Disponível em: https://github.com/Imprensa-Nacional/inlabs
5. Base dos Dados. **Diário Oficial da União (DOU)**. Disponível em: https://basedosdados.org
