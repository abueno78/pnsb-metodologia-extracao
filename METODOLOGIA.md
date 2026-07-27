# Metodologia de Extração de Dados Nacionais sobre a Política Nacional de Saúde Bucal

## Resumo

Este documento descreve a estratégia metodológica para identificação, extração e consolidação de dados normativos e programáticos em nível nacional sobre a Política Nacional de Saúde Bucal (PNSB) no Brasil, cobrindo o período de 2004 a 2026. A abordagem utiliza múltiplas bases de dados federais complementares, com protocolos de busca padronizados e critérios explícitos de inclusão/exclusão, garantindo reprodutibilidade e cobertura abrangente.

**Palavras-chave:** Política Nacional de Saúde Bucal; PNSB; Brasil Sorridente; metodologia de pesquisa; fontes de dados; governo eletrônico.

---

## 1. Introdução

### 1.1 Contexto

A Política Nacional de Saúde Bucal (PNSB), lançada em 2004 sob o programa **Brasil Sorridente**, representa uma das maiores expansões de cobertura em saúde bucal pública do mundo. Sua análise requer a recuperação de documentos normativos produzidos por múltiplos atores institucionais ao longo de mais de duas décadas.

### 1.2 Problema

Não existe uma base de dados unificada que concentre toda a produção normativa federal sobre saúde bucal. Os documentos estão dispersos em:
- Diário Oficial da União (DOU)
- Portal da Legislação (LexML/Planalto)
- Sistemas de informação em saúde (DATASUS)
- Portais de transparência

### 1.3 Objetivo

Desenvolver e documentar uma estratégia de busca multi-fonte que:
1. Identifique **toda** a produção normativa federal sobre PNSB (2004–2026)
2. Permita análise temporal por períodos de governo
3. Garanta reprodutibilidade
4. Integre dados normativos e indicadores

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
| Editais | Chamadas públicas federais |

---

## 3. Fontes de Dados

### 3.1 Visão geral

A estratégia utiliza **5 fontes primárias** organizadas em camadas de complementaridade:

```
CAMADA 1 — Normativa (obrigatória)
├── Imprensa Nacional (DOU) ........... Fonte oficial primária
├── LexML Brasil ...................... Agregador legislativo
└── Base dos Dados (DOU) .............. DOU estruturado (2019–2024)

CAMADA 2 — Indicadores (complementar)
├── DATASUS / TABNET .................. Indicadores assistenciais
└── Base dos Dados (indicadores) ...... Dados estruturados

CAMADA 3 — Jurisprudência (contextual)
├── LexML (jurisprudência) ............ Decisões federais
└── JusBrasil ......................... DOU + jurisprudência (suplementar)
```

### 3.2 Fonte 1: Imprensa Nacional (DOU)

- **URL:** https://www.in.gov.br/consulta
- **API:** https://github.com/Imprensa-Nacional/inlabs
- **Período:** 2001–presente (digital)
- **Formato:** PDF + XML (via inlabs)
- **Cobertura:** 100% das publicações federais
- **Vantagem:** Fonte primária oficial
- **Limitação:** Requer processamento de PDF/XML

### 3.3 Fonte 2: LexML Brasil

- **URL:** https://www.lexml.gov.br
- **API:** OAI-PMH (Open Archives Initiative)
- **Período:** Variável por tipo documental
- **Formato:** XML estruturado com metadados
- **Cobertura:** Legislação + Jurisprudência + Proposições
- **Vantagem:** Metadados ricos (URN, ementa, assunto)
- **Limitação:** Não inclui portarias corriqueiras

### 3.4 Fonte 3: Base dos Dados (DOU)

- **URL:** https://basedosdados.org/dataset/0bd844d9-454a-4c47-83e2-fc15df4f5ed7
- **API:** BigQuery (SQL)
- **Período:** 2019–2024
- **Formato:** Tabela estruturada (texto + metadados)
- **Cobertura:** DOU Seções 1, 2, 3
- **Vantagem:** Dados tabulares, busca SQL
- **Limitação:** Período restrito; IN suspendeu alimentação em 2024

### 3.5 Fonte 4: DATASUS

- **URL:** https://datasus.saude.gov.br
- **API:** TABNET / API REST
- **Período:** 2000–presente
- **Formato:** CSV / JSON
- **Cobertura:** Indicadores de saúde bucal (SIA/SIH)
- **Vantagem:** Dados quantitativos nacionais
- **Limitação:** Agregação por procedimento, não por norma

### 3.6 Fonte 5: JusBrasil (suplementar)

- **URL:** https://www.jusbrasil.com.br/diarios/
- **API:** Paga (via Digesto)
- **Período:** Variável
- **Cobertura:** 300+ diários (DOU, DOEs, DJe)
- **Vantagem:** Busca textual com snippet
- **Limitação:** API paga; scraping bloqueado por Cloudflare

---

## 4. Estratégia de Busca

### 4.1 Termos de busca

Os seguintes termos serão utilizados em todas as fontes, adaptados à sintaxe de cada plataforma:

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
9. "Cirurgia-Dentista" AND "ESF" OR "Equipe de Saúde Bucal"
10. "fluoretação" AND "água" AND "SUS"
11. "odontologia" AND "política pública"
12. "atenção odontológica" AND "SUS"
```

**Termos para indicadores:**
```
13. "procedimento odontológico" AND "SIA"
14. "produção odontológica" AND "APS"
15. "incentivo saúde bucal"
```

### 4.2 Protocolo de busca por fonte

#### 4.2.1 Imprensa Nacional (DOU via inlabs)

```python
# Estratégia: Download diário via API inlabs → filtragem por termos
# Passo 1: Clonar repositório inlabs
# Passo 2: Configurar download por período
# Passo 3: Extração de texto dos XMLs
# Passo 4: Busca booleana com os termos definidos
# Passo 5: Classificação por tipo documental (portaria, resolução, etc.)
```

**Filtros aplicáveis:**
- Seção: 1 (Atos do Poder Executivo)
- Órgão: Ministério da Saúde
- Data: 01/01/2004 – 31/12/2026

#### 4.2.2 LexML Brasil

```python
# Estratégia: OAI-PMH harvesting com filtros
# Passo 1: Consulta via API com termos de busca
# Passo 2: Filtro por autoridade = Federal
# Passo 3: Filtro por categoria = Legislação
# Passo 4: Paginação completa dos resultados
# Passo 5: Extração de metadados (URN, ementa, data, assunto)
```

**Filtros aplicáveis:**
- Autoridade: Federal
- Esfera: Federal
- Categoria: Legislação / Proposições Legislativas

#### 4.2.3 Base dos Dados (BigQuery)

```sql
-- Query exemplo para DOU via Base dos Dados
SELECT
  data_publicacao,
  titulo,
  ementa,
  tipo_edicao,
  edicao,
  secao,
  texto_completo
FROM `basedosdados.br_imprensa_nacional_dou.secao_1`
WHERE data_publicacao BETWEEN '2019-01-01' AND '2024-12-31'
  AND (
    LOWER(texto_completo) LIKE '%política nacional de saúde bucal%'
    OR LOWER(texto_completo) LIKE '%brasil sorridente%'
    OR LOWER(texto_completo) LIKE '%pnsb%'
    OR (
      LOWER(texto_completo) LIKE '%saúde bucal%'
      AND LOWER(texto_completo) LIKE '%sus%'
    )
  )
ORDER BY data_publicacao ASC
```

#### 4.2.4 DATASUS

```python
# Estratégia: Extração de indicadores via TABNET/API
# Passo 1: Identificar tabelas relevantes (SIA, SIH, e-SUS)
# Passo 2: Extração de procedimentos odontológicos
# Passo 3: Agregação nacional por ano
# Passo 4: Cruzamento com marcos normativos
```

**Indicadores prioritários:**
- Procedimentos odontológicos realizados (SIA)
- Cobertura de Equipes de Saúde Bucal na APS
- Número de CEO ativos
- Produção de próteses (LRPD)

---

## 5. Critérios de Inclusão e Exclusão

### 5.1 Inclusão

| Critério | Descrição |
|----------|-----------|
| Escopo | Documento de âmbito **federal** |
| Tema | Conteúdo relacionado à PNSB ou saúde bucal no SUS |
| Período | Publicado entre 01/01/2004 e 31/12/2026 |
| Tipo | Lei, decreto, portaria, resolução, norma operacional, plano |
| Fonte | Uma das 5 fontes primárias |

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
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│ DOU      │ LexML    │ BD (DOU) │ DATASUS  │ JusBrasil      │
│ (inlabs) │ (OAI)    │ (BQ)     │ (API)    │ (suplementar)  │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴───────┬────────┘
     │          │          │          │             │
     ▼          ▼          ▼          ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│              EXTRAÇÃO PADRONIZADA                            │
│  (Python: requests, BeautifulSoup, pandas, SPARQL)          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              DEDUPLICAÇÃO E LIMPEZA                          │
│  - Identificação de duplicatas por URN/título/data          │
│  - Normalização de campos                                    │
│  - Validação de campos obrigatórios                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              CLASSIFICAÇÃO                                   │
│  - Tipo documental (lei, portaria, resolução...)            │
│  - Tema (PNSB, CEO, LRPD, ESB, fluoretação...)             │
│  - Período de governo                                        │
│  - Órgão emissor                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              BASE CONSOLIDADA                                │
│  - Formato: CSV + Parquet + SQLite                          │
│  - Metadados: proveniência, data extração, versão           │
│  - Repositório: GitHub (este repositório)                   │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Variáveis extraídas

| Variável | Tipo | Descrição | Fonte |
|----------|------|-----------|-------|
| `id_documento` | string | Identificador único (URN ou hash) | Todas |
| `titulo` | string | Título do documento | Todas |
| `ementa` | text | Ementa/resumo | LexML, DOU |
| `tipo_documento` | categorical | Lei/Decreto/Portaria/Resolução | Todas |
| `orgao_emissor` | string | Órgão responsável | Todas |
| `data_publicacao` | date | Data de publicação | Todas |
| `data_assinatura` | date | Data de assinatura (quando diferente) | DOU |
| `periodo_governo` | categorical | Governo de referência | Derivada |
| `tema` | categorical | Classificação temática | Derivada |
| `urn` | string | URN LexML (quando disponível) | LexML |
| `secao_dou` | string | Seção do DOU (1, 2, 3) | DOU |
| `texto_completo` | text | Conteúdo integral | DOU, BD |
| `fonte_primaria` | string | Fonte de origem | Todas |
| `url_acesso` | string | URL permanente | Todas |

---

## 7. Análise de Dados

### 7.1 Análises previstas

1. **Temporal:** Distribuição de publicações por ano e por governo
2. **Tipológica:** Frequência de tipos documentais
3. **Temática:** Evolução dos temas ao longo do tempo
4. **Rede:** Relações entre documentos (citações, referências, revogações)
5. **Indicadores:** Correlação entre marcos normativos e indicadores assistenciais

### 7.2 Framework analítico

Os dados serão analisados à luz de frameworks de **ciência de políticas públicas**:
- **CFIR** (Consolidated Framework for Implementation Research)
- **RE-AIM** (Reach, Effectiveness, Adoption, Implementation, Maintenance)
- **Análise de conteúdo** (Bardin)

---

## 8. Reprodutibilidade

### 8.1 Versionamento

- Todos os scripts estão no GitHub com versionamento Git
- Dados brutos e processados são versionados via DVC (Data Version Control)
- Ambiente reproduzível via `requirements.txt` ou `environment.yml`

### 8.2 Registro de execução

Cada execução de extração registra:
- Data/hora de execução
- Versão dos scripts (commit hash)
- Parâmetros de busca utilizados
- Número de resultados por fonte
- Eventuais erros ou inconsistências

### 8.3 Auditoria

- Logs detalhados de cada etapa
- Validação cruzada entre fontes
- Documentação de decisões de classificação

---

## 9. Limitações

| Limitação | Mitigação |
|-----------|----------|
| Base dos Dados DOU limitada a 2019–2024 | Complementar com inlabs (2001+) |
| LexML não indexa todas as portarias | Complementar com DOU direto |
| JusBrasil tem API paga | Usar apenas como suplementar |
| PDFs antigos podem ter OCR imperfeito | Validação manual amostral |
| Termos de busca podem perder documentos | Revisão iterativa + busca por referência cruzada |
| DATASUS pode ter descontinuidades | Documentar gaps e usar fontes alternativas |

---

## 10. Cronograma

| Fase | Atividade | Duração |
|------|-----------|--------|
| 1 | Configuração de APIs e ambiente | 1 semana |
| 2 | Extração DOU (inlabs) | 2 semanas |
| 3 | Extração LexML | 1 semana |
| 4 | Extração Base dos Dados | 1 semana |
| 5 | Extração DATASUS | 1 semana |
| 6 | Consolidação e deduplicação | 1 semana |
| 7 | Classificação e validação | 2 semanas |
| 8 | Análise exploratória | 1 semana |
| **Total** | | **~10 semanas** |

---

## 11. Referências

1. Brasil. Ministério da Saúde. **Política Nacional de Saúde Bucal**. Brasília: MS; 2004.
2. Brasil. Lei nº 14.572, de 8 de maio de 2023. Institui a Política Nacional de Saúde Bucal no âmbito do SUS.
3. Lobczowska NG. Using the Consolidated Framework for Implementation Research (CFIR) to identify factors influencing the implementation of oral health policies in Brazil [Tese]. 2022.
4. Open Knowledge Brasil. **Querido Diário**: Diários oficiais brasileiros acessíveis a todos. 2024. Disponível em: https://queridodiario.ok.org.br
5. Base dos Dados. **Diário Oficial da União (DOU)**. Disponível em: https://basedosdados.org
6. Imprensa Nacional. **API inlabs**. Disponível em: https://github.com/Imprensa-Nacional/inlabs
