"""Testes unitários para PNCPHttpClient (sem rede real)."""
import time
import pytest
import httpx
import pytest_httpx

from pncp_client.http_client import PNCPHttpClient, InMemoryCache, RateLimiter


# ---------------------------------------------------------------------------
# InMemoryCache
# ---------------------------------------------------------------------------

class TestInMemoryCache:
    def test_set_e_get(self):
        cache = InMemoryCache(ttl=60)
        cache.set("http://exemplo.com", {"q": "1"}, {"data": [1, 2, 3]})
        resultado = cache.get("http://exemplo.com", {"q": "1"})
        assert resultado == {"data": [1, 2, 3]}

    def test_miss_retorna_none(self):
        cache = InMemoryCache(ttl=60)
        assert cache.get("http://nao-existe.com") is None

    def test_ttl_expirado(self):
        cache = InMemoryCache(ttl=0)  # TTL zero = expira imediatamente
        cache.set("http://exemplo.com", {}, "valor")
        time.sleep(0.01)
        assert cache.get("http://exemplo.com", {}) is None

    def test_clear(self):
        cache = InMemoryCache(ttl=60)
        cache.set("http://x.com", {}, "y")
        cache.clear()
        assert cache.get("http://x.com", {}) is None

    def test_params_diferentes_sao_chaves_diferentes(self):
        cache = InMemoryCache(ttl=60)
        cache.set("http://x.com", {"p": 1}, "a")
        cache.set("http://x.com", {"p": 2}, "b")
        assert cache.get("http://x.com", {"p": 1}) == "a"
        assert cache.get("http://x.com", {"p": 2}) == "b"


# ---------------------------------------------------------------------------
# RateLimiter
# ---------------------------------------------------------------------------

class TestRateLimiter:
    def test_sem_delay_na_primeira_chamada(self):
        rl = RateLimiter(delay=0.05)
        inicio = time.monotonic()
        rl.wait()
        assert time.monotonic() - inicio < 0.05

    def test_aplica_delay_na_segunda_chamada(self):
        rl = RateLimiter(delay=0.1)
        rl.wait()
        inicio = time.monotonic()
        rl.wait()
        assert time.monotonic() - inicio >= 0.09  # margem de 10ms


# ---------------------------------------------------------------------------
# PNCPHttpClient (com httpx mock)
# ---------------------------------------------------------------------------

class TestPNCPHttpClientGet:
    def test_get_retorna_json(self, httpx_mock):
        httpx_mock.add_response(
            url="https://pncp.gov.br/api/pncp/v1/compras/proposta?pagina=1",
            json={"data": [{"id": 1}]},
        )
        client = PNCPHttpClient(use_cache=False)
        resultado = client.get("/compras/proposta", params={"pagina": 1})
        assert resultado == {"data": [{"id": 1}]}
        client.close()

    def test_get_usa_cache_na_segunda_chamada(self, httpx_mock):
        httpx_mock.add_response(
            url="https://pncp.gov.br/api/pncp/v1/compras/proposta",
            json={"data": []},
        )
        client = PNCPHttpClient(use_cache=True)
        client.get("/compras/proposta")
        # Segunda chamada não deve disparar nova requisição HTTP
        client.get("/compras/proposta")
        assert len(httpx_mock.get_requests()) == 1
        client.close()

    def test_context_manager(self, httpx_mock):
        httpx_mock.add_response(
            url="https://pncp.gov.br/api/pncp/v1/ping",
            json={"ok": True},
        )
        with PNCPHttpClient(use_cache=False) as client:
            r = client.get("/ping")
        assert r == {"ok": True}
