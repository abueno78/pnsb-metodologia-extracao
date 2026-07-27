# Dicionário de Variáveis — Base Consolidada PNSB

## Sumário

Este documento define todas as variáveis da base consolidada resultante da extração multi-fonte sobre a Política Nacional de Saúde Bucal.

---

## 1. Variáveis de Identificação

| Variável | Tipo | Descrição | Exemplo |
|----------|------|-----------|--------|
| `id_documento` | string | Identificador único gerado (hash SHA-256) | `a1b2c3d4...` |
| `urn_lexml` | string | URN LexML (quando disponível) | `urn:lex:br:federal:lei:2023-05-08;14572` |
| `url_fonte` | string | URL permanente na fonte original | `https://www.lexml.gov.br/...` |
| `fonte_primaria` | categorical | Fonte de origem primária | `DOU`, `LexML`, `BD`, `DATASUS` |
| `fonte_secundaria` | string | Fontes adicionais onde encontrado | `LexML,JusBrasil` |

---

## 2. Variáveis Documentais

| Variável | Tipo | Descrição | Exemplo |
|----------|------|-----------|--------|
| `tipo_documento` | categorical | Tipo do documento | `Lei`, `Decreto`, `Portaria`, `Resolução`, `Norma Operacional`, `Edital`, `Plano` |
| `numero_documento` | string | Número do documento | `14572`, `182`, `3528` |
| `orgao_emissor` | string | Órgão responsável | `Ministério da Saúde`, `Presidência da República`, `Conselho Nacional de Saúde` |
| `sigla_orgao` | string | Sigla do órgão | `MS`, `PR`, `CNS` |
| `data_publicacao` | date | Data de publicação no DOU | `2023-05-08` |
| `data_assinatura` | date | Data de assinatura (se diferente) | `2023-05-07` |
| `data_vigencia` | date | Data de entrada em vigor | `2023-05-09` |
| `secao_dou` | categorical | Seção do DOU | `1`, `2`, `3`, `E` (extra) |
| `edicao_dou` | string | Número da edição | `87-A` |

---

## 3. Variáveis de Conteúdo

| Variável | Tipo | Descrição | Exemplo |
|----------|------|-----------|--------|
| `titulo` | string | Título completo | `LEI Nº 14.572, DE 8 DE MAIO DE 2023` |
| `ementa` | text | Ementa oficial | `Institui a Política Nacional de Saúde Bucal...` |
| `texto_completo` | text | Conteúdo integral (quando disponível) | `...` |
| `resumo` | text | Resumo gerado (se aplicável) | `...` |

---

## 4. Variáveis de Classificação

| Variável | Tipo | Categorias | Descrição |
|----------|------|-----------|-----------|
| `tema_principal` | categorical | Ver abaixo | Tema central do documento |
| `tema_secundario` | categorical | Ver abaixo | Temas adicionais |
| `periodo_governo` | categorical | Ver abaixo | Governo vigente na publicação |
| `status` | categorical | `Vigente`, `Revogada`, `Alterada`, `Suspensa` | Status atual |
| `revoga` | string | ID do documento revogado | `id_documento` |
| `revogado_por` | string | ID do documento que revogou | `id_documento` |
| `altera` | string | ID do documento alterado | `id_documento` |
| `alterado_por` | string | ID do documento que alterou | `id_documento` |

### 4.1 Temas (classificação)

| Código | Tema | Descrição |
|--------|------|-----------|
| `PNSB` | Política Nacional de Saúde Bucal | Marco geral da política |
| `BS` | Brasil Sorridente | Programa Brasil Sorridente |
| `CEO` | Centro de Especialidades Odontológicas | CEO e regulamentação |
| `LRPD` | Laboratório Regional de Prótese Dentária | LRPD e regulamentação |
| `ESB` | Equipe de Saúde Bucal | Composição, incentivos, PNAB |
| `FLUOR` | Fluoretação | Fluoretação de água e programas |
| `APS` | Atenção Primária | Componente bucal na APS |
| `PROC` | Procedimentos | Tabela de procedimentos |
| `FINANC` | Financiamento | Incentivos financeiros |
| `VIGIL` | Vigilância | Epidemiologia e vigilância |
| `EDUC` | Educação | Formação e educação permanente |
| `REGUL` | Regulação | Regulação do setor |
| `OUTROS` | Outros | Não classificado |

### 4.2 Períodos de governo

| Código | Governo | Período |
|--------|---------|--------|
| `LULA1` | Lula I | 2003–2006 |
| `LULA2` | Lula II | 2007–2010 |
| `DILMA1` | Dilma I | 2011–2014 |
| `DILMA2` | Dilma II | 2015–2016 |
| `TEMER` | Temer | 2017–2018 |
| `BOLSONARO1` | Bolsonaro I | 2019–2022 |
| `BOLSONARO2` | Bolsonaro II | 2019–2022 |
| `LULA3` | Lula III | 2023–2026 |

---

## 5. Variáveis de Metadados

| Variável | Tipo | Descrição | Exemplo |
|----------|------|-----------|--------|
| `data_extracao` | datetime | Data/hora da extração | `2026-07-27T23:00:00Z` |
| `versao_script` | string | Commit hash do script | `cd222b4` |
| `termo_busca` | string | Termo que encontrou o documento | `política nacional de saúde bucal` |
| `confianca` | float | Confiança da classificação (0–1) | `0.95` |
| `validacao_manual` | boolean | Se foi validado manualmente | `true` |
| `observacoes` | text | Notas sobre o documento | `...` |

---

## 6. Variáveis de Indicadores (DATASUS)

| Variável | Tipo | Descrição | Exemplo |
|----------|------|-----------|--------|
| `ano` | integer | Ano de competência | `2023` |
| `mes` | integer | Mês de competência | `5` |
| `uf` | string | UF (ou `BR` para nacional) | `BR` |
| `codigo_procedimento` | string | Código SIA/SIH | `02.10.04.001-1` |
| `descricao_procedimento` | string | Descrição do procedimento | `Consulta odontológica` |
| `quantidade` | integer | Quantidade realizada | `15000000` |
| `valor_total` | float | Valor total (R$) | `150000000.00` |
| `cobertura_esb` | float | Cobertura de ESB na APS (%) | `72.5` |
| `num_ceo_ativos` | integer | CEO ativos no período | `983` |
| `num_lprd_ativos` | integer | LRPD ativos no período | `245` |

---

## 7. Esquema de banco de dados

```sql
CREATE TABLE documentos (
    id_documento TEXT PRIMARY KEY,
    urn_lexml TEXT,
    url_fonte TEXT,
    fonte_primaria TEXT NOT NULL,
    fonte_secundaria TEXT,
    tipo_documento TEXT NOT NULL,
    numero_documento TEXT,
    orgao_emissor TEXT,
    sigla_orgao TEXT,
    data_publicacao DATE NOT NULL,
    data_assinatura DATE,
    data_vigencia DATE,
    secao_dou TEXT,
    edicao_dou TEXT,
    titulo TEXT NOT NULL,
    ementa TEXT,
    texto_completo TEXT,
    resumo TEXT,
    tema_principal TEXT,
    tema_secundario TEXT,
    periodo_governo TEXT,
    status TEXT DEFAULT 'Vigente',
    revoga TEXT,
    revogado_por TEXT,
    altera TEXT,
    alterado_por TEXT,
    data_extracao TIMESTAMP,
    versao_script TEXT,
    termo_busca TEXT,
    confianca REAL,
    validacao_manual BOOLEAN DEFAULT FALSE,
    observacoes TEXT
);

CREATE TABLE indicadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ano INTEGER NOT NULL,
    mes INTEGER,
    uf TEXT,
    codigo_procedimento TEXT,
    descricao_procedimento TEXT,
    quantidade INTEGER,
    valor_total REAL,
    cobertura_esb REAL,
    num_ceo_ativos INTEGER,
    num_lprd_ativos INTEGER
);

CREATE TABLE termos_busca (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    termo TEXT NOT NULL,
    categoria TEXT,
    fonte TEXT,
    data_uso TIMESTAMP
);

CREATE TABLE logs_extracao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_execucao TIMESTAMP NOT NULL,
    fonte TEXT NOT NULL,
    versao_script TEXT,
    parametros TEXT,
    num_resultados INTEGER,
    erros TEXT,
    duracao_segundos REAL
);
```

---

## 8. Controle de versão dos dados

Os dados serão versionados usando **DVC (Data Version Control)**:

```bash
# Inicializar DVC
dvc init

# Adicionar dados
dvc add dados/base_consolidada.csv

# Commit
git add dados/base_consolidada.csv.dvc
git commit -m "Atualiza base consolidada v1.0"

# Push para storage remoto
dvc push
```

Cada versão da base terá:
- Hash único (content-addressable)
- Metadados de proveniência
- Link para commit do script que gerou
