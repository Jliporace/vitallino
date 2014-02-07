#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Vitallino - Criador de Jogos Simplificado
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2014/02/07  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.3 $
:Home: `Labase http://labase.nce.ufrj.br/`__
:Copyright: 2011, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.3 $Revision$"[10:-1]
__date__    = "2014/02/07 $Date$"
"""
import sys


def _logger(*a):
    print(a)

logger = _logger


class NullSprite:
    def move(self, place, x, y):
        pass

    def __init__(self, *a):
        pass
DESAFIO = 'Tenho um desafio para você'
FALHOU = 'A sua tentativa falhou'

FALA = '''
<H1>Aprendendo a falar língua de cobra</H1>

Python é lingua de cobra. Nesta língua tudo vai acontencendo na hora em que se fala e não depois.
Os nomes vão sendo dados às coisas, mas depois estes mesmos nomes podem ser dados a coisas diferentes.
Os nomes são fortes e representam sempre aquilo que nomeiam.
Existem nomes que já foram dados a muitas coisas, mas outros você deve dar para tudo que criar.
Toda coisa é de um tipo que já existia, mas você pode criar novos tipos e novas coisas de todos os tipos.
Os nomes são diferentes se escritos com letras maiúsculas ou minúsculas.
Os espaços são muito importantes em toda a fala de Python.
Se a fala começa com um número diferente de espaços é porque não é a mesma fala, é uma outra.
'''
CODIGO = ''
SUCESSO = 'Você conseguiu superar o desafio'
TENTA = 'Esbarre em mim para tentar de novo'


class Tipada:
    def __init__(self, title=DESAFIO, talk=FALA, code=CODIGO, fail=FALHOU, success=SUCESSO):
        self.value = self.entry = self._response = self.dialog = None


class Ato:
    def _first_response(self, dialog):
        logger('first response %s %s %s' % (dialog, sys.stdout, sys.stderr))
        action = dialog.get_text()
        action += self.code
        logger('first response code %s' % action)
        self.value.value = ''
        sys_out, sys_err = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = self.value
        he = self.entry
        try:
            exec(action, locals())
            pass
            logger('first correct response: else %s' % self.plan[0][0])
            self.talk = dialog.get_text()
            #self.move(self.world.plan[0][0])
            self.speak(self.success)
            self._response = self._first_response
        except Exception as exc:
            logger('first response exception error %s %s' % (exc, self.value.value))
            #traceback.print_exc()
            self.talk = dialog.get_text()
            dialog.set_text(str(exc) + ' ' + self.value.value)
            self._response = self._second_response
            self.speak(self.fail)
            dialog.show()
        sys.stdout = sys_out
        sys.stderr = sys_err
        logger('first response value error %s' % self.value.value)

    def _second_response(self, dialog):
        self._response = self._first_response
        self.speak(self.retry)

    def response(self, dialog):
        self._response(dialog)

    def start(self, dialog, entry, speak, plan):
        self.entry, self.speak, self.plan = entry, speak, plan
        dialog(text=self.talk, act=self.response).show()

    def __init__(self,
                 title=DESAFIO, talk=FALA, code=CODIGO, fail=FALHOU, success=SUCESSO, retry=TENTA):

        class Capture_sysouterr:
            def __init__(self):
                self.value = ''

            def write(self, data):
                self.value += str(data)

        self.entry, self.speak, self.plan = [None] * 3
        self.title, self.talk, self.code, self.fail, self.success, self.retry = title, talk, code, fail, success, retry
        value = self.value = Capture_sysouterr()
        self._response = self._first_response
