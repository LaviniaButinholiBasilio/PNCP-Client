"""
pncp_client/models/preco.py
Modelo Pydantic para preços pesquisados via API de Pesquisa de Preços.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class PrecoItem(BaseModel):
    """Representa um preço praticado em compra pública."""

    descricao: str = Field("", alias="descricao")
    valor_unitario: float = Field(..., alias="valorUnitario")
    unidade_medida: str = Field("", alias="unidadeMedida")
    data_referencia: Optional[datetime] = Field(None, alias="dataReferencia")
    orgao_cnpj: str = Field("", alias="cnpjOrgao")
    orgao_nome: str = Field("", alias="nomeOrgao")
    numero_licitacao: str = Field("", alias="numeroLicitacao")
    municipio: Optional[str] = Field(None, alias="municipio")
    uf: Optional[str] = Field(None, alias="uf")
    codigo_item: Optional[str] = Field(None, alias="codigoItem")
    codigo_classe: Optional[str] = Field(None, alias="codigoClasse")

    model_config = {"populate_by_name": True, "extra": "ignore"}
