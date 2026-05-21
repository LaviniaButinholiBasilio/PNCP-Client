"""
pncp_client/api/pesquisa_preco.py
Consulta de preços praticados em compras públicas.
"""
from __future__ import annotations

import statistics
from typing import Dict, List, Optional

from ..http_client import PNCPHttpClient
from ..models.preco import PrecoItem


class PesquisaPrecoAPI:
    """Acesso à API de pesquisa de preços do PNCP."""

    def __init__(self, client: PNCPHttpClient) -> None:
        self._client = client

    def pesquisar(
        self,
        descricao: str,
        uf: Optional[str] = None,
        codigo_item: Optional[str] = None,
        pagina: int = 1,
        tamanho_pagina: int = 50,
    ) -> List[PrecoItem]:
        """
        Pesquisa preços de itens praticados em compras públicas.

        Args:
            descricao: Descrição do item a pesquisar.
            uf: Filtrar por estado (sigla).
            codigo_item: Código do item no catálogo.
            pagina: Página atual (1-based).
            tamanho_pagina: Itens por página.

        Returns:
            Lista de :class:`PrecoItem` com preços encontrados.
        """
        params: dict = {
            k: v
            for k, v in {
                "descricao": descricao,
                "uf": uf,
                "codigoItem": codigo_item,
                "pagina": pagina,
                "tamanhoPagina": tamanho_pagina,
            }.items()
            if v is not None
        }
        data = self._client.get("/itens/preco", params=params, base="consulta")
        return [PrecoItem(**item) for item in data.get("data", [])]

    def pesquisar_todas_paginas(
        self,
        descricao: str,
        uf: Optional[str] = None,
        limite: int = 500,
    ) -> List[PrecoItem]:
        """
        Pesquisa percorrendo páginas automaticamente até *limite*.

        Args:
            limite: Número máximo total de registros a retornar.
        """
        resultados: List[PrecoItem] = []
        pagina = 1
        tamanho = 50

        while len(resultados) < limite:
            lote = self.pesquisar(
                descricao=descricao,
                uf=uf,
                pagina=pagina,
                tamanho_pagina=tamanho,
            )
            if not lote:
                break
            resultados.extend(lote)
            if len(lote) < tamanho:
                break
            pagina += 1

        return resultados[:limite]

    def estatisticas(self, precos: List[PrecoItem]) -> Dict[str, float | int]:
        """
        Calcula estatísticas descritivas a partir de uma lista de preços.

        Args:
            precos: Lista de :class:`PrecoItem`.

        Returns:
            Dicionário com ``minimo``, ``maximo``, ``media``, ``mediana``,
            ``desvio_padrao`` e ``total_amostras``.
        """
        valores = [p.valor_unitario for p in precos if p.valor_unitario > 0]
        if not valores:
            return {
                "minimo": 0.0,
                "maximo": 0.0,
                "media": 0.0,
                "mediana": 0.0,
                "desvio_padrao": 0.0,
                "total_amostras": 0,
            }

        return {
            "minimo": round(min(valores), 4),
            "maximo": round(max(valores), 4),
            "media": round(statistics.mean(valores), 4),
            "mediana": round(statistics.median(valores), 4),
            "desvio_padrao": round(statistics.stdev(valores), 4) if len(valores) > 1 else 0.0,
            "total_amostras": len(valores),
        }
