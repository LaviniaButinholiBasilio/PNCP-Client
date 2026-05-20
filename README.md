# 🏛️ PNCP Client

> Cliente Python para consulta ao **Portal Nacional de Compras Públicas (PNCP)**  
> Pesquise licitações, contratos, atas de registro de preços e preços praticados — direto do terminal ou via código.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/Licença-MIT-green)](LICENSE)
[![API](https://img.shields.io/badge/API-PNCP%20Gov.br-yellow)](https://pncp.gov.br)

---

## 📋 Índice

- [Sobre](#sobre)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso — CLI](#uso--cli)
- [Uso — Biblioteca Python](#uso--biblioteca-python)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Dependências](#dependências)
- [Roadmap](#roadmap)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## Sobre

O **PNCP Client** é uma ferramenta de linha de comando e biblioteca Python que abstrai a API REST pública do [Portal Nacional de Compras Públicas](https://www.pncp.gov.br), permitindo consultar e exportar dados de compras governamentais de forma simples e programática.

A API do PNCP é **pública e gratuita** — não requer cadastro ou token para leitura.

---

## Funcionalidades

- 🔍 **Buscar licitações** com filtros por UF, modalidade, período e órgão
- 💰 **Pesquisar preços** praticados em compras públicas, com estatísticas (média, mediana, min/max)
- 📄 **Consultar contratos** celebrados por órgãos públicos
- 📋 **Consultar atas** de registro de preços
- ⬇️ **Baixar documentos** (editais, anexos, contratos em PDF) — individual ou em lote
- 📊 **Exportar dados** para CSV, Excel (.xlsx) e JSON
- 💾 **Cache local** em SQLite para evitar requisições repetidas
- 🔄 **Retry automático** em caso de falhas na API

---

## Instalação

**Pré-requisitos:** Python 3.11 ou superior.

```bash
# Via pip (recomendado)
pip install pncp-client

# Ou clonando o repositório
git clone https://github.com/seu-usuario/pncp-client.git
cd pncp-client
pip install -e ".[dev]"
```

Verificando a instalação:

```bash
pncp --help
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto (ou copie o exemplo):

```bash
cp .env.example .env
```

Variáveis disponíveis:

```env
PNCP_BASE_URL=https://pncp.gov.br/api/pncp/v1
PNCP_TIMEOUT=30
PNCP_RATE_LIMIT_DELAY=0.5
PNCP_MAX_RETRIES=3
PNCP_DOWNLOAD_DIR=./downloads
PNCP_DB_PATH=./pncp.db
PNCP_CACHE_TTL=3600
```

Todas as variáveis têm valores padrão — a configuração é opcional.

---

## Uso — CLI

### Licitações

```bash
# Buscar licitações por estado
pncp licitacoes buscar --uf SP

# Filtrar por período
pncp licitacoes buscar --uf RJ --de 2026-01-01 --ate 2026-05-31

# Filtrar por modalidade (1=Leilão, 6=Pregão, 8=Concurso...)
pncp licitacoes buscar --uf MG --modalidade 6

# Exportar resultado para Excel
pncp licitacoes buscar --uf SP --exportar excel

# Ver detalhes de uma licitação específica
pncp licitacoes detalhe 12345678000195 2026 42

# Listar itens de uma licitação
pncp licitacoes itens 12345678000195 2026 42
```

### Pesquisa de Preços

```bash
# Pesquisar preços de um item
pncp preco "notebook i5"

# Filtrar por UF e exportar
pncp preco "cadeira ergonômica" --uf SP --exportar csv

# Exibir mais amostras
pncp preco "papel A4" --paginas 5
```

Saída de exemplo:

```
Estatísticas para: notebook i5
  Amostras:  47
  Mínimo:    R$ 2.450,00
  Máximo:    R$ 5.899,00
  Média:     R$ 3.812,34
  Mediana:   R$ 3.650,00
  Desvio:    R$   721,18
```

### Contratos

```bash
# Consultar contratos de um órgão
pncp contratos buscar --cnpj 12345678000195 --ano 2026

# Ver detalhes de um contrato
pncp contratos detalhe 12345678000195 2026 10
```

### Atas de Registro de Preços

```bash
# Listar atas de um órgão
pncp atas buscar --cnpj 12345678000195 --ano 2025

# Ver itens de uma ata
pncp atas itens 12345678000195 2025 3
```

### Download de Documentos

```bash
# Listar documentos disponíveis
pncp baixar 12345678000195 2026 42

# Baixar todos os documentos de uma licitação
pncp baixar 12345678000195 2026 42 --todos

# Baixar um documento específico pelo ID
pncp baixar 12345678000195 2026 42 --id 5
```

Os arquivos são salvos em `downloads/{cnpj}/{ano}/{sequencial}/`.

---

## Uso — Biblioteca Python

```python
from pncp_client import PNCPClient

client = PNCPClient()

# ── Licitações ──────────────────────────────────────────────
licitacoes = client.licitacoes.buscar(
    uf="SP",
    data_inicio="2026-01-01",
    data_fim="2026-05-31"
)

for lic in licitacoes:
    print(f"{lic.orgao_nome}: {lic.objeto_compra[:60]}")
    print(f"  Valor estimado: R$ {lic.valor_total_estimado:,.2f}")

# ── Pesquisa de Preços ───────────────────────────────────────
precos = client.pesquisa_preco.pesquisar("cadeira de escritório", uf="SP")
stats = client.pesquisa_preco.estatisticas(precos)

print(f"Mediana: R$ {stats['mediana']:.2f} ({stats['total_amostras']} amostras)")

# ── Contratos ────────────────────────────────────────────────
contratos = client.contratos.buscar(cnpj="12345678000195", ano=2026)

# ── Atas de Registro de Preços ───────────────────────────────
atas = client.atas.buscar(cnpj="12345678000195", ano=2025)

# ── Download de Documentos ───────────────────────────────────
arquivos = client.documentos.baixar_todos("12345678000195", 2026, 42)
print(f"{len(arquivos)} arquivo(s) baixados.")

# ── Exportação ───────────────────────────────────────────────
import pandas as pd

df = pd.DataFrame([lic.model_dump() for lic in licitacoes])
df.to_excel("licitacoes_sp_2026.xlsx", index=False)
df.to_csv("licitacoes_sp_2026.csv", index=False)
```

---

## Estrutura do Projeto

```
pncp-client/
├── pncp_client/
│   ├── api/
│   │   ├── licitacoes.py       # Endpoints de licitações
│   │   ├── contratos.py        # Endpoints de contratos
│   │   ├── atas.py             # Atas de registro de preços
│   │   ├── documentos.py       # Download de arquivos
│   │   └── pesquisa_preco.py   # Pesquisa e estatísticas de preços
│   ├── models/
│   │   ├── licitacao.py        # Modelos Pydantic
│   │   ├── contrato.py
│   │   ├── ata.py
│   │   └── preco.py
│   ├── storage/
│   │   ├── database.py         # SQLite (SQLAlchemy)
│   │   └── cache.py            # Cache de requisições
│   ├── exportacao/
│   │   ├── csv_exporter.py
│   │   ├── excel_exporter.py
│   │   └── json_exporter.py
│   ├── http_client.py          # Cliente HTTP com retry e rate limiting
│   └── config.py               # Configurações e variáveis de ambiente
├── cli/
│   ├── main.py                 # Entrypoint CLI (Typer)
│   ├── cmd_licitacoes.py
│   ├── cmd_contratos.py
│   ├── cmd_atas.py
│   ├── cmd_preco.py
│   └── cmd_documentos.py
├── tests/
│   ├── unit/
│   └── integration/
├── downloads/                  # Documentos baixados (gerado automaticamente)
├── .env.example
├── pyproject.toml
└── README.md
```

---

## Dependências

| Pacote | Versão | Uso |
|---|---|---|
| `httpx` | ≥ 0.27 | Requisições HTTP |
| `pydantic` | ≥ 2.6 | Modelos e validação de dados |
| `typer` | ≥ 0.12 | Interface de linha de comando |
| `rich` | ≥ 13.7 | Output colorido e tabelas no terminal |
| `tenacity` | ≥ 8.2 | Retry automático em falhas |
| `sqlalchemy` | ≥ 2.0 | Persistência local (SQLite) |
| `pandas` | ≥ 2.2 | Manipulação e exportação de dados |
| `openpyxl` | ≥ 3.1 | Exportação para Excel |
| `python-dotenv` | ≥ 1.0 | Variáveis de ambiente |
| `tqdm` | ≥ 4.66 | Barra de progresso no download |

---

## Roadmap

- [x] Estrutura base do projeto
- [x] HTTP Client com retry e rate limiting
- [x] Modelos Pydantic para todos os recursos
- [ ] Módulos de API: licitações, contratos, atas
- [ ] Pesquisa de preços com estatísticas
- [ ] Download de documentos em lote
- [ ] Cache local em SQLite
- [ ] CLI com Typer + Rich
- [ ] Exportação CSV / Excel / JSON
- [ ] Testes de integração
- [ ] Documentação com MkDocs
- [ ] Publicação no PyPI

---

## Contribuindo

Contribuições são bem-vindas! Veja como começar:

```bash
# Fork o repositório e clone
git clone https://github.com/seu-usuario/pncp-client.git
cd pncp-client

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# Instale as dependências de desenvolvimento
pip install -e ".[dev]"

# Rode os testes
pytest tests/ -v

# Verifique o estilo de código
ruff check .
mypy pncp_client/
```

Antes de abrir um PR, certifique-se de que os testes passam e o código está formatado com `ruff`.

---

## Referências

- [Portal Nacional de Compras Públicas](https://www.pncp.gov.br)
- [Documentação da API PNCP](https://pncp.gov.br/app/documentos/Manualdeusurio.pdf)
- [BrasilAPI](https://brasilapi.com.br/docs)
- [Lei nº 14.133/2021 — Nova Lei de Licitações](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/L14133.htm)

---

## Licença

Distribuído sob a licença **MIT**. Veja [`LICENSE`](LICENSE) para mais detalhes.

---

> Dados obtidos via API pública do Governo Federal brasileiro.  
> Este projeto não possui vínculo oficial com o PNCP ou o Governo Federal.
