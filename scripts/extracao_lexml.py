#!/usr/bin/env python3
"""
Extração de documentos do LexML Brasil relacionados à Política Nacional de Saúde Bucal.
API: OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting)
"""

import os
import re
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

try:
    import requests
    from bs4 import BeautifulSoup
    from tqdm import tqdm
except ImportError:
    print("Instale dependências: pip install -r requirements.txt")
    raise

# ============================================================
# CONFIGURAÇÃO
# ============================================================

LEXML_BASE_URL = "https://www.lexml.gov.br"
LEXML_OAI_ENDPOINT = f"{LEXML_BASE_URL}/oai"
LEXML_BUSCA_URL = f"{LEXML_BASE_URL}/busca"

DATA_INICIO = "2004-01-01"
DATA_FIM = "2026-12-31"

TERMOS_BUSCA = [
    '"Política Nacional de Saúde Bucal"',
    '"Brasil Sorridente"',
    '"saúde bucal" AND SUS',
    '"Centro de Especialidades Odontológicas"',
    '"Programa Brasil Sorridente"',
    '"Equipe de Saúde Bucal"',
]

DIR_DADOS = Path("dados/lexml")
DIR_DADOS.mkdir(parents=True, exist_ok=True)


@dataclass
class DocumentoLexML:
    """Estrutura de um documento extraído do LexML."""
    id_documento: str
    urn: str
    titulo: str
    ementa: str
    tipo_documento: str
    data_publicacao: str
    autoridade: str
    localidade: str
    assuntos: List[str]
    url_fonte: str
    termos_encontrados: List[str]
    data_extracao: str


def gerar_id_documento(urn: str) -> str:
    """Gera ID único baseado no URN."""
    return hashlib.sha256(urn.encode()).hexdigest()[:16]


def classificar_tipo_documento(titulo: str) -> str:
    """Classifica o tipo documental pelo título."""
    titulo_lower = titulo.lower()
    if "lei" in titulo_lower and "n" in titulo_lower:
        return "Lei"
    elif "decreto" in titulo_lower:
        return "Decreto"
    elif "portaria" in titulo_lower:
        return "Portaria"
    elif "resolução" in titulo_lower:
        return "Resolução"
    elif "projeto de lei" in titulo_lower or titulo_lower.startswith("pl "):
        return "Projeto de Lei"
    elif "habeas corpus" in titulo_lower or "hc" in titulo_lower:
        return "Jurisprudência"
    else:
        return "Outro"


def buscar_termos(texto: str) -> List[str]:
    """Verifica quais termos estão presentes no texto."""
    texto_lower = texto.lower()
    termos_simples = [
        "política nacional de saúde bucal",
        "brasil sorridente",
        "saúde bucal",
        "centro de especialidades odontológicas",
        "equipe de saúde bucal",
    ]
    return [t for t in termos_simples if t in texto_lower]


def buscar_lexml_web(termo: str, pagina: int = 1) -> Dict:
    """
    Busca no LexML via interface web (parsing HTML).
    Retorna resultados da página.
    """
    params = {
        "q": termo,
        "page": pagina,
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Pesquisa Acadêmica PNSB)",
        "Accept": "text/html",
    }
    
    try:
        response = requests.get(LEXML_BUSCA_URL, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        resultados = []
        
        # Parsear resultados
        for item in soup.select(".result-item, .resultado-item"):
            titulo_elem = item.select_one(".titulo a, h3 a")
            ementa_elem = item.select_one(".ementa, .descricao")
            
            if titulo_elem:
                titulo = titulo_elem.get_text(strip=True)
                url = titulo_elem.get("href", "")
                if url and not url.startswith("http"):
                    url = f"{LEXML_BASE_URL}{url}"
                
                ementa = ementa_elem.get_text(strip=True) if ementa_elem else ""
                
                resultados.append({
                    "titulo": titulo,
                    "ementa": ementa,
                    "url": url,
                })
        
        # Verificar se há próxima página
        tem_proxima = soup.select_one(".next, .proximo") is not None
        
        return {"resultados": resultados, "tem_proxima": tem_proxima}
    
    except Exception as e:
        print(f"Erro na busca LexML: {e}")
        return {"resultados": [], "tem_proxima": False}


def buscar_lexml_oai(termo: str) -> List[Dict]:
    """
    Busca via OAI-PMH (mais estruturado, mas limitado).
    """
    resultados = []
    resumption_token = None
    pagina = 0
    
    while True:
        pagina += 1
        params = {
            "verb": "ListRecords",
            "metadataPrefix": "oai_dc",
            "from": DATA_INICIO,
            "until": DATA_FIM,
        }
        
        if resumption_token:
            params = {"verb": "ListRecords", "resumptionToken": resumption_token}
        
        try:
            response = requests.get(LEXML_OAI_ENDPOINT, params=params, timeout=60)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml-xml")
            
            for record in soup.find_all("record"):
                metadata = record.find("metadata")
                if not metadata:
                    continue
                
                dc_title = metadata.find("title")
                dc_description = metadata.find("description")
                dc_date = metadata.find("date")
                dc_identifier = metadata.find("identifier")
                dc_subject = metadata.find_all("subject")
                
                titulo = dc_title.get_text(strip=True) if dc_title else ""
                ementa = dc_description.get_text(strip=True) if dc_description else ""
                data = dc_date.get_text(strip=True) if dc_date else ""
                identifier = dc_identifier.get_text(strip=True) if dc_identifier else ""
                assuntos = [s.get_text(strip=True) for s in dc_subject]
                
                # Filtrar por termos
                texto_conjunto = f"{titulo} {ementa}"
                termos = buscar_termos(texto_conjunto)
                
                if termos:
                    resultados.append({
                        "titulo": titulo,
                        "ementa": ementa,
                        "data": data,
                        "identifier": identifier,
                        "assuntos": assuntos,
                        "termos": termos,
                    })
            
            # Verificar resumption token
            token_elem = soup.find("resumptionToken")
            if token_elem and token_elem.get_text(strip=True):
                resumption_token = token_elem.get_text(strip=True)
                time.sleep(1)  # Rate limiting
            else:
                break
        
        except Exception as e:
            print(f"Erro OAI-PMH (página {pagina}): {e}")
            break
    
    return resultados


def executar_extracao_completa():
    """Executa a extração completa do LexML."""
    print("=" * 60)
    print("EXTRAÇÃO LexML — Política Nacional de Saúde Bucal")
    print("=" * 60)
    print(f"Período: {DATA_INICIO} até {DATA_FIM}")
    print(f"Termos de busca: {len(TERMOS_BUSCA)}")
    print()
    
    todos_resultados = []
    
    # Estratégia 1: Busca web (mais abrangente)
    print("[1/2] Buscando via interface web...")
    for termo in tqdm(TERMOS_BUSCA, desc="Termos"):
        pagina = 1
        while True:
            dados = buscar_lexml_web(termo, pagina)
            resultados = dados["resultados"]
            
            for r in resultados:
                texto_conjunto = f"{r['titulo']} {r['ementa']}"
                termos = buscar_termos(texto_conjunto)
                
                if termos:
                    todos_resultados.append({
                        "titulo": r["titulo"],
                        "ementa": r["ementa"],
                        "url": r["url"],
                        "termos_encontrados": termos,
                        "tipo_documento": classificar_tipo_documento(r["titulo"]),
                    })
            
            if not dados["tem_proxima"]:
                break
            pagina += 1
            time.sleep(0.5)  # Rate limiting
        
        print(f"  '{termo}': {len([r for r in todos_resultados if termo.lower() in r.get('ementa', '').lower()])} resultados")
    
    # Estratégia 2: OAI-PMH (complementar)
    print("\n[2/2] Buscando via OAI-PMH...")
    resultados_oai = buscar_lexml_oai("saúde bucal")
    for r in resultados_oai:
        todos_resultados.append({
            "titulo": r["titulo"],
            "ementa": r["ementa"],
            "url": r.get("identifier", ""),
            "termos_encontrados": r["termos"],
            "tipo_documento": classificar_tipo_documento(r["titulo"]),
            "data_publicacao": r.get("data", ""),
            "assuntos": r.get("assuntos", []),
        })
    
    # Deduplicação
    print(f"\nTotal antes da deduplicação: {len(todos_resultados)}")
    titulos_vistos = set()
    resultados_unicos = []
    for doc in todos_resultados:
        titulo_norm = doc["titulo"].lower().strip()
        if titulo_norm not in titulos_vistos:
            titulos_vistos.add(titulo_norm)
            doc["id_documento"] = gerar_id_documento(doc["titulo"])
            doc["data_extracao"] = datetime.now().isoformat()
            resultados_unicos.append(doc)
    
    print(f"Total após deduplicação: {len(resultados_unicos)}")
    
    # Salvar resultados
    output_file = DIR_DADOS / "lexml_pnsb_extraido.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados_unicos, f, ensure_ascii=False, indent=2)
    print(f"\nResultados salvos em: {output_file}")
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO POR TIPO DOCUMENTAL")
    print("=" * 60)
    from collections import Counter
    tipo_counts = Counter(doc["tipo_documento"] for doc in resultados_unicos)
    for tipo, count in sorted(tipo_counts.items(), key=lambda x: -x[1]):
        print(f"  {tipo}: {count}")
    
    return resultados_unicos


if __name__ == "__main__":
    executar_extracao_completa()
