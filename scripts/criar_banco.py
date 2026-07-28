#!/usr/bin/env python3
"""
Cria o banco de dados consolidado da PNSB com dados extraídos do LexML.
Foco: documentos federais sobre Política Nacional de Saúde Bucal (2004-2026).
"""

import json
import sqlite3
import hashlib
import csv
from datetime import datetime
from pathlib import Path
from collections import Counter

documentos_lexml = [
    {
        "titulo": "Lei nº 14.572 de 08/05/2023",
        "ementa": "Institui a Política Nacional de Saúde Bucal no âmbito do Sistema Único de Saúde (SUS) e altera a Lei nº 8.080, de 19 de setembro de 1990, para incluir a saúde bucal no campo de atuação do SUS.",
        "data_publicacao": "2023-05-08",
        "autoridade": "Federal",
        "urn": "urn:lex:br:federal:lei:2023-05-08;14572",
        "tipo_documento": "Lei",
        "fonte": "LexML"
    },
    {
        "titulo": "PL 7192/2006",
        "ementa": "Estabelece diretrizes para a Política Nacional de Saúde Bucal e dá outras providências.",
        "data_publicacao": "2006-06-08",
        "autoridade": "Câmara dos Deputados",
        "urn": "urn:lex:br:camara.deputados:projeto.lei;pl:2006-06-08;7192",
        "tipo_documento": "Projeto de Lei",
        "fonte": "LexML"
    },
    {
        "titulo": "PL 8131/2017",
        "ementa": "Institui a Política Nacional de Saúde Bucal no âmbito do SUS e altera a Lei nº 8.080/1990.",
        "data_publicacao": "2017-08-01",
        "autoridade": "Senado Federal / Câmara dos Deputados",
        "urn": "urn:lex:br:senado.federal:projeto.lei;pls:2017;8",
        "tipo_documento": "Projeto de Lei",
        "fonte": "LexML"
    },
    {
        "titulo": "PL 6836/2017",
        "ementa": "Dispõe sobre a Política Nacional de Saúde Bucal no âmbito do SUS e altera a Lei nº 8.080/1990.",
        "data_publicacao": "2017-02-07",
        "autoridade": "Câmara dos Deputados",
        "urn": "urn:lex:br:camara.deputados:projeto.lei;pl:2017-02-07;6836",
        "tipo_documento": "Projeto de Lei",
        "fonte": "LexML"
    },
    {
        "titulo": "PL 904/2024",
        "ementa": "Altera a Lei nº 14.572/2023 para dispor sobre a PNSB para Pessoas com Deficiência.",
        "data_publicacao": "2024-03-20",
        "autoridade": "Câmara dos Deputados",
        "urn": "urn:lex:br:camara.deputados:projeto.lei;pl:2024-03-20;904",
        "tipo_documento": "Projeto de Lei",
        "fonte": "LexML"
    },
    {
        "titulo": "AgRg no AgRg no HC 822492 / RO",
        "ementa": "AGRAVO REGIMENTAL EM HC. Remição de pena por estudo. Curso de Saúde Bucal mencionado incidentalmente.",
        "data_publicacao": "2023-08-15",
        "autoridade": "Superior Tribunal de Justiça",
        "urn": "urn:lex:br:superior.tribunal.justica:turma.5:acordao;hc:2023-08-15;822492",
        "tipo_documento": "Jurisprudência",
        "fonte": "LexML"
    },
]

def gerar_id(titulo, data, autoridade):
    return hashlib.sha256(f"{titulo}|{data}|{autoridade}".encode()).hexdigest()[:16]

def classificar_tema(doc):
    texto = f"{doc.get('titulo', '')} {doc.get('ementa', '')}".lower()
    if "política nacional de saúde bucal" in texto or "pnsb" in texto:
        return "PNSB"
    elif "brasil sorridente" in texto:
        return "BS"
    elif "ceo" in texto:
        return "CEO"
    elif "lrpd" in texto:
        return "LRPD"
    elif "esb" in texto:
        return "ESB"
    elif "fluor" in texto:
        return "FLUOR"
    return "SAUDE_BUCAL_GERAL"

def classificar_governo(data_str):
    try:
        ano = int(data_str[:4])
    except (ValueError, IndexError):
        return "DESCONHECIDO"
    if 2003 <= ano <= 2006: return "LULA1"
    elif 2007 <= ano <= 2010: return "LULA2"
    elif 2011 <= ano <= 2014: return "DILMA1"
    elif 2015 <= ano <= 2016: return "DILMA2"
    elif 2017 <= ano <= 2018: return "TEMER"
    elif 2019 <= ano <= 2022: return "BOLSONARO"
    elif ano >= 2023: return "LULA3"
    return "DESCONHECIDO"

def main():
    print("="*70)
    print("CRIAÇÃO DO BANCO DE DADOS — PNSB")
    print("="*70)
    
    autoridades_federais = ["Federal", "Câmara dos Deputados", "Senado Federal",
                            "Senado Federal / Câmara dos Deputados",
                            "Superior Tribunal de Justiça", "Presidência da República"]
    
    docs = []
    for doc in documentos_lexml:
        if doc["autoridade"] not in autoridades_federais:
            continue
        docs.append({
            "id_documento": gerar_id(doc["titulo"], doc["data_publicacao"], doc["autoridade"]),
            "titulo": doc["titulo"],
            "ementa": doc["ementa"],
            "tipo_documento": doc["tipo_documento"],
            "data_publicacao": doc["data_publicacao"],
            "orgao_emissor": doc["autoridade"],
            "fonte_primaria": doc["fonte"],
            "fontes": json.dumps([doc["fonte"]]),
            "tema_principal": classificar_tema(doc),
            "periodo_governo": classificar_governo(doc["data_publicacao"]),
            "url_fonte": f"https://www.lexml.gov.br/resolver/{doc['urn']}",
            "urn": doc["urn"],
            "data_extracao": datetime.now().isoformat(),
        })
    
    print(f"\nDocumentos federais: {len(docs)}")
    
    # Resumos
    for label, key in [("Governo", "periodo_governo"), ("Tipo", "tipo_documento"), ("Tema", "tema_principal")]:
        print(f"\n{label}:")
        for k, v in sorted(Counter(d[key] for d in docs).items(), key=lambda x: -x[1]):
            print(f"  {k}: {v}")
    
    # SQLite
    db_dir = Path("dados/consolidado")
    db_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_dir / "pnsb_consolidado.db"))
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS documentos (
        id_documento TEXT PRIMARY KEY, titulo TEXT, ementa TEXT,
        tipo_documento TEXT, data_publicacao TEXT, orgao_emissor TEXT,
        fonte_primaria TEXT, fontes TEXT, tema_principal TEXT,
        periodo_governo TEXT, url_fonte TEXT, urn TEXT, data_extracao TEXT)""")
    for d in docs:
        c.execute("INSERT OR REPLACE INTO documentos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  tuple(d[k] for k in ["id_documento","titulo","ementa","tipo_documento",
                  "data_publicacao","orgao_emissor","fonte_primaria","fontes","tema_principal",
                  "periodo_governo","url_fonte","urn","data_extracao"]))
    conn.commit()
    conn.close()
    print(f"\n✅ SQLite: {db_dir / 'pnsb_consolidado.db'}")
    
    # CSV
    csv_path = db_dir / "pnsb_documentos.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=docs[0].keys())
        w.writeheader()
        w.writerows(docs)
    print(f"✅ CSV: {csv_path}")
    
    # JSON
    json_path = db_dir / "pnsb_documentos.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON: {json_path}")
    print("\n✅ Concluído!")

if __name__ == "__main__":
    main()
