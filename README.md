# Estratégia Metodológica para Extração de Dados Nacionais da Política Nacional de Saúde Bucal (PNSB)

## 📋 Sobre este repositório

Este repositório documenta a estratégia metodológica robusta para extração e consolidação de dados normativos em nível **nacional** sobre a **Política Nacional de Saúde Bucal (PNSB)** no âmbito do Sistema Único de Saúde (SUS), utilizando múltiplas bases de dados federais normativas.

## 🎯 Objetivos

1. **Mapear** toda a produção normativa federal sobre saúde bucal (2004–2026)
2. **Consolidar** dados de múltiplas fontes em base unificada
3. **Permitir** análise temporal por períodos de governo
4. **Garantir** reprodutibilidade e transparência metodológica

## 📁 Estrutura do repositório

```
├── README.md                    # Este arquivo
├── METODOLOGIA.md               # Documento metodológico principal (estilo artigo)
├── FONTES-DADOS.md              # Detalhamento técnico de cada fonte
├── DICIONARIO-VARIAVEIS.md      # Dicionário de variáveis extraídas
├── scripts/
│   ├── extracao_dou.py          # Extração do DOU (Imprensa Nacional)
│   ├── extracao_lexml.py        # Extração do LexML
│   └── consolidacao.py          # Consolidação das bases
└── dados/
    └── .gitkeep                 # Diretório para dados extraídos
```

## 🔗 Fontes de dados utilizadas

| Fonte | Escopo | Período | API | Status |
|-------|--------|---------|-----|--------|
| Imprensa Nacional (DOU) | Normas federais | 2001+ | inlabs | ✅ Pública |
| LexML Brasil | Legislação + Jurisprudência | Variável | OAI-PMH | ✅ Pública |
| Base dos Dados (DOU) | DOU estruturado | 2019–2024 | BigQuery | ✅ Pública |
| JusBrasil | DOU + Jurisprudência | Variável | Paga | ⚠️ Suplementar |

## 📊 Escopo

- **Escala:** Nacional (Brasil)
- **Período:** 2004–2026 (cobertura de governos Lula I/II, Dilma I/II, Temer, Bolsonaro, Lula III)
- **Exclusões:** Normas estaduais e municipais; indicadores assistenciais
- **Tipos documentais:** Leis, decretos, portarias, resoluções, normas operacionais

## 📄 Licença

MIT License - Ver arquivo LICENSE

## 👤 Autor

Andre Bueno | Pesquisador PUCRS

## 📖 Como citar

```
Bueno, A. (2026). Estratégia Metodológica para Extração de Dados Nacionais 
da Política Nacional de Saúde Bucal. Repositório GitHub. 
https://github.com/abueno78/pnsb-metodologia-extracao
```
