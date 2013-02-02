#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pygame Factory : Gui interface to pygame
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/02/02  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2011, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2013/02/02 $Date$"

        
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

  def _expect_all_place(self):
    "place expectations"
    expect(self.mg.avatar()).result(self.ma)
    expect(self.mg.handler(ARGS)).count(1,6)
    expect(self.ma.move(ARGS))
    expect(self.mg(ARGS)).count(1,96)
  def _replay_and_create_place(self):
    "create place"
    self.mock_gui.replay()
    self.app = Place(self.mg, self.__list(), '.&.')
  def testa_cria_place(self):
    "create place"
    self._expect_all_place()
    self._replay_and_create_place()

  def testa_move_forward(self):
    "move forward"
    self._expect_all_place()
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    self._replay_and_create_place()
    B, A = 2,3
    assert isinstance(self.app.plan[1][B].thing, Place),self.app.plan[1][B].thing
    self.app.actor.go_forward()
    assert self.app.actor.x == 3,self.app.actor.x
    assert isinstance(self.app.plan[1][B], Door),self.app.plan[1][B]
    assert isinstance(self.app.plan[1][B].thing, Place),self.app.plan[1][B].thing
    assert self.app.plan[1][A].thing == self.app.actor,self.app.plan[1][A].thing 
    assert isinstance(self.app.plan[1][A].thing.thing, Way),self.app.plan[1][A].thing.thing
    
  def testa_move_forward_and_back(self):
    "move forward"
    self._expect_all_place()
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    expect(self.ma.get_direction()).result(1)
    expect(self.ma.move(ARGS))
    self._replay_and_create_place()
    B, A = 3,2
    assert isinstance(self.app.plan[1][2].thing, Place),self.app.plan[1][B].thing
    self.app.actor.go_forward()
    assert self.app.actor.x == B,self.app.actor.x
    self.app.actor.go_backward()
    assert self.app.actor.x == A,self.app.actor.x
    assert isinstance(self.app.plan[1][B], Way),self.app.plan[1][B]
    assert isinstance(self.app.plan[1][B].thing, Place),self.app.plan[1][B].thing
    assert isinstance(self.app.plan[1][A], Door),self.app.plan[1][A].thing.thing
    assert self.app.plan[1][A].thing == self.app.actor,self.app.plan[1][A].thing 
    assert isinstance(self.app.plan[1][A].thing.thing, Door),self.app.plan[1][A].thing.thing
    


if __name__ == '__main__':
    import unittest
    unittest.main()