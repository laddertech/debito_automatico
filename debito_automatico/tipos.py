# -*- coding: utf-8 -*-

import codecs
from typing import Optional

from debito_automatico import errors


class Arquivo(object):
    def __init__(self, banco, **kwargs):
        """Arquivo Débito Automático."""

        self._registros = []
        self._total_linhas = 0
        self.banco = banco
        arquivo = kwargs.get("arquivo")

        if isinstance(arquivo, codecs.StreamReaderWriter):
            self.carregar_retorno(arquivo)
        else:
            self.header = self.banco.registros.RegistroA(**kwargs)
            self.trailer = self.banco.registros.RegistroZ(**kwargs)
            self.trailer.total_registros = 2
            self._total_linhas = 2

    def _carrega_registro(self, tipo: str, linha: Optional[str], **kwargs):
        match tipo:
            case "B": seg = self.banco.registros.RegistroB(**kwargs)
            case "C": seg = self.banco.registros.RegistroC(**kwargs)
            case "D": seg = self.banco.registros.RegistroD(**kwargs)
            case "E": seg = self.banco.registros.RegistroE(**kwargs)
            case "F": seg = self.banco.registros.RegistroF(**kwargs)
            case "H": seg = self.banco.registros.RegistroH(**kwargs)
            case "I": seg = self.banco.registros.RegistroI(**kwargs)
            case "J": seg = self.banco.registros.RegistroJ(**kwargs)
            case "K": seg = self.banco.registros.RegistroK(**kwargs)
            case "L": seg = self.banco.registros.RegistroL(**kwargs)
            case "T": seg = self.banco.registros.RegistroT(**kwargs)
            case "X": seg = self.banco.registros.RegistroX(**kwargs)
            case _: seg = None

        if seg is not None:
            if linha:
                seg.carregar(linha)
            self._registros.append(seg)
            # Incrementar numero de registros
            self._total_linhas += 1

    def carregar_retorno(self, arquivo):
        self._total_linhas = 0
        for linha in arquivo:
            tipo_registro = linha[0]

            if tipo_registro == "A":
                self.header = self.banco.registros.RegistroA()
                self.header.carregar(linha)
                self._total_linhas += 1
                
            self._carrega_registro(tipo=tipo_registro, linha=linha)

            if tipo_registro == "Z":
                self.trailer = self.banco.registros.RegistroZ()
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
        codigo_registro = kwargs.get("codigo_registro")
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
