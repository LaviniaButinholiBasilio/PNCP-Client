"""
pncp_client/models/contrato.py
Modelo Pydantic para contratos celebrados.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Contrato(BaseModel):
    """Representa um contrato celebrado e publicado no PNCP."""

    numero_controle_pncp: str = Field(..., alias="numeroControlePNCP")
    orgao_cnpj: str = Field(..., alias="orgaoEntidade")
    orgao_nome: str = Field("", alias="unidadeOrgao")
    numero_contrato: str = Field("", alias="numeroContratoEmpenho")
    ano_contrato: int = Field(..., alias="anoContrato")
    sequencial_contrato: int = Field(..., alias="sequencialContrato")
    objeto_contrato: str = Field("", alias="objetoContrato")
    valor_inicial: Optional[float] = Field(None, alias="valorInicial")
    valor_global: Optional[float] = Field(None, alias="valorGlobal")
    data_vigencia_inicio: Optional[datetime] = Field(None, alias="dataVigenciaInicio")
    data_vigencia_fim: Optional[datetime] = Field(None, alias="dataVigenciaFim")
    data_assinatura: Optional[datetime] = Field(None, alias="dataAssinatura")
    razao_social_fornecedor: Optional[str] = Field(None, alias="nomeRazaoSocialFornecedor")
    cnpj_cpf_fornecedor: Optional[str] = Field(None, alias="cnpjCpfFornecedor")
    situacao_nome: Optional[str] = Field(None, alias="situacaoContrato")
    numero_licitacao_associada: Optional[str] = Field(None, alias="numeroProcedimentoContratacao")

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
