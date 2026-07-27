# Dados extraídos

Este diretório contém os dados extraídos das diversas fontes.

## Estrutura

```
dados/
├── dou/                    # Dados extraídos do DOU
│   └── dou_pnsb_extraido.json
├── lexml/                  # Dados extraídos do LexML
│   └── lexml_pnsb_extraido.json
├── datasus/                # Dados extraídos do DATASUS
│   ├── datasus_indicadores_bruto.json
│   └── datasus_indicadores_consolidado.csv
└── consolidado/            # Base consolidada multi-fonte
    ├── pnsb_consolidado.db
    └── pnsb_documentos.csv
```

## Como gerar os dados

1. Execute cada script de extração:
   ```bash
   python scripts/extracao_dou.py
   python scripts/extracao_lexml.py
   python scripts/extracao_datasus.py
   ```

2. Execute a consolidação:
   ```bash
   python scripts/consolidacao.py
   ```

## Nota

Os arquivos gerados podem ser grandes e não são versionados no Git.
Use DVC (Data Version Control) para versionar os dados se necessário.
