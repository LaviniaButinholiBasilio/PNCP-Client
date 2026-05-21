"""
pncp_client/models/licitacao.py
Modelos Pydantic para licitações/compras e seus itens.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Licitacao(BaseModel):
    """Representa uma compra/licitação publicada no PNCP."""

    numero_controle_pncp: str = Field(..., description="Identificador único no PNCP")
    orgao_cnpj: str = Field(..., alias="orgaoEntidade", description="CNPJ do órgão")
    orgao_nome: str = Field(..., alias="unidadeOrgao", description="Nome do órgão")
    ano_compra: int = Field(..., alias="anoCompra")
    sequencial_compra: int = Field(..., alias="sequencialCompra")
    modalidade_nome: str = Field(default="", alias="modalidadeNome")
    situacao_compra_nome: str = Field(default="", alias="situacaoCompraNome")
    objeto_compra: str = Field(default="", alias="objetoCompra")
    valor_total_estimado: Optional[float] = Field(None, alias="valorTotalEstimado")
    data_publicacao_pncp: Optional[datetime] = Field(None, alias="dataPublicacaoPncp")
    data_abertura_proposta: Optional[datetime] = Field(None, alias="dataAberturaProposta")
    data_encerramento_proposta: Optional[datetime] = Field(None, alias="dataEncerramentoProposta")
    link_sistema_origem: Optional[str] = Field(None, alias="linkSistemaOrigem")
    uf: Optional[str] = Field(None, alias="uf")
    municipio_nome: Optional[str] = Field(None, alias="municipioNome")
    codigo_modalidade: Optional[int] = Field(None, alias="codigoModalidadeContratacao")

    model_config = {"populate_by_name": True, "extra": "ignore"}

    @field_validator("orgao_cnpj", mode="before")
    @classmethod
    def extrair_cnpj(cls, v: object) -> str:
        """Aceita tanto string direta quanto dict {cnpj: ...}."""
        if isinstance(v, dict):
            return str(v.get("cnpj", ""))
        return str(v)

    @field_validator("orgao_nome", mode="before")
    @classmethod
    def extrair_nome_orgao(cls, v: object) -> str:
        """Aceita tanto string direta quanto dict {nomeUnidade: ...}."""
        if isinstance(v, dict):
            return str(v.get("nomeUnidade", v.get("razaoSocial", "")))
        return str(v)


class ItemCompra(BaseModel):
    """Representa um item de uma compra/licitação."""

    numero_item: int = Field(..., alias="numeroItem")
    descricao: str = Field(default="", alias="descricao")
    quantidade: float = Field(default=0.0, alias="quantidade")
    unidade_medida: str = Field(default="", alias="unidadeMedida")
    valor_unitario_estimado: Optional[float] = Field(None, alias="valorUnitarioEstimado")
    valor_total: Optional[float] = Field(None, alias="valorTotal")
    material_ou_servico: str = Field("", alias="materialOuServico")
    codigo_item_catalogo: Optional[str] = Field(None, alias="codigoItemCatalogo")
    situacao_compra_item: Optional[str] = Field(None, alias="situacaoCompraItemNome")

    model_config = {"populate_by_name": True, "extra": "ignore"}
