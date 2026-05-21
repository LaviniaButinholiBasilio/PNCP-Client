"""
pncp_client/api/contratos.py
Endpoints de contratos do PNCP.
"""
from __future__ import annotations

from typing import List, Optional

from ..http_client import PNCPHttpClient
from ..models.contrato import Contrato


class ContratosAPI:
    """Acesso aos endpoints de contratos da API PNCP."""

    def __init__(self, client: PNCPHttpClient) -> None:
        self._client = client

    def obter(self, cnpj: str, ano: int, sequencial: int) -> Contrato:
        """
        Retorna os detalhes de um contrato específico.

        Args:
            cnpj: CNPJ do órgão (somente números).
            ano: Ano do contrato.
            sequencial: Número sequencial do contrato.
        """
        data = self._client.get(f"/orgaos/{cnpj}/contratos/{ano}/{sequencial}")
        return Contrato(**data)

    def listar_por_orgao(
        self,
        cnpj: str,
        ano: int,
        pagina: int = 1,
        tamanho_pagina: int = 20,
    ) -> List[Contrato]:
        """
        Lista contratos de um órgão em determinado ano.

        Args:
            cnpj: CNPJ do órgão (somente números).
            ano: Ano dos contratos.
            pagina: Página atual (1-based).
            tamanho_pagina: Itens por página.
        """
        params = {"pagina": pagina, "tamanhoPagina": tamanho_pagina}
        data = self._client.get(f"/orgaos/{cnpj}/contratos/{ano}", params=params)
        return [Contrato(**item) for item in data.get("data", [])]

    def buscar(
        self,
        cnpj: Optional[str] = None,
        cnpj_orgao: Optional[str] = None,
        ano: Optional[int] = None,
        cnpj_fornecedor: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        pagina: int = 1,
        tamanho_pagina: int = 20,
    ) -> List[Contrato]:
        """
        Busca contratos com filtros.

        Args:
            cnpj: Alias conveniente para cnpj_orgao.
            cnpj_orgao: CNPJ do órgão contratante.
            ano: Ano dos contratos.
            cnpj_fornecedor: CNPJ do fornecedor/contratado.
            data_inicio: Data inicial (AAAA-MM-DD).
            data_fim: Data final (AAAA-MM-DD).
        """
        orgao = cnpj or cnpj_orgao
        params: dict = {
            k: v
            for k, v in {
                "cnpjOrgao": orgao,
                "ano": ano,
                "cnpjFornecedor": cnpj_fornecedor,
                "dataInicial": data_inicio,
                "dataFinal": data_fim,
                "pagina": pagina,
                "tamanhoPagina": tamanho_pagina,
            }.items()
            if v is not None
        }
        data = self._client.get("/contratos", params=params)
        return [Contrato(**item) for item in data.get("data", [])]
