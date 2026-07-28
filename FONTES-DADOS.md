# Detalhamento Técnico das Fontes de Dados

## Sumário

Este documento fornece o detalhamento técnico de cada fonte de dados utilizada na estratégia de extração, incluindo endpoints, autenticação, limites e exemplos práticos.

---

## 1. LexML Brasil

### 1.1 Visão geral

| Campo | Valor |
|-------|-------|
| Nome oficial | LexML Brasil — Rede de Informação Legislativa e Jurídica |
| URL | https://www.lexml.gov.br |
| API | OAI-PMH + interface web |
| Formato | XML (Dublin Core) + HTML |
| Autenticação | Não requer |

### 1.2 Busca via interface web

```
URL: https://www.lexml.gov.br/busca
Termo: "Política Nacional de Saúde Bucal"
Filtros disponíveis:
  - Categoria: Legislação / Jurisprudência / Proposições / Doutrina
  - Localidade: Brasil / Estados / Municípios
  - Autoridade: Federal / Estadual / Municipal
  - Data: intervalo personalizado
```

### 1.3 Estratégia de extração

```python
import requests
from bs4 import BeautifulSoup

LEXML_BUSCA_URL = "https://www.lexml.gov.br/busca"

def buscar_lexml(termo, pagina=1):
    """Busca no LexML via interface web."""
    params = {"query": termo, "page": pagina}
    headers = {"User-Agent": "Mozilla/5.0 (Pesquisa Acadêmica)"}
    
    response = requests.get(LEXML_BUSCA_URL, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    
    resultados = []
    for item in soup.select(".result-item"):
        titulo = item.select_one(".titulo a")
        ementa = item.select_one(".ementa")
        if titulo:
            resultados.append({
                "titulo": titulo.get_text(strip=True),
                "ementa": ementa.get_text(strip=True) if ementa else "",
                "url": titulo.get("href", ""),
            })
    return resultados
```

### 1.4 Campos extraídos

- Título do documento
- Ementa
- URN (identificador único)
- Data de publicação
- Autoridade emitente
- Localidade
- Assuntos/Indexação
- Tipo documental

---

## 2. Imprensa Nacional — DOU (via inlabs)

### 2.1 Visão geral

| Campo | Valor |
|-------|-------|
| Nome oficial | Diário Oficial da União |
| URL | https://www.in.gov.br |
| API | https://github.com/Imprensa-Nacional/inlabs |
| Formato | XML estruturado + PDF |
| Período | 2001–presente |
| Autenticação | Requer cadastro gratuito |

### 2.2 Acesso via inlabs

```bash
# Clonar repositório
git clone https://github.com/Imprensa-Nacional/inlabs.git

# Configurar credenciais (editar script)
# login = "seu@email.com"
# senha = "sua_senha"

# Download de XMLs
python public/python/inlabs-auto-download-xml.py
```

### 2.3 Estrutura do XML

```xml
<documento>
  <identifica>
    <pubName>Diário Oficial da União</pubName>
    <publishDate>2023-05-08</publishDate>
    <edition>87</edition>
    <section>1</section>
  </identifica>
  <materia>
    <titulo>LEI Nº 14.572, DE 8 DE MAIO DE 2023</titulo>
    <ementa>Institui a Política Nacional de Saúde Bucal...</ementa>
    <texto>...</texto>
  </materia>
</documento>
```

### 2.4 Estratégia de filtragem

```python
TERMOS_BUSCA = [
    "política nacional de saúde bucal",
    "brasil sorridente",
    "saúde bucal sus",
    "centro de especialidades odontológicas",
]

def filtrar_dou(xml_path):
    """Filtra documentos do DOU relacionados à saúde bucal."""
    # Parse XML e busca termos
    # Retorna lista de documentos matching
```

---

## 3. Base dos Dados (BigQuery)

### 3.1 Visão geral

| Campo | Valor |
|-------|-------|
| Dataset | `br_imprensa_nacional_dou` |
| Tabelas | `secao_1`, `secao_2`, `secao_3` |
| Período | 2019–2024 |
| Acesso | BigQuery (gratuito até 1TB/mês) |
| Autenticação | Google Cloud account |

### 3.2 Queries SQL

```sql
SELECT
  data_publicacao,
  titulo,
  ementa,
  texto_completo
FROM `basedosdados.br_imprensa_nacional_dou.secao_1`
WHERE data_publicacao BETWEEN '2019-01-01' AND '2024-12-31'
  AND (
    LOWER(texto_completo) LIKE '%política nacional de saúde bucal%'
    OR LOWER(texto_completo) LIKE '%brasil sorridente%'
    OR LOWER(ementa) LIKE '%saúde bucal%'
  )
ORDER BY data_publicacao ASC
```

### 3.3 Acesso via Python

```python
from google.cloud import bigquery

def consultar_dou_bigquery(query):
    client = bigquery.Client()
    query_job = client.query(query)
    return query_job.to_dataframe()
```

---

## 4. Estratégia de Integração

### 4.1 Prioridade de fontes

```
1. LexML — FONTE PRIMÁRIA (metadados ricos, busca facetada)
2. Imprensa Nacional (DOU via inlabs) — Complementar (portarias)
3. Base dos Dados — Complementar (período 2019-2024, SQL)
```

### 4.2 Deduplicação

Documentos podem aparecer em múltiplas fontes. A deduplicação será feita por:
1. **URN** (quando disponível — LexML)
2. **Título + Data + Órgão** (hash combinado)
3. **Número do documento + Tipo + Data**

### 4.3 Resolução de conflitos

Quando houver discrepância entre fontes:
- **Texto:** Priorizar Imprensa Nacional (fonte oficial)
- **Data de publicação:** Priorizar DOU
- **Ementa:** Priorizar LexML (mais estruturada)
