"""
    Testa o objeto Arquivo responsável por carregar 
    e gerar arquivos de débito automático
"""

import codecs
import os

import pytest

from debito_automatico.layout import versao_06
from debito_automatico import errors
from debito_automatico.tipos import Arquivo
from tests.consts import ARQS_DIRPATH


RETORNO_PATH_BANCOOB = os.path.join(ARQS_DIRPATH, "bancoob_retorno_v6.cnv")
REMESSA_PATH_BANCOOB = os.path.join(ARQS_DIRPATH, "bancoob_remessa_v6.txt")


@pytest.mark.parametrize("input_file", [RETORNO_PATH_BANCOOB, REMESSA_PATH_BANCOOB])
def test_leitura_arquivo(input_file):
    """Verifica se ao carregar um arquivo, o objeto Arquivo também
    irá gerar um conteúdo igual ao que foi carregado

    Args:
        input_file (str): Path do arquivo de entrada para verificação
    """
    ret_file = codecs.open(input_file, encoding="utf8")
    arquivo = Arquivo(versao_06, arquivo=ret_file)

    ret_file.seek(0)
    content_file = ret_file.read()
    content_obj = str(arquivo)
    assert content_file == content_obj
    ret_file.close()


def test_arquivo_vazio():
    """Verifica se irá retornar um erro caso tente converter um
    objeto Arquivo em texto, estando ele vazio
    """
    arquivo = Arquivo(versao_06)
    with pytest.raises(errors.ArquivoVazioError):
        assert str(arquivo) == ""


@pytest.mark.parametrize("input_file", [RETORNO_PATH_BANCOOB, REMESSA_PATH_BANCOOB])
def test_num_linhas_arquivo(input_file):
    """Verifica se a quantidade de linhas do arquivo será igual a
    quantidade de linhas do objeto após carregamento do arquivo.

    Args:
        input_file (str): Path do arquivo de entrada para verificação
    """
    ret_file = codecs.open(input_file, encoding="utf8")
    arquivo = Arquivo(versao_06, arquivo=ret_file)

    ret_file.seek(0)
    total_lines = sum(1 for _ in ret_file)

    assert total_lines == arquivo.total_linhas
    ret_file.close()
