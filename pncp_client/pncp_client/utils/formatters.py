"""
pncp_client/utils/formatters.py
Formatação de CNPJ, datas e valores monetários.
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Optional


def formatar_cnpj(cnpj: str) -> str:
    """
    Formata um CNPJ no padrão XX.XXX.XXX/XXXX-XX.

    Args:
        cnpj: CNPJ com ou sem formatação.

    Returns:
        CNPJ formatado ou a string original se inválida.
    """
    numeros = re.sub(r"\D", "", cnpj)
    if len(numeros) != 14:
        return cnpj
    return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"


def formatar_valor(valor: Optional[float], simbolo: str = "R$") -> str:
    """
    Formata um valor monetário no padrão brasileiro.

    Args:
        valor: Valor numérico.
        simbolo: Símbolo da moeda (padrão ``"R$"``).

    Returns:
        String formatada como ``"R$ 1.234.567,89"`` ou ``"-"`` se None.
    """
    if valor is None:
        return "-"
    # Formata com separadores brasileiros
    inteiros, decimais = f"{abs(valor):,.2f}".split(".")
    inteiros = inteiros.replace(",", ".")
    sinal = "-" if valor < 0 else ""
    return f"{sinal}{simbolo} {inteiros},{decimais}"


def formatar_data(data: Optional[datetime], fmt: str = "%d/%m/%Y") -> str:
    """
    Formata uma data/datetime para exibição.

    Args:
        data: Objeto datetime (ou None).
        fmt: Formato de saída (padrão ``"%d/%m/%Y"``).

    Returns:
        Data formatada ou ``"-"`` se None.
    """
    if data is None:
        return "-"
    return data.strftime(fmt)


def formatar_data_hora(data: Optional[datetime]) -> str:
    """Formata data e hora no padrão brasileiro."""
    return formatar_data(data, "%d/%m/%Y %H:%M")


def truncar(texto: str, limite: int = 60, sufixo: str = "...") -> str:
    """
    Trunca *texto* em *limite* caracteres, acrescentando *sufixo*.

    Args:
        texto: Texto a truncar.
        limite: Comprimento máximo (incluindo sufixo).
        sufixo: Sufixo para indicar truncamento.

    Returns:
        Texto possivelmente truncado.
    """
    if len(texto) <= limite:
        return texto
    return texto[: limite - len(sufixo)] + sufixo
