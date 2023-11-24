# # -*- coding: utf-8 -*-

import codecs
import os
from decimal import Decimal

import pytest
from debito_automatico import errors
from debito_automatico.layout import versao_06

from tests.consts import ARQS_DIRPATH

REMESSA_PATH_BANCOOB = os.path.join(ARQS_DIRPATH, "bancoob_remessa_v6.txt")


def test_leitura_campo_num_decimal():
    with codecs.open(REMESSA_PATH_BANCOOB, encoding="utf8") as ret_file:
        # Lê a primeira linha para pular o Registro A
        ret_file.readline()
        # Captura a segunda linha que é um Registro E
        reg_e_str = ret_file.readline().strip("\r\n")

        reg_e = versao_06.registros.RegistroE()
        reg_e.carregar(reg_e_str)

        assert reg_e.valor_debito, Decimal("12500.00")


def test_escrita_campo_num_decimal():
    reg_e = versao_06.registros.RegistroE()

    # aceitar somente tipo Decimal
    with pytest.raises(errors.NumDecimaisError):
        reg_e.valor_debito = "10.0"
    with pytest.raises(errors.TipoError):
        reg_e.valor_debito = ""

    # Testa se as casas decimais estão sendo verificadas
    with pytest.raises(errors.NumDecimaisError):
        reg_e.valor_debito = Decimal("100.2")
    with pytest.raises(errors.NumDecimaisError):
        reg_e.valor_debito = Decimal("1001")
    with pytest.raises(errors.NumDecimaisError):
        reg_e.valor_debito = Decimal("1.000")

    # Verifica se o numero de dígitos esta sendo verificado
    with pytest.raises(errors.NumDigitosExcedidoError):
        reg_e.valor_debito = Decimal("10000000008100.21")

    # Armazemamento correto de um decimal
    reg_e.valor_debito = Decimal("2.13")
    assert reg_e.valor_debito == Decimal("2.13")


def test_leitura_campo_num_int():
    with codecs.open(REMESSA_PATH_BANCOOB, encoding="utf8") as ret_file:
        # Lê a primeira linha - Registro A
        reg_a_str = ret_file.readline()
        reg_a = versao_06.registros.RegistroA()
        reg_a.carregar(reg_a_str)
        assert reg_a.codigo_banco == 756


def test_escrita_campo_num_int():
    with codecs.open(REMESSA_PATH_BANCOOB, encoding="utf8") as ret_file:
        # Lê a primeira linha - Registro A
        reg_a_str = ret_file.readline()
        reg_a = versao_06.registros.RegistroA()
        reg_a.carregar(reg_a_str)

    # Aceitar somente inteiros (int e long)
    with pytest.raises(errors.TipoError):
        reg_a.codigo_banco = "10.0"
    with pytest.raises(errors.TipoError):
        reg_a.codigo_banco = ""

    # Verifica se o numero de dígitos esta sendo verificado
    with pytest.raises(errors.NumDigitosExcedidoError):
        reg_a.codigo_banco = 12345678234567890234567890
    with pytest.raises(errors.NumDigitosExcedidoError):
        reg_a.codigo_banco = 1234

    # verifica valor armazenado
    reg_a.codigo_banco = 5
    assert reg_a.codigo_banco == 5


def test_leitura_campo_alfa():
    with codecs.open(REMESSA_PATH_BANCOOB, encoding="utf8") as ret_file:
        # Lê a primeira linha - Registro A
        reg_a_str = ret_file.readline()
        reg_a = versao_06.registros.RegistroA()
        reg_a.carregar(reg_a_str)

    assert reg_a.nome_banco == "SICOOB"


def test_escrita_campo_alfa():
    with codecs.open(REMESSA_PATH_BANCOOB, encoding="utf8") as ret_file:
        # Lê a primeira linha - Registro A
        reg_a_str = ret_file.readline()
        reg_a = versao_06.registros.RegistroA()
        reg_a.carregar(reg_a_str)

    # Testa que serão aceitos apenas unicode objects
    with pytest.raises(errors.TipoError):
        reg_a.nome_banco = "CAIXA".encode()

    # Testa que strings mais longas que obj.digitos nao serao aceitas
    with pytest.raises(errors.NumDigitosExcedidoError):
        reg_a.nome_banco = "123456789012345678901"

    # Testa que o valor atribuído foi guardado no objeto
    reg_a.nome_banco = "BB"
    assert reg_a.nome_banco == "BB"


def test_fromdict():
    with codecs.open(REMESSA_PATH_BANCOOB, encoding="utf8") as ret_file:
        # Lê a primeira linha - Registro A
        reg_a_str = ret_file.readline()
        reg_a = versao_06.registros.RegistroA()
        reg_a.carregar(reg_a_str)

    reg_a_dict = reg_a.todict()
    reg_a_arquivo = versao_06.registros.RegistroA(**reg_a_dict)
    assert reg_a_arquivo.nome_empresa == "LADDER TECNOLOGIA"
    assert reg_a_arquivo.nome_banco == "SICOOB"


def test_unicode():
    with codecs.open(REMESSA_PATH_BANCOOB, encoding="utf8") as ret_file:
        # Lê a primeira linha - Registro A
        reg_a_str = ret_file.readline().strip("\r\n")
        reg_a = versao_06.registros.RegistroA()
        reg_a.carregar(reg_a_str)

        reg_e_str = ret_file.readline().strip("\r\n")
        reg_e = versao_06.registros.RegistroE()
        reg_e.carregar(reg_e_str)

    def unicode_test(seg_instance, seg_str):
        seg_gen_str = str(seg_instance)

        assert len(seg_gen_str) == 150
        assert len(seg_str) == 150
        assert seg_gen_str == seg_str

    unicode_test(reg_a, reg_a_str)
    unicode_test(reg_e, reg_e_str)
