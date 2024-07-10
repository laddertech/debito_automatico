# -*- coding: utf-8 -*-

import codecs
from decimal import Decimal
from typing import Optional

from debito_automatico import errors


class Arquivo(object):
    def __init__(self, layout, **kwargs):
        """Arquivo Débito Automático."""

        self._registros = []
        self._total_linhas = 0
        self.layout = layout
        arquivo = kwargs.get("arquivo")

        if isinstance(arquivo, codecs.StreamReaderWriter):
            self.carregar_retorno(arquivo)
        else:
            self.header = self.layout.registros.RegistroA(**kwargs)
            self.trailer = self.layout.registros.RegistroZ(**kwargs)
            self.trailer.total_registros = 2
            self.trailer.valor_total = Decimal('0.00')
            self._total_linhas = 2

    def _carrega_registro(self, tipo: str, linha: Optional[str], **kwargs):
        seg_value = Decimal('0.00')
        match tipo:
            case "B": seg = self.layout.registros.RegistroB(**kwargs)
            case "C": seg = self.layout.registros.RegistroC(**kwargs)
            case "D": seg = self.layout.registros.RegistroD(**kwargs)
            case "E":
                seg = self.layout.registros.RegistroE(**kwargs)
                seg_value = seg.valor_debito
            case "F":
                seg = self.layout.registros.RegistroF(**kwargs)
                seg_value = seg.valor_original_ou_debitado
            case "H": seg = self.layout.registros.RegistroH(**kwargs)
            case "I": seg = self.layout.registros.RegistroI(**kwargs)
            case "J": seg = self.layout.registros.RegistroJ(**kwargs)
            case "K": seg = self.layout.registros.RegistroK(**kwargs)
            case "L": seg = self.layout.registros.RegistroL(**kwargs)
            case "T": seg = self.layout.registros.RegistroT(**kwargs)
            case "X": seg = self.layout.registros.RegistroX(**kwargs)
            case _: seg = None

        if seg is not None:
            if linha:
                seg.carregar(linha)
            self._registros.append(seg)
            # Incrementar numero de registros
            self._total_linhas += 1

            if hasattr(self, 'trailer'):
                self.trailer.total_registros = self._total_linhas
                self.trailer.valor_total += seg_value

    def carregar_retorno(self, arquivo):
        self._total_linhas = 0
        for linha in arquivo:
            tipo_registro = linha[0]

            if tipo_registro == "A":
                self.header = self.layout.registros.RegistroA()
                self.header.carregar(linha)
                self._total_linhas += 1

            self._carrega_registro(tipo=tipo_registro, linha=linha)

            if tipo_registro == "Z":
                self.trailer = self.layout.registros.RegistroZ()
                self.trailer.carregar(linha)
                self._total_linhas += 1
                self.trailer.total_registros = self._total_linhas

    @property
    def registros(self):
        return self._registros

    @property
    def total_linhas(self):
        return self._total_linhas

    def incluir_registro(self, **kwargs):
        codigo_registro = kwargs.get("codigo_registro", "")
        self._carrega_registro(tipo=codigo_registro, linha='', **kwargs)

    def escrever(self, file_):
        with open(file_, "wt", encoding="ascii") as file:
            file.write(str(self))

    def __str__(self):
        if not self._registros:
            raise errors.ArquivoVazioError()

        result = []
        result.append(str(self.header))
        result.extend(str(reg) for reg in self._registros)
        result.append(str(self.trailer))
        # Adicionar elemento vazio para arquivo terminar com \r\n
        result.append("")
        return "\r\n".join(result)
