#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pygame Factory : Gui interface to pygame
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2011/07/31  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2011/07/31 $Date$"

        
import mocker
from mocker import Mocker,KWARGS, ARGS, ANY, CONTAINS, MATCH, expect
from kwarwp import Place,Way,Border,Door,Tar,Trunk

class TestPyjama(mocker.MockerTestCase):
  """Testes unitários para o Pyjamas"""
  def __list(self):
        INVENTORY = {'.':Way, ' ': Border, '&':Door, '@':Tar, '%':Border}
        ES =FS = self.mg       
        INVENTORY = {'.':[Way,ES,None], ' ': [Border,ES,None], '&':[Door,ES,None]
            , '@':[Tar,FS,'piche.gif'], '%':[Trunk,FS,'tronco.gif']}
        return INVENTORY

  def setUp(self):
    self.mock_gui = Mocker()
    self.mock_avt = Mocker()
    self.mg = self.mock_gui.mock()
    self.ma = self.mock_gui.mock()

  def tearDown(self):
    self.mock_gui.restore()
    self.mock_avt.restore()
    self.mock_avt.verify()
    self.mock_avt = None
    self.app = None
    pass

  def _testa_cria_place(self):
    "create place"
    expect(self.mc.avatar()).result(self.mc)
    expect(self.mc.handler(ARGS)).count(1,6)
    expect(self.mc.move(ARGS))
    self.mock.replay()
    self.app = Place(self.mc, self.__list(), '.&.')

  def testa_move_forward(self):
    "move forward"
    expect(self.mg.avatar()).result(self.ma)
    expect(self.mg.handler(ARGS)).count(1,6)
    expect(self.ma.move(ARGS))
    expect(self.mg(ARGS)).count(1,96)
    self.mock_gui.replay()
    self.app = Place(self.mg, self.__list(), '.%&')
    self.mock_gui.restore()
    self.mock_avt.restore()
    #expect(self.ma.get_direction()).result(1)
    #expect(self.ma.get_direction()).result(1)
    #expect(self.ma.move(ARGS))
    #self.mock_avt.replay()
    #self.app.actor.go_forward()
    


if __name__ == '__main__':
    import unittest
    unittest.main()