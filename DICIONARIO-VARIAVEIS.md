# Dicionário de Variáveis — Base Consolidada PNSB

## Sumário

Este documento define todas as variáveis da base consolidada resultante da extração multi-fonte sobre a Política Nacional de Saúde Bucal.

---

## 1. Variáveis de Identificação

| Variável | Tipo | Descrição | Exemplo |
|----------|------|-----------|--------|
| `id_documento` | string | Identificador único (hash SHA-256) | `7b126197ddce60ea` |
| `urn` | string | URN LexML (quando disponível) | `urn:lex:br:federal:lei:2023-05-08;14572` |
| `url_fonte` | string | URL permanente na fonte original | `https://www.lexml.gov.br/resolver/...` |
| `fonte_primaria` | string | Fonte de origem primária | `LexML`, `DOU`, `BD` |
| `fontes` | JSON array | Fontes onde o documento foi encontrado | `["LexML", "DOU"]` |

---

## 2. Variáveis Documentais

| Variável | Tipo | Descrição | Exemplo |
|----------|------|-----------|--------|
| `tipo_documento` | categorical | Tipo do documento | `Lei`, `Decreto`, `Portaria`, `Resolução`, `Projeto de Lei`, `Jurisprudência` |
| `orgao_emissor` | string | Órgão responsável | `Federal`, `Câmara dos Deputados`, `Senado Federal`, `STJ` |
| `data_publicacao` | date | Data de publicação | `2023-05-08` |
| `titulo` | string | Título completo | `Lei nº 14.572 de 08/05/2023` |
| `ementa` | text | Ementa oficial | `Institui a Política Nacional de Saúde Bucal...` |

---

## 3. Variáveis de Classificação

| Variável | Tipo | Categorias | Descrição |
|----------|------|-----------|-----------|
| `tema_principal` | categorical | Ver abaixo | Tema central do documento |
| `periodo_governo` | categorical | Ver abaixo | Governo vigente na publicação |

### 3.1 Temas (classificação)

| Código | Tema | Descrição |
|--------|------|-----------|
| `PNSB` | Política Nacional de Saúde Bucal | Marco geral da política |
| `BS` | Brasil Sorridente | Programa Brasil Sorridente |
| `CEO` | Centro de Especialidades Odontológicas | CEO e regulamentação |
| `LRPD` | Laboratório Regional de Prótese Dentária | LRPD e regulamentação |
| `ESB` | Equipe de Saúde Bucal | Composição, incentivos |
| `FLUOR` | Fluoretação | Fluoretação de água |
| `SAUDE_BUCAL_GERAL` | Saúde Bucal Geral | Outros temas de saúde bucal |

### 3.2 Períodos de governo

| Código | Governo | Período |
|--------|---------|--------|
| `LULA1` | Lula I | 2003–2006 |
| `LULA2` | Lula II | 2007–2010 |
| `DILMA1` | Dilma I | 2011–2014 |
| `DILMA2` | Dilma II | 2015–2016 |
| `TEMER` | Temer | 2017–2018 |
| `BOLSONARO` | Bolsonaro | 2019–2022 |
| `LULA3` | Lula III | 2023–2026 |

---

## 4. Variáveis de Metadados

| Variável | Tipo | Descrição | Exemplo |
|----------|------|-----------|--------|
| `data_extracao` | datetime | Data/hora da extração | `2026-07-28T00:37:35` |

---

## 5. Esquema de banco de dados

```sql
CREATE TABLE documentos (
    id_documento TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    ementa TEXT,
    tipo_documento TEXT,
    data_publicacao TEXT,
    orgao_emissor TEXT,
    fonte_primaria TEXT,
    fontes TEXT,
    tema_principal TEXT,
    periodo_governo TEXT,
    url_fonte TEXT,
    urn TEXT,
    data_extracao TEXT
);
```

---

## 6. Base atual (dados extraídos)

A base consolidada atual contém **6 documentos federais** extraídos do LexML:

| # | Tipo | Título | Data | Governo | Tema |
|---|------|--------|------|---------|------|
| 1 | Lei | Lei nº 14.572/2023 | 2023-05-08 | LULA3 | PNSB |
| 2 | PL | PL 7192/2006 | 2006-06-08 | LULA1 | PNSB |
| 3 | PL | PL 8131/2017 | 2017-08-01 | TEMER | PNSB |
| 4 | PL | PL 6836/2017 | 2017-02-07 | TEMER | PNSB |
| 5 | PL | PL 904/2024 | 2024-03-20 | LULA3 | PNSB |
| 6 | Jurisprudência | AgRg no HC 822492/RO | 2023-08-15 | LULA3 | Geral |

**Período coberto:** 2006–2024
**Fontes:** LexML

---

## 7. Controle de versão dos dados

Os dados são versionados diretamente no repositório GitHub:
- `dados/consolidado/pnsb_documentos.csv` — formato tabular
- `dados/consolidado/pnsb_documentos.json` — formato estruturado
- `dados/consolidado/pnsb_consolidado.db` — banco SQLite
