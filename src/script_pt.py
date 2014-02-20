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
from parts import Actor


def _logger(*a):
    print(a)

logger = _logger
WIND = [(0, -1), (1, 0), (0, 1), (-1, 0)]


class Protagonist(Actor):
    def _look(self, a=0):
        x, y = self.place.get_position()
        x, y = self.get_position()
        dx, dy = WIND[self.get_direction()]

        print('thing %s x %d y %d, dx %d dy %d' % (self.place.place, x, y, dx, dy))
        ahead = self.place.place.get_next(self, self)
        #print('ahead %s avatar %s avatar%s' % (ahead, ahead))
        print(self.place.place.plan[8][1].name, ahead)
        self.talk(ahead.name)
        return ahead.name

    def va_adiante(self, a=0):
        self.stepper.run_command(self._forward)

    def va_de_re(self, a=0):
        self.stepper.run_command(self._backward)

    def vire_direita(self, a=0):
        self.stepper.run_command(self._right)

    def vire_esquerda(self, a=0):
        self.stepper.run_command(self._left)

    def pegue(self, a=0):
        self.stepper.run_command(self._take)

    def devolva(self, a=0):
        self.stepper.run_command(self._give)

    def puxe(self, a=0):
        self.stepper.run_command(self._pull)

    def empurre(self, a=0):
        self.stepper.run_command(self._push)

    def olhe(self, a=0):
        self.stepper.run_command(self._look)


class NullSprite:
    def move(self, place, x, y):
        pass

    def __init__(self, *a):
        pass
DESAFIO = 'Tenho um desafio para você'

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
FALHOU = 'Algo deu errado em sua tentativa'
TENTA = 'Esbarre em mim para tentar de novo'


class Ato:
    def _zero_response(self, dialog):
        logger('zero response')
        dialog.set_text(self.code)
        self._response = self._first_response
        dialog.show()

    def _first_response(self, dialog):
        logger('first response %s %s %s' % (dialog, sys.stdout, sys.stderr))
        action = dialog.get_text()
        action += self.test
        logger('first response code %s' % action)
        self.value.value = ''
        sys_out, sys_err = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = self.value
        try:
            kaio = self.entry
            kaio.olhe()
            #exec(action, locals())
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

    def start(self, dialog, entry, world):
        self.entry, self.speak, self.plan = entry, world.talk, world.plan
        self.speak(self.title)
        dialog(text=self.talk, act=self.response).show()

    def __init__(self,
                 title=DESAFIO, talk=FALA, code=CODIGO, test=CODIGO, fail=FALHOU, success=SUCESSO, retry=TENTA):

        class Capture_sysouterr:
            def __init__(self):
                self.value = ''

            def write(self, data):
                self.value += str(data)

        self.entry, self.speak, self.plan = [None] * 3
        self.title, self.talk, self.code, self.test = title, talk, code, test
        self.fail, self.success, self.retry = fail, success, retry
        value = self.value = Capture_sysouterr()
        self._response = self._zero_response


STORY = [
    Ato("Nomes para Tudo","""
Em lingua de cobra tudo tem o seu nome.
    """,'''
"""
Neste encantamento o Pajé vai usar estes nomes para escolher
a tarefa do índio e quantas vezes ela vai ser feita.
Para a palavra use tronco, pedra ou bicho e para o
numero, quantas vezes o índio vai fazer.
"""
nome_de_palavra = "tronco"
nome_de_numero = 1
    ''',
'''
por_onde = list('1000')
for vez in range(nome_de_numero):
    while kaio.olhe() != nome_de_palavra:
        kaio.vire_direita()
        por_onde = [por_onde.pop(-1)] + por_onde
''')
]