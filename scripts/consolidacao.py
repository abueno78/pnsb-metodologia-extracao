#!/usr/bin/env python3
"""
Consolidação de dados de múltiplas fontes sobre a Política Nacional de Saúde Bucal.
Integra: DOU, LexML, Base dos Dados, DATASUS
"""

import os
import json
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter

try:
    import pandas as pd
except ImportError:
    print("Instale dependências: pip install -r requirements.txt")
    raise

# ============================================================
# CONFIGURAÇÃO
# ============================================================

DIR_DADOS = Path("dados")
DIR_CONSOLIDADO = DIR_DADOS / "consolidado"
DIR_CONSOLIDADO.mkdir(parents=True, exist_ok=True)

DB_FILE = DIR_CONSOLIDADO / "pnsb_consolidado.db"


class ConsolidadorPNSB:
    """Consolida dados de múltiplas fontes sobre a PNSB."""
    
    def __init__(self):
        self.documentos = []
        self.indicadores = []
        self.logs = []
    
    def carregar_dou(self) -> List[Dict]:
        """Carrega documentos extraídos do DOU."""
        arquivo = DIR_DADOS / "dou" / "dou_pnsb_extraido.json"
        if not arquivo.exists():
            print("[DOU] Arquivo não encontrado. Execute extracao_dou.py primeiro.")
            return []
        
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        # Padronizar campos
        for doc in dados:
            doc["fonte_primaria"] = "DOU"
            doc.setdefault("urn", "")
            doc.setdefault("assuntos", [])
        
        print(f"[DOU] {len(dados)} documentos carregados")
        return dados
    
    def carregar_lexml(self) -> List[Dict]:
        """Carrega documentos extraídos do LexML."""
        arquivo = DIR_DADOS / "lexml" / "lexml_pnsb_extraido.json"
        if not arquivo.exists():
            print("[LexML] Arquivo não encontrado. Execute extracao_lexml.py primeiro.")
            return []
        
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        # Padronizar campos
        for doc in dados:
            doc["fonte_primaria"] = "LexML"
            doc.setdefault("texto_completo", "")
            doc.setdefault("secao", "")
            doc.setdefault("edicao", "")
            doc.setdefault("orgao_emissor", "")
        
        print(f"[LexML] {len(dados)} documentos carregados")
        return dados
    
    def carregar_datasus(self) -> List[Dict]:
        """Carrega indicadores extraídos do DATASUS."""
        arquivo = DIR_DADOS / "datasus" / "datasus_indicadores_bruto.json"
        if not arquivo.exists():
            print("[DATASUS] Arquivo não encontrado. Execute extracao_datasus.py primeiro.")
            return []
        
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        print(f"[DATASUS] {len(dados)} registros carregados")
        return dados
    
    def deduplicar(self, documentos: List[Dict]) -> List[Dict]:
        """
        Deduplica documentos por título + data + órgão.
        Mantém a versão mais completa (mais campos preenchidos).
        """
        vistos = {}
        
        for doc in documentos:
            # Chave de deduplicação
            chave = self._gerar_chave_deduplicacao(doc)
            
            if chave in vistos:
                # Manter a versão mais completa
                existente = vistos[chave]
                if self._versao_mais_completa(doc, existente):
                    # Mesclar fontes
                    fontes = set(existente.get("fontes", [existente["fonte_primaria"]]))
                    fontes.add(doc["fonte_primaria"])
                    doc["fontes"] = list(fontes)
                    vistos[chave] = doc
                else:
                    fontes = set(existente.get("fontes", [existente["fonte_primaria"]]))
                    fontes.add(doc["fonte_primaria"])
                    existente["fontes"] = list(fontes)
            else:
                doc["fontes"] = [doc["fonte_primaria"]]
                vistos[chave] = doc
        
        return list(vistos.values())
    
    def _gerar_chave_deduplicacao(self, doc: Dict) -> str:
        """Gera chave para deduplicação."""
        titulo = doc.get("titulo", "").lower().strip()
        data = doc.get("data_publicacao", "").strip()
        orgao = doc.get("orgao_emissor", "").strip()
        
        # Normalizar
        titulo = "".join(c for c in titulo if c.isalnum() or c.isspace())
        
        texto = f"{titulo}|{data}|{orgao}"
        return hashlib.md5(texto.encode()).hexdigest()
    
    def _versao_mais_completa(self, doc1: Dict, doc2: Dict) -> bool:
        """Verifica qual versão tem mais campos preenchidos."""
        campos = ["ementa", "texto_completo", "assuntos", "urn"]
        score1 = sum(1 for c in campos if doc1.get(c))
        score2 = sum(1 for c in campos if doc2.get(c))
        return score1 >= score2
    
    def classificar_documentos(self, documentos: List[Dict]) -> List[Dict]:
        """Aplica classificação temática e por período de governo."""
        for doc in documentos:
            # Classificar tema
            if "tema_principal" not in doc or not doc["tema_principal"]:
                doc["tema_principal"] = self._classificar_tema(doc)
            
            # Classificar período de governo
            if "periodo_governo" not in doc or not doc["periodo_governo"]:
                doc["periodo_governo"] = self._classificar_periodo(doc.get("data_publicacao", ""))
        
        return documentos
    
    def _classificar_tema(self, doc: Dict) -> str:
        """Classifica o tema principal do documento."""
        texto = f"{doc.get('titulo', '')} {doc.get('ementa', '')} {doc.get('texto_completo', '')}".lower()
        
        if "política nacional de saúde bucal" in texto or "pnsb" in texto:
            return "PNSB"
        elif "brasil sorridente" in texto:
            return "BS"
        elif "centro de especialidades odontológicas" in texto or "ceo" in texto:
            return "CEO"
        elif "laboratório regional" in texto or "lrpd" in texto:
            return "LRPD"
        elif "equipe de saúde bucal" in texto or "esb" in texto:
            return "ESB"
        elif "fluor" in texto:
            return "FLUOR"
        elif "atenção primária" in texto or "aps" in texto:
            return "APS"
        else:
            return "OUTROS"
    
    def _classificar_periodo(self, data_str: str) -> str:
        """Classifica o período de governo pela data."""
        try:
            if "-" in data_str:
                data = datetime.strptime(data_str.split("T")[0], "%Y-%m-%d")
            else:
                data = datetime.strptime(data_str[:4], "%Y")
            ano = data.year
        except (ValueError, IndexError):
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
    
    def salvar_sqlite(self, documentos: List[Dict], indicadores: List[Dict]):
        """Salva base consolidada em SQLite."""
        conn = sqlite3.connect(str(DB_FILE))
        cursor = conn.cursor()
        
        # Criar tabela de documentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documentos (
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
            )
        """)
        
        # Criar tabela de indicadores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS indicadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ano INTEGER,
                mes INTEGER,
                uf TEXT,
                codigo_procedimento TEXT,
                descricao_procedimento TEXT,
                quantidade INTEGER,
                valor_total REAL
            )
        """)
        
        # Inserir documentos
        for doc in documentos:
            cursor.execute("""
                INSERT OR REPLACE INTO documentos
                (id_documento, titulo, ementa, tipo_documento, data_publicacao,
                 orgao_emissor, fonte_primaria, fontes, tema_principal,
                 periodo_governo, url_fonte, urn, data_extracao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                doc.get("id_documento"),
                doc.get("titulo"),
                doc.get("ementa"),
                doc.get("tipo_documento"),
                doc.get("data_publicacao"),
                doc.get("orgao_emissor"),
                doc.get("fonte_primaria"),
                json.dumps(doc.get("fontes", [])),
                doc.get("tema_principal"),
                doc.get("periodo_governo"),
                doc.get("url_fonte"),
                doc.get("urn"),
                doc.get("data_extracao"),
            ))
        
        # Inserir indicadores
        for ind in indicadores:
            cursor.execute("""
                INSERT INTO indicadores
                (ano, mes, uf, codigo_procedimento, descricao_procedimento,
                 quantidade, valor_total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ind.get("ano"),
                ind.get("mes"),
                ind.get("uf"),
                ind.get("codigo_procedimento"),
                ind.get("descricao_procedimento"),
                ind.get("quantidade"),
                ind.get("valor_total"),
            ))
        
        conn.commit()
        conn.close()
        print(f"Base SQLite salva em: {DB_FILE}")
    
    def exportar_csv(self, documentos: List[Dict]):
        """Exporta documentos para CSV."""
        df = pd.DataFrame(documentos)
        output_file = DIR_CONSOLIDADO / "pnsb_documentos.csv"
        df.to_csv(output_file, index=False, encoding="utf-8")
        print(f"CSV exportado para: {output_file}")
    
    def gerar_relatorio(self, documentos: List[Dict], indicadores: List[Dict]):
        """Gera relatório consolidado."""
        print("\n" + "=" * 70)
        print("RELATÓRIO DE CONSOLIDAÇÃO — PNSB")
        print("=" * 70)
        
        # Total de documentos
        print(f"\n📄 Total de documentos únicos: {len(documentos)}")
        
        # Por fonte
        print("\n📊 Por fonte:")
        fontes = Counter()
        for doc in documentos:
            for f in doc.get("fontes", [doc.get("fonte_primaria")]):
                fontes[f] += 1
        for fonte, count in sorted(fontes.items(), key=lambda x: -x[1]):
            print(f"  {fonte}: {count}")
        
        # Por tipo documental
        print("\n📋 Por tipo documental:")
        tipos = Counter(doc.get("tipo_documento", "Outro") for doc in documentos)
        for tipo, count in sorted(tipos.items(), key=lambda x: -x[1]):
            print(f"  {tipo}: {count}")
        
        # Por período de governo
        print("\n🏛️ Por período de governo:")
        governos = Counter(doc.get("periodo_governo", "DESCONHECIDO") for doc in documentos)
        for gov, count in sorted(governos.items()):
            print(f"  {gov}: {count}")
        
        # Por tema
        print("\n🎯 Por tema:")
        temas = Counter(doc.get("tema_principal", "OUTROS") for doc in documentos)
        for tema, count in sorted(temas.items(), key=lambda x: -x[1]):
            print(f"  {tema}: {count}")
        
        # Indicadores
        if indicadores:
            print(f"\n📈 Total de registros de indicadores: {len(indicadores)}")
            anos = set(ind.get("ano") for ind in indicadores)
            print(f"   Período coberto: {min(anos)}–{max(anos)}")
        
        print("\n" + "=" * 70)
    
    def executar(self):
        """Executa a consolidação completa."""
        print("=" * 70)
        print("CONSOLIDAÇÃO MULTI-FONTE — Política Nacional de Saúde Bucal")
        print("=" * 70)
        print()
        
        # Carregar dados de todas as fontes
        print("[1/5] Carregando dados das fontes...")
        docs_dou = self.carregar_dou()
        docs_lexml = self.carregar_lexml()
        indicadores = self.carregar_datasus()
        
        # Combinar documentos
        todos_documentos = docs_dou + docs_lexml
        print(f"\nTotal de documentos brutos: {len(todos_documentos)}")
        
        # Deduplicar
        print("\n[2/5] Deduplicando...")
        documentos_unicos = self.deduplicar(todos_documentos)
        print(f"Documentos únicos após deduplicação: {len(documentos_unicos)}")
        
        # Classificar
        print("\n[3/5] Classificando documentos...")
        documentos_classificados = self.classificar_documentos(documentos_unicos)
        
        # Salvar
        print("\n[4/5] Salvando base consolidada...")
        self.salvar_sqlite(documentos_classificados, indicadores)
        self.exportar_csv(documentos_classificados)
        
        # Relatório
        print("\n[5/5] Gerando relatório...")
        self.gerar_relatorio(documentos_classificados, indicadores)
        
        print("\n✅ Consolidação concluída!")
        return documentos_classificados, indicadores


if __name__ == "__main__":
    consolidador = ConsolidadorPNSB()
    documentos, indicadores = consolidador.executar()
