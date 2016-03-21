#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Vittolino
# Copyright 2011-2016 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# Vittolino é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>


"""
############################################################
Vittolino - Classes básicas de Jogo e Interface Gráfica
############################################################
Configurador de conteúdo e API gráfica.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
from invariant import NOCODE, NODOC, NOMAP, DEFAULT_GUI, DEFAUlT_GAME


class GamePlay:
    """
    Define a configuração de uma fase ou nível do jogo.

    :param level_map: Mapa textual que posiciona os artefatos
    :param level_instruction: Documentação da tarefa da fase
    :param level_code: Código exemplo da fase
    """
    def __init__(self, level_map=NOMAP, level_instruction=NODOC, level_code=NOCODE):
        self.level_code = level_code
        self.level_instruction = level_instruction
        self.level_map = level_map


class GenericGUI:
    """
    Representa um game configurado pelo *game_content* a ser renderizado no *user_interface*.

    :param game_content: Uma instância de uma classe que herda de Game_Play
    :param user_interface: Uma instância de uma classe que herda de Generic_GUI
    """
    def __init__(self, game_content=DEFAUlT_GAME, user_interface=DEFAULT_GUI):
        self.game_content = game_content
        self.user_interface = user_interface
