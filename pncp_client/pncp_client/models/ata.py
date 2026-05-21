"""
pncp_client/models/ata.py
Modelo Pydantic para atas de registro de preços.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Ata(BaseModel):
    """Representa uma ata de registro de preços publicada no PNCP."""

    numero_controle_pncp: str = Field(..., alias="numeroControlePNCP")
    orgao_cnpj: str = Field(..., alias="orgaoEntidade")
    orgao_nome: str = Field("", alias="unidadeOrgao")
    numero_ata: str = Field("", alias="numeroAtaRegistroPreco")
    ano_ata: int = Field(..., alias="anoAta")
    sequencial_ata: int = Field(..., alias="sequencialAta")
    objeto_ata: str = Field("", alias="objetoAta")
    valor_global: Optional[float] = Field(None, alias="valorGlobal")
    data_vigencia_inicio: Optional[datetime] = Field(None, alias="dataVigenciaInicio")
    data_vigencia_fim: Optional[datetime] = Field(None, alias="dataVigenciaFim")
    data_assinatura: Optional[datetime] = Field(None, alias="dataAssinatura")
    situacao_nome: Optional[str] = Field(None, alias="situacaoAtaRegistroPrecoNome")

    model_config = {"populate_by_name": True, "extra": "ignore"}

    @field_validator("orgao_cnpj", mode="before")
    @classmethod
    def extrair_cnpj(cls, v: object) -> str:
        if isinstance(v, dict):
            return str(v.get("cnpj", ""))
        return str(v)

    @field_validator("orgao_nome", mode="before")
    @classmethod
    def extrair_nome(cls, v: object) -> str:
        if isinstance(v, dict):
            return str(v.get("nomeUnidade", ""))
        return str(v)
