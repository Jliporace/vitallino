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
from jeppeto.pyjamas_factory import GUI

class TestPyjama(mocker.MockerTestCase):
  """Testes unitários para o Pyjamas"""

  def setUp(self):
    self.mock = Mocker()
    self.mc = self.mock.mock()
    self.app = GUI()
    self.app.canvas = self.mc
    self.app.build_event = self.mc
    self.app.build_drag = self.mc
    self.app.offset = (0,0)

  def tearDown(self):
    self.mock.restore()
    self.mock.verify()
    self.mock = None
    self.app = None
    pass

  def testa_cria_rect(self):
    "cria rect"
    expect(self.mc.rect(1,2,2,2)).result(self.mc)
    expect(self.mc.setAttrs(ANY))
    #self.mc.avatar = ANY
    self.mock.replay()
    self.app.rect(1,2,3,4)

  def testa_cria_img(self):
    "cria img"
    expect(self.mc.rect(1,2,3,4)).result(self.mc)
    expect(self.mc.setAttrs(ANY))
    #self.mc.avatar = ANY
    expect(self.mc.set()).result(self.mc)
    self.mc.add(ANY)
    self.mock.replay()
    self.app.image(None,1,2,3,4)
  def testa_cria_drag(self):
    "cria drag"
    mk= self.mc
    expect(self.mc(ANY,ANY)).result(self.mc)
    self.mc.get_avatar().drag(ARGS)
    mk.action
    mk.start
    mk.stop
    
    self.mock.replay()
    self.app.dragg(self.mc)

if __name__ == '__main__':
    import unittest
    unittest.main()