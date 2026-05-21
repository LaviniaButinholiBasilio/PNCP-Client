"""Testes unitários para pncp_client.utils.formatters."""
from datetime import datetime
import pytest
from pncp_client.utils.formatters import (
    formatar_cnpj,
    formatar_valor,
    formatar_data,
    truncar,
)


class TestFormatarCnpj:
    def test_cnpj_sem_formatacao(self):
        assert formatar_cnpj("11222333000181") == "11.222.333/0001-81"

    def test_cnpj_ja_formatado(self):
        assert formatar_cnpj("11.222.333/0001-81") == "11.222.333/0001-81"

    def test_cnpj_invalido_retorna_original(self):
        assert formatar_cnpj("123") == "123"


class TestFormatarValor:
    def test_valor_positivo(self):
        resultado = formatar_valor(1234567.89)
        assert "1.234.567" in resultado
        assert "89" in resultado

    def test_valor_none(self):
        assert formatar_valor(None) == "-"

    def test_valor_negativo(self):
        resultado = formatar_valor(-100.0)
        assert "-" in resultado

    def test_valor_zero(self):
        resultado = formatar_valor(0.0)
        assert "0" in resultado


class TestFormatarData:
    def test_data_valida(self):
        dt = datetime(2026, 5, 20, 10, 30)
        assert formatar_data(dt) == "20/05/2026"

    def test_data_none(self):
        assert formatar_data(None) == "-"

    def test_formato_customizado(self):
        dt = datetime(2026, 5, 20)
        assert formatar_data(dt, "%Y-%m-%d") == "2026-05-20"


class TestTruncar:
    def test_texto_curto_nao_trunca(self):
        assert truncar("abc", limite=10) == "abc"

    def test_texto_longo_trunca(self):
        resultado = truncar("a" * 100, limite=20)
        assert len(resultado) <= 20
        assert resultado.endswith("...")

    def test_limite_customizado(self):
        resultado = truncar("abcdefgh", limite=5, sufixo="…")
        assert len(resultado) <= 5
