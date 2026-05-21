"""Testes unitários para PesquisaPrecoAPI e estatísticas."""
import pytest
from unittest.mock import MagicMock
from pncp_client.api.pesquisa_preco import PesquisaPrecoAPI
from pncp_client.models.preco import PrecoItem


def _make_preco(valor: float) -> PrecoItem:
    return PrecoItem(
        descricao="item",
        valorUnitario=valor,
        unidadeMedida="UN",
        cnpjOrgao="00000000000000",
        nomeOrgao="Órgão X",
        numeroLicitacao="XXX",
    )


class TestEstatisticas:
    def setup_method(self):
        mock_client = MagicMock()
        self.api = PesquisaPrecoAPI(mock_client)

    def test_lista_vazia(self):
        stats = self.api.estatisticas([])
        assert stats["total_amostras"] == 0

    def test_calcula_media(self):
        precos = [_make_preco(v) for v in [100.0, 200.0, 300.0]]
        stats = self.api.estatisticas(precos)
        assert stats["media"] == 200.0

    def test_calcula_mediana_impar(self):
        precos = [_make_preco(v) for v in [10.0, 20.0, 30.0]]
        stats = self.api.estatisticas(precos)
        assert stats["mediana"] == 20.0

    def test_calcula_minimo_maximo(self):
        precos = [_make_preco(v) for v in [5.0, 50.0, 15.0]]
        stats = self.api.estatisticas(precos)
        assert stats["minimo"] == 5.0
        assert stats["maximo"] == 50.0

    def test_ignora_valores_zero(self):
        precos = [_make_preco(v) for v in [0.0, 100.0, 200.0]]
        stats = self.api.estatisticas(precos)
        assert stats["total_amostras"] == 2  # 0.0 excluído

    def test_desvio_padrao_amostra_unica_e_zero(self):
        precos = [_make_preco(42.0)]
        stats = self.api.estatisticas(precos)
        assert stats["desvio_padrao"] == 0.0
