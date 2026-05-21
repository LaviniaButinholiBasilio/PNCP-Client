"""
pncp_client/api/atas.py
Endpoints de atas de registro de preços do PNCP.
"""
from __future__ import annotations

from typing import List, Optional

from ..http_client import PNCPHttpClient
from ..models.ata import Ata


class AtasAPI:
    """Acesso aos endpoints de atas de registro de preços."""

    def __init__(self, client: PNCPHttpClient) -> None:
        self._client = client

    def obter(self, cnpj: str, ano: int, sequencial: int) -> Ata:
        """
        Retorna os detalhes de uma ata específica.

        Args:
            cnpj: CNPJ do órgão (somente números).
            ano: Ano da ata.
            sequencial: Número sequencial da ata.
        """
        data = self._client.get(f"/orgaos/{cnpj}/atas/{ano}/{sequencial}")
        return Ata(**data)

    def listar_por_orgao(
        self,
        cnpj: str,
        ano: int,
        pagina: int = 1,
        tamanho_pagina: int = 20,
    ) -> List[Ata]:
        """
        Lista atas de um órgão em determinado ano.

        Args:
            cnpj: CNPJ do órgão (somente números).
            ano: Ano das atas.
        """
        params = {"pagina": pagina, "tamanhoPagina": tamanho_pagina}
        data = self._client.get(f"/orgaos/{cnpj}/atas/{ano}", params=params)
        return [Ata(**item) for item in data.get("data", [])]

    def buscar(
        self,
        cnpj: Optional[str] = None,
        cnpj_orgao: Optional[str] = None,
        ano: Optional[int] = None,
        uf: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        pagina: int = 1,
        tamanho_pagina: int = 20,
    ) -> List[Ata]:
        """
        Busca atas com filtros.

        Args:
            cnpj: Alias conveniente para cnpj_orgao.
            cnpj_orgao: CNPJ do órgão.
            ano: Ano das atas.
            uf: Sigla do estado.
            data_inicio: Data inicial (AAAA-MM-DD).
            data_fim: Data final (AAAA-MM-DD).
        """
        orgao = cnpj or cnpj_orgao
        params: dict = {
            k: v
            for k, v in {
                "cnpjOrgao": orgao,
                "ano": ano,
                "uf": uf,
                "dataInicial": data_inicio,
                "dataFinal": data_fim,
                "pagina": pagina,
                "tamanhoPagina": tamanho_pagina,
            }.items()
            if v is not None
        }
        data = self._client.get("/atas", params=params)
        return [Ata(**item) for item in data.get("data", [])]
