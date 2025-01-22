"""Módulo com as funções para extração, transformação e carregamento.

Funções disponíveis:
- extrair_dados: Extrai dados de arquivos JSON em um diretório e os combina
  em um DataFrame.
- calcular_total_vendas: Calcula o total de vendas multiplicando quantidade
  e valor de venda.
- carregar_dados: Salva os dados processados em formatos CSV e/ou Parquet.
"""

import glob
import os
from typing import List

import pandas as pd


def extrair_dados(pasta: str) -> pd.DataFrame:
    """Extrai e combina dados de arquivos JSON em um diretório.

    Parameters
    ----------
    pasta : str
        Caminho do diretório contendo os arquivos JSON.

    Returns
    -------
    pd.DataFrame
        DataFrame contendo os dados extraídos de todos os arquivos JSON encontrados
        no diretório.
    """
    arquivos_json: List[str] = glob.glob(os.path.join(pasta, "*.json"))
    df_list: List[pd.DataFrame] = [pd.read_json(arquivo) for arquivo in arquivos_json]
    df_total: pd.DataFrame = pd.concat(df_list, ignore_index=False)
    return df_total


def calcular_total_vendas(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula o total de vendas para cada linha do DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame contendo as colunas "Quantidade" e "Venda".

    Returns
    -------
    pd.DataFrame
        DataFrame atualizado com uma nova coluna "Total", que é oproduto das colunas
        "Quantidade" e "Venda".
    """
    df["Total"] = df["Quantidade"] * df["Venda"]
    return df


def carregar_dados(dados_processados: pd.DataFrame, formatos: List[str]) -> None:
    """Salva os dados processados em arquivos nos formatos especificados.

    Parameters
    ----------
    dados_processados : pd.DataFrame
        DataFrame contendo os dados processados para exportação.
    formatos : list of str
        Lista de formatos para salvar os dados. Suporta "csv" e "parquet".

    Raises
    ------
    TypeError
        Se nenhum dos formatos especificados for reconhecido.
    """
    arquivos_gerados: int = 0
    for formato in formatos:
        if formato.lower() == "csv":
            dados_processados.to_csv("dados_processados.csv")
            arquivos_gerados += 1
        elif formato.lower() == "parquet":
            dados_processados.to_parquet("dados_processados.parquet")
            arquivos_gerados += 1

    if arquivos_gerados == 0:
        raise TypeError("Tipos de arquivos de saída não encontrados.")


if __name__ == "__main__":
    pasta = "data"
    dados_extraido = extrair_dados(pasta)
    dados_transformados = calcular_total_vendas(dados_extraido)
    carregar_dados(dados_transformados, ["csv"])
