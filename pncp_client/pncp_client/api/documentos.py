"""
pncp_client/api/documentos.py
Download e listagem de documentos vinculados a compras do PNCP.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional

from tqdm import tqdm

from ..http_client import PNCPHttpClient
from ..config import Config

logger = logging.getLogger(__name__)


class DocumentosAPI:
    """Acesso e download de documentos de compras no PNCP."""

    def __init__(
        self,
        client: PNCPHttpClient,
        diretorio_base: Optional[Path] = None,
    ) -> None:
        self._client = client
        self.diretorio_base = diretorio_base or Config.DOWNLOAD_DIR
        self.diretorio_base.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Listagem
    # ------------------------------------------------------------------

    def listar(self, cnpj: str, ano: int, sequencial: int) -> List[Dict]:
        """
        Lista os documentos disponíveis para uma compra.

        Returns:
            Lista de dicionários com os metadados dos documentos.
        """
        data = self._client.get(
            f"/orgaos/{cnpj}/compras/{ano}/{sequencial}/documentos"
        )
        return data.get("data", [])

    # ------------------------------------------------------------------
    # Download individual
    # ------------------------------------------------------------------

    def baixar(
        self,
        cnpj: str,
        ano: int,
        sequencial: int,
        id_arquivo: int,
        nome_arquivo: Optional[str] = None,
    ) -> str:
        """
        Baixa um arquivo específico de uma compra.

        Args:
            cnpj: CNPJ do órgão.
            ano: Ano da compra.
            sequencial: Sequencial da compra.
            id_arquivo: ID do arquivo a baixar.
            nome_arquivo: Nome para salvar (usa o do servidor se omitido).

        Returns:
            Caminho absoluto do arquivo salvo.
        """
        destino_dir = self.diretorio_base / cnpj / str(ano) / str(sequencial)
        destino_dir.mkdir(parents=True, exist_ok=True)

        # Tenta obter o nome do documento nos metadados, se não fornecido
        if nome_arquivo is None:
            docs = self.listar(cnpj, ano, sequencial)
            doc = next((d for d in docs if d.get("id") == id_arquivo), None)
            nome_arquivo = doc.get("nome", f"documento_{id_arquivo}.pdf") if doc else f"documento_{id_arquivo}.pdf"

        url = (
            f"{self._client.base_url}"
            f"/orgaos/{cnpj}/compras/{ano}/{sequencial}/arquivos/{id_arquivo}"
        )
        caminho = str(destino_dir / nome_arquivo)
        return self._client.download_file(url, caminho)

    # ------------------------------------------------------------------
    # Download em lote
    # ------------------------------------------------------------------

    def baixar_todos(
        self,
        cnpj: str,
        ano: int,
        sequencial: int,
        mostrar_progresso: bool = True,
    ) -> List[str]:
        """
        Baixa todos os documentos de uma compra.

        Args:
            mostrar_progresso: Exibe barra de progresso via tqdm.

        Returns:
            Lista de caminhos dos arquivos baixados com sucesso.
        """
        docs = self.listar(cnpj, ano, sequencial)
        if not docs:
            logger.warning("Nenhum documento encontrado para %s/%s/%s", cnpj, ano, sequencial)
            return []

        caminhos: List[str] = []
        iterador = tqdm(docs, desc="Baixando documentos", unit="arq") if mostrar_progresso else docs

        for doc in iterador:
            id_arquivo = doc.get("id")
            nome = doc.get("nome", f"doc_{id_arquivo}.pdf")
            if id_arquivo is None:
                continue
            try:
                caminho = self.baixar(cnpj, ano, sequencial, id_arquivo, nome)
                caminhos.append(caminho)
                logger.info("✓ %s salvo em %s", nome, caminho)
            except Exception as exc:
                logger.error("✗ Erro ao baixar %s: %s", nome, exc)

        return caminhos
