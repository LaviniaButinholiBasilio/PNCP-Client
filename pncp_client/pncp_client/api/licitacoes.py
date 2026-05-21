"""
pncp_client/api/licitacoes.py
Endpoints de licitações / compras do PNCP.
"""
from __future__ import annotations

from typing import List, Optional

from ..http_client import PNCPHttpClient
from ..models.licitacao import Licitacao, ItemCompra


class LicitacoesAPI:
    """Acesso aos endpoints de compras/licitações da API PNCP."""

    def __init__(self, client: PNCPHttpClient) -> None:
        self._client = client

    # ------------------------------------------------------------------
    # Busca / listagem
    # ------------------------------------------------------------------

    def buscar(
        self,
        cnpj_orgao: Optional[str] = None,
        modalidade: Optional[int] = None,
        uf: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        pagina: int = 1,
        tamanho_pagina: int = 20,
    ) -> List[Licitacao]:
        """
        Busca licitações com filtros opcionais.

        Args:
            cnpj_orgao: CNPJ do órgão (somente números).
            modalidade: Código da modalidade (ex: 6 = Pregão Eletrônico).
            uf: Sigla do estado (ex: "SP").
            data_inicio: Data inicial no formato AAAA-MM-DD.
            data_fim: Data final no formato AAAA-MM-DD.
            pagina: Número da página (1-based).
            tamanho_pagina: Itens por página (máx. 500).

        Returns:
            Lista de objetos :class:`Licitacao`.
        """
        params: dict = {
            k: v
            for k, v in {
                "cnpjOrgao": cnpj_orgao,
                "codigoModalidadeContratacao": modalidade,
                "uf": uf,
                "dataInicial": data_inicio,
                "dataFinal": data_fim,
                "pagina": pagina,
                "tamanhoPagina": tamanho_pagina,
            }.items()
            if v is not None
        }
        data = self._client.get("/compras/proposta", params=params)
        return [Licitacao(**item) for item in data.get("data", [])]

    # ------------------------------------------------------------------
    # Detalhe de uma compra específica
    # ------------------------------------------------------------------

    def obter(self, cnpj: str, ano: int, sequencial: int) -> Licitacao:
        """
        Retorna os detalhes de uma compra específica.

        Args:
            cnpj: CNPJ do órgão (somente números).
            ano: Ano da compra.
            sequencial: Número sequencial da compra.
        """
        data = self._client.get(f"/orgaos/{cnpj}/compras/{ano}/{sequencial}")
        return Licitacao(**data)

    # ------------------------------------------------------------------
    # Itens de uma compra
    # ------------------------------------------------------------------

    def listar_itens(
        self,
        cnpj: str,
        ano: int,
        sequencial: int,
        pagina: int = 1,
        tamanho_pagina: int = 100,
    ) -> List[ItemCompra]:
        """
        Lista os itens de uma compra.

        Returns:
            Lista de objetos :class:`ItemCompra`.
        """
        params = {"pagina": pagina, "tamanhoPagina": tamanho_pagina}
        data = self._client.get(
            f"/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens",
            params=params,
        )
        return [ItemCompra(**item) for item in data.get("data", [])]

    # ------------------------------------------------------------------
    # Paginação automática (helper)
    # ------------------------------------------------------------------

    def buscar_todos(
        self,
        cnpj_orgao: Optional[str] = None,
        modalidade: Optional[int] = None,
        uf: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        limite: int = 200,
    ) -> List[Licitacao]:
        """
        Busca licitações percorrendo páginas automaticamente até *limite*.

        Args:
            limite: Número máximo total de registros a retornar.
        """
        resultados: List[Licitacao] = []
        pagina = 1
        tamanho = 20

        while len(resultados) < limite:
            lote = self.buscar(
                cnpj_orgao=cnpj_orgao,
                modalidade=modalidade,
                uf=uf,
                data_inicio=data_inicio,
                data_fim=data_fim,
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
