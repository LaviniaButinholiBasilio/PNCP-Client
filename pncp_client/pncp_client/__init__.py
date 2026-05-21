"""
pncp_client
===========
Cliente Python para o Portal Nacional de Compras Públicas (PNCP).

Uso básico::

    from pncp_client import PNCPClient

    client = PNCPClient()

    # Buscar licitações em SP
    licitacoes = client.licitacoes.buscar(uf="SP", data_inicio="2026-01-01")

    # Pesquisar preços
    precos = client.pesquisa_preco.pesquisar("notebook i5")
    stats  = client.pesquisa_preco.estatisticas(precos)

    # Baixar documentos
    client.documentos.baixar_todos("12345678000195", 2026, 42)
"""
from __future__ import annotations

from .config import Config
from .http_client import PNCPHttpClient
from .api import (
    LicitacoesAPI,
    ContratosAPI,
    AtasAPI,
    PesquisaPrecoAPI,
    DocumentosAPI,
)
from .models import Licitacao, ItemCompra, Contrato, Ata, PrecoItem

__version__ = "1.0.0"
__all__ = [
    "PNCPClient",
    "PNCPHttpClient",
    "Config",
    "Licitacao",
    "ItemCompra",
    "Contrato",
    "Ata",
    "PrecoItem",
]


class PNCPClient:
    """
    Facade de alto nível para a API do PNCP.

    Agrega todos os módulos de acesso à API em um único objeto.
    Gerencia o ciclo de vida do cliente HTTP subjacente.

    Example::

        with PNCPClient() as client:
            licitacoes = client.licitacoes.buscar(uf="SP")
    """

    def __init__(
        self,
        use_cache: bool = True,
        timeout: int = Config.TIMEOUT,
    ) -> None:
        self._http = PNCPHttpClient(use_cache=use_cache, timeout=timeout)
        self.licitacoes = LicitacoesAPI(self._http)
        self.contratos = ContratosAPI(self._http)
        self.atas = AtasAPI(self._http)
        self.pesquisa_preco = PesquisaPrecoAPI(self._http)
        self.documentos = DocumentosAPI(self._http)

    def limpar_cache(self) -> None:
        """Invalida todo o cache de requisições em memória."""
        if self._http._cache:
            self._http._cache.clear()

    def close(self) -> None:
        """Fecha o cliente HTTP e libera recursos."""
        self._http.close()

    def __enter__(self) -> "PNCPClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
