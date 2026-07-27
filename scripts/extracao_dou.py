#!/usr/bin/env python3
"""
Extração de documentos do DOU relacionados à Política Nacional de Saúde Bucal.
Fonte: Imprensa Nacional (via inlabs ou scraping direto)
"""

import os
import re
import json
import xml.etree.ElementTree as ET
from datetime import datetime, date
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

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

DATA_INICIO = "2004-01-01"
DATA_FIM = "2026-12-31"

TERMOS_BUSCA = [
    "política nacional de saúde bucal",
    "pnsb",
    "brasil sorridente",
    "programa brasil sorridente",
    "centro de especialidades odontológicas",
    "laboratório regional de prótese dentária",
    "equipe de saúde bucal",
    "saúde bucal sus",
    "política de saúde bucal",
    "atenção odontológica sus",
]

# Diretórios
DIR_DADOS = Path("dados/dou")
DIR_DADOS.mkdir(parents=True, exist_ok=True)


@dataclass
class DocumentoDOU:
    """Estrutura de um documento extraído do DOU."""
    id_documento: str
    titulo: str
    ementa: str
    tipo_documento: str
    numero: str
    data_publicacao: str
    orgao_emissor: str
    secao: str
    edicao: str
    texto_completo: str
    termos_encontrados: List[str]
    url_fonte: str
    data_extracao: str


def gerar_id_documento(titulo: str, data: str, orgao: str) -> str:
    """Gera ID único baseado em hash SHA-256."""
    import hashlib
    texto = f"{titulo}|{data}|{orgao}"
    return hashlib.sha256(texto.encode()).hexdigest()[:16]


def classificar_tipo_documento(titulo: str) -> str:
    """Classifica o tipo documental pelo título."""
    titulo_lower = titulo.lower()
    if titulo_lower.startswith("lei"):
        return "Lei"
    elif titulo_lower.startswith("decreto"):
        return "Decreto"
    elif "portaria" in titulo_lower:
        return "Portaria"
    elif "resolução" in titulo_lower or "resolucao" in titulo_lower:
        return "Resolução"
    elif "norma operacional" in titulo_lower:
        return "Norma Operacional"
    elif "edital" in titulo_lower:
        return "Edital"
    elif "plano" in titulo_lower:
        return "Plano"
    else:
        return "Outro"


def classificar_tema(texto: str) -> str:
    """Classifica o tema principal do documento."""
    texto_lower = texto.lower()
    if "política nacional de saúde bucal" in texto_lower or "pnsb" in texto_lower:
        return "PNSB"
    elif "brasil sorridente" in texto_lower:
        return "BS"
    elif "centro de especialidades odontológicas" in texto_lower or "ceo" in texto_lower:
        return "CEO"
    elif "laboratório regional" in texto_lower or "lrpd" in texto_lower:
        return "LRPD"
    elif "equipe de saúde bucal" in texto_lower or "esb" in texto_lower:
        return "ESB"
    elif "fluor" in texto_lower:
        return "FLUOR"
    elif "atenção primária" in texto_lower or "aps" in texto_lower:
        return "APS"
    else:
        return "OUTROS"


def classificar_periodo_governo(data_str: str) -> str:
    """Classifica o período de governo pela data."""
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d")
        ano = data.year
    except ValueError:
        return "DESCONHECIDO"
    
    if 2003 <= ano <= 2006:
        return "LULA1"
    elif 2007 <= ano <= 2010:
        return "LULA2"
    elif 2011 <= ano <= 2014:
        return "DILMA1"
    elif 2015 <= ano <= 2016:
        return "DILMA2"
    elif 2017 <= ano <= 2018:
        return "TEMER"
    elif 2019 <= ano <= 2022:
        return "BOLSONARO"
    elif ano >= 2023:
        return "LULA3"
    return "DESCONHECIDO"


def buscar_termos(texto: str) -> List[str]:
    """Verifica quais termos de busca estão presentes no texto."""
    texto_lower = texto.lower()
    return [t for t in TERMOS_BUSCA if t in texto_lower]


def extrair_dou_inlabs(caminho_xml: str) -> List[Dict]:
    """
    Extrai documentos de um arquivo XML do DOU (formato inlabs).
    """
    resultados = []
    
    try:
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Erro ao parsear {caminho_xml}: {e}")
        return resultados
    
    for materia in root.iter("materia"):
        titulo_elem = materia.find("titulo")
        ementa_elem = materia.find("ementa")
        texto_elem = materia.find("texto")
        
        titulo = titulo_elem.text if titulo_elem is not None and titulo_elem.text else ""
        ementa = ementa_elem.text if ementa_elem is not None and ementa_elem.text else ""
        texto = texto_elem.text if texto_elem is not None and texto_elem.text else ""
        
        texto_conjunto = f"{titulo} {ementa} {texto}"
        termos = buscar_termos(texto_conjunto)
        
        if termos:
            # Extrair data da publicação
            data_pub = ""
            for pub_date in root.iter("publishDate"):
                if pub_date.text:
                    data_pub = pub_date.text
                    break
            
            secao = ""
            for sec in root.iter("section"):
                if sec.text:
                    secao = sec.text
                    break
            
            edicao = ""
            for ed in root.iter("edition"):
                if ed.text:
                    edicao = ed.text
                    break
            
            doc = {
                "id_documento": gerar_id_documento(titulo, data_pub, "DOU"),
                "titulo": titulo,
                "ementa": ementa,
                "tipo_documento": classificar_tipo_documento(titulo),
                "numero": "",
                "data_publicacao": data_pub,
                "orgao_emissor": "Ministério da Saúde",
                "secao": secao,
                "edicao": edicao,
                "texto_completo": texto[:5000],  # Truncar para base
                "termos_encontrados": termos,
                "tema_principal": classificar_tema(texto_conjunto),
                "periodo_governo": classificar_periodo_governo(data_pub),
                "url_fonte": f"https://www.in.gov.br/web/dou/-/busca?q={termos[0]}",
                "data_extracao": datetime.now().isoformat(),
            }
            resultados.append(doc)
    
    return resultados


def buscar_dou_web(query: str, data_inicio: str, data_fim: str) -> List[Dict]:
    """
    Busca no site do DOU (fallback quando inlabs não disponível).
    Nota: Este método pode ser limitado por rate limiting.
    """
    url_base = "https://www.in.gov.br/consulta/-/buscar/dou"
    
    params = {
        "q": query,
        "s": "tdo",
        "exactDate": "custom",
        "publishFrom": data_inicio.replace("-", "/"),
        "publishTo": data_fim.replace("-", "/"),
        "sortType": "0",
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Pesquisa Acadêmica PNSB)",
        "Accept": "application/json",
    }
    
    try:
        response = requests.get(url_base, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        dados = response.json()
        
        resultados = []
        for item in dados.get("jsonArray", []):
            titulo = item.get("title", "")
            content = item.get("content", "")
            pub_date = item.get("pubDate", "")
            
            texto_conjunto = f"{titulo} {content}"
            termos = buscar_termos(texto_conjunto)
            
            if termos:
                doc = {
                    "id_documento": gerar_id_documento(titulo, pub_date, "DOU-WEB"),
                    "titulo": titulo,
                    "ementa": content[:500],
                    "tipo_documento": classificar_tipo_documento(titulo),
                    "numero": "",
                    "data_publicacao": pub_date,
                    "orgao_emissor": "",
                    "secao": item.get("pubName", ""),
                    "edicao": "",
                    "texto_completo": content[:5000],
                    "termos_encontrados": termos,
                    "tema_principal": classificar_tema(texto_conjunto),
                    "periodo_governo": classificar_periodo_governo(pub_date),
                    "url_fonte": item.get("urlTitle", ""),
                    "data_extracao": datetime.now().isoformat(),
                }
                resultados.append(doc)
        
        return resultados
    except Exception as e:
        print(f"Erro na busca web: {e}")
        return []


def executar_extracao_completa():
    """Executa a extração completa do DOU."""
    print("=" * 60)
    print("EXTRAÇÃO DOU — Política Nacional de Saúde Bucal")
    print("=" * 60)
    print(f"Período: {DATA_INICIO} até {DATA_FIM}")
    print(f"Termos de busca: {len(TERMOS_BUSCA)}")
    print()
    
    todos_resultados = []
    
    # Estratégia 1: Buscar via web (mais abrangente para todo o período)
    print("[1/2] Buscando via API web do DOU...")
    for termo in tqdm(TERMOS_BUSCA[:5], desc="Termos"):
        resultados = buscar_dou_web(termo, DATA_INICIO, DATA_FIM)
        todos_resultados.extend(resultados)
        print(f"  '{termo}': {len(resultados)} resultados")
    
    # Estratégia 2: Processar arquivos inlabs (se disponíveis)
    print("\n[2/2] Processando arquivos inlabs (se disponíveis)...")
    dir_inlabs = Path("inlabs/dados")
    if dir_inlabs.exists():
        arquivos_xml = list(dir_inlabs.glob("**/*.xml"))
        for xml_file in tqdm(arquivos_xml, desc="XMLs"):
            resultados = extrair_dou_inlabs(str(xml_file))
            todos_resultados.extend(resultados)
    else:
        print("  Diretório inlabs não encontrado. Pulando.")
    
    # Deduplicação
    print(f"\nTotal antes da deduplicação: {len(todos_resultados)}")
    ids_vistos = set()
    resultados_unicos = []
    for doc in todos_resultados:
        if doc["id_documento"] not in ids_vistos:
            ids_vistos.add(doc["id_documento"])
            resultados_unicos.append(doc)
    
    print(f"Total após deduplicação: {len(resultados_unicos)}")
    
    # Salvar resultados
    output_file = DIR_DADOS / "dou_pnsb_extraido.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(resultados_unicos, f, ensure_ascii=False, indent=2)
    print(f"\nResultados salvos em: {output_file}")
    
    # Resumo por período de governo
    print("\n" + "=" * 60)
    print("RESUMO POR PERÍODO DE GOVERNO")
    print("=" * 60)
    from collections import Counter
    gov_counts = Counter(doc["periodo_governo"] for doc in resultados_unicos)
    for gov, count in sorted(gov_counts.items()):
        print(f"  {gov}: {count} documentos")
    
    # Resumo por tipo
    print("\nRESUMO POR TIPO DOCUMENTAL")
    print("-" * 40)
    tipo_counts = Counter(doc["tipo_documento"] for doc in resultados_unicos)
    for tipo, count in sorted(tipo_counts.items(), key=lambda x: -x[1]):
        print(f"  {tipo}: {count}")
    
    return resultados_unicos


if __name__ == "__main__":
    executar_extracao_completa()
