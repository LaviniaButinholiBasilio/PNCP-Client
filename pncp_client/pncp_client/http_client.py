"""
pncp_client/http_client.py
Cliente HTTP centralizado: retry automático, rate limiting e cache em memória.
"""
from __future__ import annotations

import time
import hashlib
import json
import logging
from typing import Any, Dict, Optional

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log,
)

from .config import Config

logger = logging.getLogger(__name__)


class RateLimiter:
    """Garante um intervalo mínimo entre requisições."""

    def __init__(self, delay: float = Config.RATE_LIMIT_DELAY):
        self._delay = delay
        self._last: float = 0.0

    def wait(self) -> None:
        elapsed = time.monotonic() - self._last
        if elapsed < self._delay:
            time.sleep(self._delay - elapsed)
        self._last = time.monotonic()


class InMemoryCache:
    """Cache simples em memória com TTL por entrada."""

    def __init__(self, ttl: int = Config.CACHE_TTL):
        self._ttl = ttl
        self._store: Dict[str, tuple[Any, float]] = {}

    def _key(self, url: str, params: Optional[Dict] = None) -> str:
        raw = url + json.dumps(params or {}, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, url: str, params: Optional[Dict] = None) -> Optional[Any]:
        key = self._key(url, params)
        entry = self._store.get(key)
        if entry is None:
            return None
        value, ts = entry
        if time.monotonic() - ts > self._ttl:
            del self._store[key]
            return None
        return value

    def set(self, url: str, params: Optional[Dict], value: Any) -> None:
        key = self._key(url, params)
        self._store[key] = (value, time.monotonic())

    def clear(self) -> None:
        self._store.clear()


class PNCPHttpClient:
    """
    Cliente HTTP para a API do PNCP.

    Funcionalidades:
    - Rate limiting configurável
    - Retry automático com back-off exponencial (via tenacity)
    - Cache em memória com TTL
    - Download de arquivos via streaming
    """

    def __init__(
        self,
        base_url: str = Config.BASE_URL,
        consulta_url: str = Config.CONSULTA_URL,
        timeout: int = Config.TIMEOUT,
        use_cache: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.consulta_url = consulta_url.rstrip("/")
        self._rate_limiter = RateLimiter()
        self._cache = InMemoryCache() if use_cache else None
        self._client = httpx.Client(
            timeout=timeout,
            headers=Config.DEFAULT_HEADERS,
            follow_redirects=True,
        )

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        base: str = "pncp",
    ) -> Dict[str, Any]:
        """
        GET em um endpoint da API.

        Args:
            path: Caminho relativo (ex: "/compras/proposta").
            params: Query string como dicionário.
            base: "pncp" usa BASE_URL; "consulta" usa CONSULTA_URL.
        """
        root = self.consulta_url if base == "consulta" else self.base_url
        url = f"{root}{path}"

        if self._cache:
            cached = self._cache.get(url, params)
            if cached is not None:
                logger.debug("Cache hit: %s", url)
                return cached

        result = self._get_with_retry(url, params)

        if self._cache:
            self._cache.set(url, params, result)

        return result

    def download_file(self, url: str, destino: str) -> str:
        """
        Faz download de um arquivo via streaming e salva em *destino*.

        Returns:
            Caminho absoluto do arquivo salvo.
        """
        self._rate_limiter.wait()
        logger.info("Baixando arquivo: %s → %s", url, destino)
        with self._client.stream("GET", url) as r:
            r.raise_for_status()
            with open(destino, "wb") as f:
                for chunk in r.iter_bytes(chunk_size=8192):
                    f.write(chunk)
        return destino

    def close(self) -> None:
        """Fecha o cliente HTTP subjacente."""
        self._client.close()

    def __enter__(self) -> "PNCPHttpClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------

    @retry(
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        stop=stop_after_attempt(Config.MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def _get_with_retry(
        self,
        url: str,
        params: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        self._rate_limiter.wait()
        logger.debug("GET %s params=%s", url, params)
        response = self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()
