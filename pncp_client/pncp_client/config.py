"""
pncp_client/config.py
Configurações globais carregadas do ambiente / .env
"""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL: str = os.getenv("PNCP_BASE_URL", "https://pncp.gov.br/api/pncp/v1")
    CONSULTA_URL: str = os.getenv("PNCP_CONSULTA_URL", "https://pncp.gov.br/api/consulta/v1")
    TIMEOUT: int = int(os.getenv("PNCP_TIMEOUT", "30"))
    RATE_LIMIT_DELAY: float = float(os.getenv("PNCP_RATE_LIMIT_DELAY", "0.5"))
    MAX_RETRIES: int = int(os.getenv("PNCP_MAX_RETRIES", "3"))
    DOWNLOAD_DIR: Path = Path(os.getenv("PNCP_DOWNLOAD_DIR", "./downloads"))
    DB_PATH: Path = Path(os.getenv("PNCP_DB_PATH", "./pncp.db"))
    CACHE_TTL: int = int(os.getenv("PNCP_CACHE_TTL", "3600"))

    # Cabeçalhos padrão para todas as requisições
    DEFAULT_HEADERS: dict[str, str] = {
        "Accept": "application/json",
        "User-Agent": "pncp-client/1.0 (python; github.com/seu-usuario/pncp-client)",
    }
