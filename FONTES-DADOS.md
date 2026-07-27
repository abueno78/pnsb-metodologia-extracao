# Detalhamento Técnico das Fontes de Dados

## Sumário

Este documento fornece o detalhamento técnico de cada fonte de dados utilizada na estratégia de extração, incluindo endpoints, autenticação, limites e exemplos práticos.

---

## 1. Imprensa Nacional — DOU (via inlabs)

### 1.1 Visão geral

| Campo | Valor |
|-------|-------|
| Nome oficial | Diário Oficial da União |
| URL | https://www.in.gov.br |
| API | https://github.com/Imprensa-Nacional/inlabs |
| Formato | XML estruturado + PDF |
| Período | 2001–presente |
| Autenticação | Não requer (dados abertos) |
| Licença | CC BY-ND |

### 1.2 Acesso via inlabs

O repositório `inlabs` disponibiliza scripts Python e Bash para download diário dos artigos individualizados do DOU.

```bash
# Clonar repositório
git clone https://github.com/Imprensa-Nacional/inlabs.git
cd inlabs

# Instalar dependências
pip install -r requirements.txt

# Download de edições específicas
python download_dou.py --secao 1 --data-inicio 2023-01-01 --data-fim 2023-12-31
```

### 1.3 Estrutura do XML

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
    <tipo>Lei</tipo>
    <numero>14572</numero>
    <ementa>Institui a Política Nacional de Saúde Bucal...</ementa>
    <texto>...</texto>
  </materia>
</documento>
```

### 1.4 Estratégia de filtragem

```python
import xml.etree.ElementTree as ET
import os

TERMOS_BUSCA = [
    'política nacional de saúde bucal',
    'brasil sorridente',
    'pnsb',
    'centro de especialidades odontológicas',
    'laboratório regional de prótese',
    'equipe de saúde bucal',
]

def filtrar_dou_saude_bucal(xml_path):
    """Filtra documentos do DOU relacionados à saúde bucal."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    resultados = []
    
    for materia in root.findall('.//materia'):
        texto_completo = materia.find('texto').text.lower()
        titulo = materia.find('titulo').text.lower()
        ementa = materia.find('ementa').text.lower() if materia.find('ementa') is not None else ''
        
        texto_conjunto = f'{titulo} {ementa} {texto_completo}'
        
        for termo in TERMOS_BUSCA:
            if termo in texto_conjunto:
                resultados.append({
                    'titulo': materia.find('titulo').text,
                    'ementa': materia.find('ementa').text if materia.find('ementa') is not None else '',
                    'data': materia.find('.//publishDate').text,
                    'secao': materia.find('.//section').text,
                    'termo_encontrado': termo,
                })
                break
    
    return resultados
```

---

## 2. LexML Brasil

### 2.1 Visão geral

| Campo | Valor |
|-------|-------|
| Nome oficial | LexML Brasil — Rede de Informação Legislativa e Jurídica |
| URL | https://www.lexml.gov.br |
| API | OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting) |
| Endpoint | https://www.lexml.gov.br/oai |
| Formato | XML (Dublin Core) |
| Autenticação | Não requer |

### 2.2 Endpoints OAI-PMH

```
# Listar registros
GET https://www.lexml.gov.br/oai?verb=ListRecords
    &metadataPrefix=oai_dc
    &from=2004-01-01
    &until=2026-12-31
    &set=legislacao

# Buscar por termo
GET https://www.lexml.gov.br/oai?verb=ListRecords
    &metadataPrefix=oai_dc
    &query=saúde bucal AND Política Nacional
```

### 2.3 Estratégia de harvesting

```python
import requests
from xml.etree import ElementTree

LEXML_OAI_ENDPOINT = 'https://www.lexml.gov.br/oai'

def buscar_lexml(termo, data_inicio='2004-01-01', data_fim='2026-12-31'):
    """Busca documentos no LexML via OAI-PMH."""
    params = {
        'verb': 'ListRecords',
        'metadataPrefix': 'oai_dc',
        'from': data_inicio,
        'until': data_fim,
    }
    
    resultados = []
    resumption_token = None
    
    while True:
        if resumption_token:
            params = {'verb': 'ListRecords', 'resumptionToken': resumption_token}
        
        response = requests.get(LEXML_OAI_ENDPOINT, params=params)
        root = ElementTree.fromstring(response.content)
        
        for record in root.findall('.//{http://www.openarchives.org/OAI/2.0/}record'):
            metadata = record.find('.//{http://www.openarchives.org/OAI/2.0/}metadata')
            dc = metadata.find('.//{http://purl.org/dc/elements/1.1/}')
            
            titulo = dc.find('{http://purl.org/dc/elements/1.1/}title')
            ementa = dc.find('{http://purl.org/dc/elements/1.1/}description')
            data = dc.find('{http://purl.org/dc/elements/1.1/}date')
            
            resultados.append({
                'titulo': titulo.text if titulo is not None else '',
                'ementa': ementa.text if ementa is not None else '',
                'data': data.text if data is not None else '',
            })
        
        # Verificar se há mais páginas
        token_elem = root.find('.//{http://www.openarchives.org/OAI/2.0/}resumptionToken')
        if token_elem is not None and token_elem.text:
            resumption_token = token_elem.text
        else:
            break
    
    return resultados
```

### 2.4 Busca via interface web (fallback)

```
URL: https://www.lexml.gov.br/busca
Termo: "Política Nacional de Saúde Bucal"
Filtros:
  - Autoridade: Federal
  - Categoria: Legislação
  - Data: 2004-01-01 até 2026-12-31
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

#### Query 1: Busca geral por termos

```sql
SELECT
  data_publicacao,
  titulo,
  ementa,
  tipo_edicao,
  edicao,
  secao,
  texto_completo,
  'basedosdados_dou' AS fonte
FROM `basedosdados.br_imprensa_nacional_dou.secao_1`
WHERE data_publicacao BETWEEN '2019-01-01' AND '2024-12-31'
  AND (
    LOWER(texto_completo) LIKE '%política nacional de saúde bucal%'
    OR LOWER(texto_completo) LIKE '%brasil sorridente%'
    OR LOWER(ementa) LIKE '%saúde bucal%'
  )
ORDER BY data_publicacao ASC
```

#### Query 2: Portarias do Ministério da Saúde

```sql
SELECT
  data_publicacao,
  titulo,
  ementa,
  texto_completo
FROM `basedosdados.br_imprensa_nacional_dou.secao_1`
WHERE data_publicacao BETWEEN '2019-01-01' AND '2024-12-31'
  AND LOWER(titulo) LIKE '%portaria%'
  AND (
    LOWER(texto_completo) LIKE '%saúde bucal%'
    OR LOWER(texto_completo) LIKE '%odontológica%'
    OR LOWER(texto_completo) LIKE '%dentista%'
    OR LOWER(texto_completo) LIKE '%ceo%'
  )
ORDER BY data_publicacao ASC
```

### 3.3 Acesso via Python

```python
from google.cloud import bigquery

def consultar_dou_bigquery(query):
    """Executa query no BigQuery e retorna DataFrame."""
    client = bigquery.Client()
    query_job = client.query(query)
    return query_job.to_dataframe()
```

---

## 4. DATASUS

### 4.1 Visão geral

| Campo | Valor |
|-------|-------|
| Nome | DATASUS — Departamento de Informática do SUS |
| URL | https://datasus.saude.gov.br |
| API | TABNET (web) + API REST |
| Formato | CSV, DBF, XLS |
| Período | 2000–presente |
| Autenticação | Não requer |

### 4.2 Tabelas relevantes para saúde bucal

| Tabela | Descrição | Período |
|--------|-----------|--------|
| SIA (Sistema de Informações Ambulatoriais) | Procedimentos odontológicos | 2008+ |
| SIH (Sistema de Informações Hospitalares) | Internações odontológicas | 2000+ |
| e-SUS / AB | Equipes de Saúde Bucal na APS | 2012+ |
| CNES | Estabelecimentos (CEO, LRPD) | 2000+ |

### 4.3 Procedimentos odontológicos (SIA)

Códigos de procedimentos relevantes:

| Código | Descrição |
|--------|-----------|
| 02.10.04.001-1 | Consulta odontológica |
| 02.10.04.002-0 | Escovação supervisionada |
| 02.10.04.004-6 | Aplicação tópica de flúor |
| 02.10.04.007-0 | Restauração dental |
| 02.10.04.010-0 | Exodontia |
| 02.10.04.019-3 | Tratamento endodôntico |
| 02.10.04.024-0 | Prótese dentária |
| 02.10.04.030-4 | Atendimento em CEO |

### 4.4 Extração via TABNET

```
URL: https://datasus.saude.gov.br/transferencia-de-arquivos/
Caminho: SIA → Procedimentos → Por localização → Brasil
Ano: 2008–2026
Procedimento: Todos (filtrar depois por códigos odontológicos)
```

### 4.5 Extração via API (quando disponível)

```python
import requests

def consultar_datasus_sia(uf, ano, mes):
    """Consulta procedimentos SIA via API."""
    url = f'https://apisus.saude.gov.br/dados/sia'
    params = {
        'UF': uf,
        'competencia': f'{ano}{mes}',
        'procedimento': '021004',  # prefixo odontológico
    }
    response = requests.get(url, params=params)
    return response.json()
```

---

## 5. JusBrasil (Suplementar)

### 5.1 Visão geral

| Campo | Valor |
|-------|-------|
| URL | https://www.jusbrasil.com.br/diarios/ |
| API | Paga (via Digesto) |
| Cobertura | 300+ diários |
| Formato | Texto + snippet |
| Autenticação | API key |

### 5.2 Uso recomendado

O JusBrasil deve ser utilizado apenas como **fonte suplementar** para:
1. Validação cruzada de documentos encontrados em outras fontes
2. Busca de jurisprudência federal relacionada
3. Cobertura de períodos onde outras fontes têm lacunas

### 5.3 Limitações

- API paga (módulo "Diários Oficiais: buscar" via Digesto)
- Scraping bloqueado por Cloudflare
- Termos de uso restringem mineração em massa
- Não é fonte primária para pesquisa acadêmica

---

## 6. Estratégia de Integração

### 6.1 Prioridade de fontes

```
1. Imprensa Nacional (DOU via inlabs) — FONTE PRIMÁRIA
2. LexML — Complementar (metadados enriquecidos)
3. Base dos Dados — Complementar (período 2019-2024)
4. DATASUS — Indicadores quantitativos
5. JusBrasil — Validação cruzada apenas
```

### 6.2 Deduplicação

Documentos podem aparecer em múltiplas fontes. A deduplicação será feita por:
1. **URN** (quando disponível — LexML)
2. **Título + Data + Órgão** (hash combinado)
3. **Número do documento + Tipo + Data**

### 6.3 Resolução de conflitos

Quando houver discrepância entre fontes:
- **Texto:** Priorizar Imprensa Nacional (fonte oficial)
- **Data de publicação:** Priorizar DOU
- **Ementa:** Priorizar LexML (mais estruturada)
- **Classificação:** Consenso entre fontes
