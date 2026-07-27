#!/usr/bin/env python3
"""
Extração de indicadores de saúde bucal do DATASUS.
Fontes: SIA (procedimentos ambulatoriais), CNES (estabelecimentos), e-SUS (cobertura APS)
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    import requests
    import pandas as pd
    from tqdm import tqdm
except ImportError:
    print("Instale dependências: pip install -r requirements.txt")
    raise

# ============================================================
# CONFIGURAÇÃO
# ============================================================

DATA_INICIO = "2008"  # SIA odontológico disponível a partir de 2008
DATA_FIM = "2026"

# Códigos de procedimentos odontológicos (SIA)
CODIGOS_ODONTO = {
    "02.10.04.001-1": "Consulta odontológica",
    "02.10.04.002-0": "Escovação supervisionada",
    "02.10.04.003-8": "Aplicação tópica de flúor",
    "02.10.04.004-6": "Aplicação de selante",
    "02.10.04.005-4": "Restauração dental",
    "02.10.04.006-2": "Tratamento endodôntico",
    "02.10.04.007-0": "Exodontia simples",
    "02.10.04.008-9": "Exodontia complexa",
    "02.10.04.009-7": "Profilaxia dental",
    "02.10.04.010-0": "Cirurgia oral menor",
    "02.10.04.019-3": "Atendimento em CEO",
    "02.10.04.024-0": "Prótese dentária",
    "02.10.04.030-4": "Atendimento especializado",
}

DIR_DADOS = Path("dados/datasus")
DIR_DADOS.mkdir(parents=True, exist_ok=True)


def consultar_sia_procedimentos(ano: int, mes: int, uf: str = "BR") -> Dict:
    """
    Consulta procedimentos odontológicos do SIA.
    Usa a API pública do DATASUS (quando disponível) ou scraping do TABNET.
    """
    # Estratégia 1: API pública (se disponível)
    url_api = "https://apisus.saude.gov.br/dados/sia"
    params = {
        "UF": uf,
        "competencia": f"{ano}{mes:02d}",
        "procedimento": "021004",  # prefixo odontológico
    }
    
    try:
        response = requests.get(url_api, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    # Estratégia 2: Download direto do DATASUS (FTP/HTTP)
    return consultar_sia_ftp(ano, mes, uf)


def consultar_sia_ftp(ano: int, mes: int, uf: str) -> Dict:
    """
    Download de arquivos do SIA via FTP/HTTP do DATASUS.
    """
    base_url = "https://datasus.saude.gov.br/transferencia-de-arquivos/"
    
    # O DATASUS disponibiliza arquivos DBF/CSV compactados
    # Formato: SIA{UF}{ANO}{MES}.dbc
    competencia = f"{ano}{mes:02d}"
    
    # URLs de download (exemplo - pode variar)
    url_download = f"https://datasus.saude.gov.br/arquivos/sia/SIA{uf}{competencia}.dbc"
    
    try:
        response = requests.get(url_download, timeout=60, stream=True)
        if response.status_code == 200:
            # Salvar arquivo
            output_file = DIR_DADOS / f"sia_{uf}_{competencia}.dbc"
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return {"status": "ok", "arquivo": str(output_file)}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    
    return {"status": "indisponivel"}


def consultar_cnes_estabelecimentos(ano: int, mes: int) -> Dict:
    """
    Consulta estabelecimentos de saúde bucal (CEO, LRPD) no CNES.
    """
    # CNES disponibiliza dados via download direto
    url_base = "https://datasus.saude.gov.br/transferencia-de-arquivos/"
    
    competencia = f"{ano}{mes:02d}"
    url_download = f"https://datasus.saude.gov.br/arquivos/cnes/CNES{competencia}.dbc"
    
    try:
        response = requests.get(url_download, timeout=60, stream=True)
        if response.status_code == 200:
            output_file = DIR_DADOS / f"cnes_{competencia}.dbc"
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return {"status": "ok", "arquivo": str(output_file)}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    
    return {"status": "indisponivel"}


def processar_arquivo_sia(caminho_arquivo: str) -> pd.DataFrame:
    """
    Processa arquivo DBF/DBC do SIA e filtra procedimentos odontológicos.
    """
    try:
        # Tentar ler como DBF (se tiver dbfread instalado)
        try:
            from dbfread import DBF
            table = DBF(caminho_arquivo, encoding="latin1")
            df = pd.DataFrame(iter(table))
        except ImportError:
            # Fallback: ler como CSV (se convertido)
            df = pd.read_csv(caminho_arquivo)
        
        # Filtrar procedimentos odontológicos
        if "PROC_REAL" in df.columns:
            df_odonto = df[df["PROC_REAL"].str.startswith("021004", na=False)]
            return df_odonto
        
        return pd.DataFrame()
    
    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {e}")
        return pd.DataFrame()


def extrair_indicadores_nacionais(ano_inicio: int, ano_fim: int) -> List[Dict]:
    """
    Extrai indicadores nacionais de saúde bucal ano a ano.
    """
    indicadores = []
    
    for ano in tqdm(range(ano_inicio, ano_fim + 1), desc="Anos"):
        for mes in range(1, 13):
            # Consultar SIA
            resultado_sia = consultar_sia_procedimentos(ano, mes, "BR")
            
            if resultado_sia.get("status") == "ok":
                # Processar arquivo
                df = processar_arquivo_sia(resultado_sia["arquivo"])
                
                if not df.empty:
                    # Agregar por procedimento
                    for codigo, descricao in CODIGOS_ODONTO.items():
                        mask = df["PROC_REAL"] == codigo.replace(".", "").replace("-", "")
                        quantidade = mask.sum()
                        
                        if quantidade > 0:
                            indicadores.append({
                                "ano": ano,
                                "mes": mes,
                                "uf": "BR",
                                "codigo_procedimento": codigo,
                                "descricao_procedimento": descricao,
                                "quantidade": int(quantidade),
                                "valor_total": 0.0,  # Calcular depois
                            })
            
            time.sleep(0.1)  # Rate limiting
    
    return indicadores


def gerar_relatorio_indicadores(indicadores: List[Dict]) -> pd.DataFrame:
    """
    Gera relatório consolidado de indicadores.
    """
    df = pd.DataFrame(indicadores)
    
    if df.empty:
        return df
    
    # Agregar por ano
    df_anual = df.groupby(["ano", "codigo_procedimento", "descricao_procedimento"]).agg({
        "quantidade": "sum"
    }).reset_index()
    
    # Pivotar para ter procedimentos como colunas
    df_pivot = df_anual.pivot_table(
        index="ano",
        columns="descricao_procedimento",
        values="quantidade",
        fill_value=0
    )
    
    return df_pivot


def executar_extracao_completa():
    """Executa a extração completa do DATASUS."""
    print("=" * 60)
    print("EXTRAÇÃO DATASUS — Indicadores de Saúde Bucal")
    print("=" * 60)
    print(f"Período: {DATA_INICIO} até {DATA_FIM}")
    print(f"Procedimentos monitorados: {len(CODIGOS_ODONTO)}")
    print()
    
    # Extrair indicadores
    print("[1/2] Extraindo indicadores nacionais...")
    indicadores = extrair_indicadores_nacionais(int(DATA_INICIO), int(DATA_FIM))
    
    print(f"\nTotal de registros extraídos: {len(indicadores)}")
    
    # Salvar dados brutos
    output_file = DIR_DADOS / "datasus_indicadores_bruto.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(indicadores, f, ensure_ascii=False, indent=2)
    print(f"Dados brutos salvos em: {output_file}")
    
    # Gerar relatório consolidado
    print("\n[2/2] Gerando relatório consolidado...")
    df_relatorio = gerar_relatorio_indicadores(indicadores)
    
    if not df_relatorio.empty:
        output_csv = DIR_DADOS / "datasus_indicadores_consolidado.csv"
        df_relatorio.to_csv(output_csv, encoding="utf-8")
        print(f"Relatório salvo em: {output_csv}")
        
        # Mostrar resumo
        print("\n" + "=" * 60)
        print("RESUMO — PROCEDIMENTOS ODONTOLÓGICOS (NACIONAL)")
        print("=" * 60)
        print(df_relatorio.tail(10))  # Últimos 10 anos
    
    return indicadores


if __name__ == "__main__":
    executar_extracao_completa()
