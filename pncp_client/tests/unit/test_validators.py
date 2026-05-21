"""Testes unitários para pncp_client.utils.validators."""
import pytest
from pncp_client.utils.validators import (
    limpar_cnpj,
    validar_cnpj,
    validar_data,
    validar_uf,
)


class TestLimparCnpj:
    def test_remove_pontuacao(self):
        assert limpar_cnpj("11.222.333/0001-81") == "11222333000181"

    def test_ja_limpo(self):
        assert limpar_cnpj("11222333000181") == "11222333000181"


class TestValidarCnpj:
    # CNPJs válidos reais (fictícios mas com dígitos corretos)
    def test_cnpj_valido_sem_formatacao(self):
        assert validar_cnpj("11222333000181") is True

    def test_cnpj_valido_com_formatacao(self):
        assert validar_cnpj("11.222.333/0001-81") is True

    def test_cnpj_invalido_digitos_errados(self):
        assert validar_cnpj("11111111111111") is False

    def test_cnpj_curto(self):
        assert validar_cnpj("1234") is False

    def test_cnpj_todos_iguais(self):
        assert validar_cnpj("00000000000000") is False


class TestValidarData:
    def test_data_valida(self):
        assert validar_data("2026-05-20") is True

    def test_data_invalida_formato(self):
        assert validar_data("20/05/2026") is False

    def test_data_inexistente(self):
        assert validar_data("2026-02-30") is False

    def test_formato_customizado(self):
        assert validar_data("20/05/2026", "%d/%m/%Y") is True


class TestValidarUf:
    def test_uf_valida(self):
        assert validar_uf("SP") is True
        assert validar_uf("rj") is True  # case insensitive

    def test_uf_invalida(self):
        assert validar_uf("XX") is False
        assert validar_uf("Brasil") is False
