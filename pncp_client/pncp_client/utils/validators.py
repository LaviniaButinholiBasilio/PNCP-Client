"""
pncp_client/utils/validators.py
Validação de CNPJ, CPF e datas.
"""
from __future__ import annotations

import re
from datetime import datetime


def limpar_cnpj(cnpj: str) -> str:
    """Remove pontuação de um CNPJ e retorna apenas os dígitos."""
    return re.sub(r"\D", "", cnpj)


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida um CNPJ usando o algoritmo oficial da Receita Federal.

    Args:
        cnpj: CNPJ com ou sem formatação.

    Returns:
        ``True`` se o CNPJ for válido.
    """
    cnpj = limpar_cnpj(cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj: str, pesos: list[int]) -> int:
        soma = sum(int(d) * p for d, p in zip(cnpj, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1

    d1 = calcular_digito(cnpj[:12], pesos1)
    d2 = calcular_digito(cnpj[:13], pesos2)
    return cnpj[-2:] == f"{d1}{d2}"


def validar_data(data: str, fmt: str = "%Y-%m-%d") -> bool:
    """
    Valida se *data* está no formato esperado.

    Args:
        data: String de data.
        fmt: Formato esperado (padrão ISO 8601).

    Returns:
        ``True`` se válida.
    """
    try:
        datetime.strptime(data, fmt)
        return True
    except ValueError:
        return False


def validar_uf(uf: str) -> bool:
    """Verifica se a UF informada é um estado brasileiro válido."""
    ufs_validas = {
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
        "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
        "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
    }
    return uf.upper() in ufs_validas
