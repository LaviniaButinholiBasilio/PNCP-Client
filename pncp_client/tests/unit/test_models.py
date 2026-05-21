"""Testes unitários para os modelos Pydantic."""
import pytest
from datetime import datetime
from pncp_client.models import Licitacao, ItemCompra, Contrato, Ata, PrecoItem


# ---------------------------------------------------------------------------
# Fixtures com payloads simulando a resposta da API
# ---------------------------------------------------------------------------

PAYLOAD_LICITACAO = {
    "numero_controle_pncp": "12345678000195-1-000042/2026",
    "orgaoEntidade": {"cnpj": "12345678000195", "razaoSocial": "Ministério X"},
    "unidadeOrgao": {"nomeUnidade": "Secretaria Y"},
    "anoCompra": 2026,
    "sequencialCompra": 42,
    "modalidadeNome": "Pregão Eletrônico",
    "situacaoCompraNome": "Publicada",
    "objetoCompra": "Aquisição de notebooks",
    "valorTotalEstimado": 500000.00,
    "dataPublicacaoPncp": "2026-05-01T00:00:00",
    "dataAberturaProposta": "2026-05-10T09:00:00",
    "dataEncerramentoProposta": "2026-05-20T18:00:00",
    "linkSistemaOrigem": "https://comprasnet.gov.br/xxx",
    "uf": "SP",
}

PAYLOAD_ITEM = {
    "numeroItem": 1,
    "descricao": "Notebook Intel Core i5",
    "quantidade": 50.0,
    "unidadeMedida": "UN",
    "valorUnitarioEstimado": 4500.00,
    "valorTotal": 225000.00,
    "materialOuServico": "M",
    "codigoItemCatalogo": "2414.01",
}

PAYLOAD_PRECO = {
    "descricao": "Cadeira ergonômica",
    "valorUnitario": 850.00,
    "unidadeMedida": "UN",
    "dataReferencia": "2026-03-15T00:00:00",
    "cnpjOrgao": "99887766000111",
    "nomeOrgao": "Tribunal Z",
    "numeroLicitacao": "99887766000111-1-000010/2026",
    "municipio": "São Paulo",
    "uf": "SP",
}


class TestLicitacao:
    def test_parse_payload_completo(self):
        lic = Licitacao(**PAYLOAD_LICITACAO)
        assert lic.ano_compra == 2026
        assert lic.sequencial_compra == 42
        assert lic.valor_total_estimado == 500000.00
        assert lic.uf == "SP"

    def test_extrai_cnpj_de_dict(self):
        lic = Licitacao(**PAYLOAD_LICITACAO)
        assert lic.orgao_cnpj == "12345678000195"

    def test_extrai_nome_de_dict(self):
        lic = Licitacao(**PAYLOAD_LICITACAO)
        assert "Secretaria Y" in lic.orgao_nome

    def test_campos_opcionais_podem_ser_none(self):
        payload = {**PAYLOAD_LICITACAO}
        payload.pop("valorTotalEstimado")
        lic = Licitacao(**payload)
        assert lic.valor_total_estimado is None

    def test_ignora_campos_extras(self):
        payload = {**PAYLOAD_LICITACAO, "campoDesconhecido": "x"}
        lic = Licitacao(**payload)
        assert not hasattr(lic, "campoDesconhecido")


class TestItemCompra:
    def test_parse_basico(self):
        item = ItemCompra(**PAYLOAD_ITEM)
        assert item.numero_item == 1
        assert item.quantidade == 50.0
        assert item.material_ou_servico == "M"

    def test_valor_unitario_presente(self):
        item = ItemCompra(**PAYLOAD_ITEM)
        assert item.valor_unitario_estimado == 4500.00


class TestPrecoItem:
    def test_parse_basico(self):
        preco = PrecoItem(**PAYLOAD_PRECO)
        assert preco.valor_unitario == 850.00
        assert preco.uf == "SP"
        assert preco.municipio == "São Paulo"
