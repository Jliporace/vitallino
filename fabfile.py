# -*- coding: utf-8 -*-
"""
############################################################
Kuarup - Fabric deployment
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/03/03  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2013, `GPL <http://is.gd/3Udt>__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "1.1 $Revision$"[10:-1]
__date__    = "2013/03/03 $Date$"

from fabric.api import local, settings, cd, run, lcd
KG_ORIGIN = '/home/carlo/Dropbox/Android/git/vitallino'
KG_DEST = '/home/carlo/Dropbox/Public/labase/kwarwp'
#KG_DEST = '/tmp/kwarwp'
SOURCES = '*.py'
KSOURCES = 'kuarup.py tchuk.py kuarupfest.py tkinter_factory.py'
KG_IMAGES = '/home/carlo/Dropbox/Android/git/vitallino/src/public/image'
PARTS = '/src/kwarwp.html /src/*.py /src/public/image/*.*'.split()
DESTS = '/src /src /src/public/image / /libs'.split()
def hello():
    print("Hello world!")


def ktest():
    local("nosetests")

def _do_copy(source,targ):
    local ("mkdir -p %s"%targ)
    local("cp -u %s -t %s"%(source,targ))

def _nk_copy():
    targ = KG_DEST+'/src'
    _do_copy(KSOURCES,targ)
    targ =  KG_DEST +'/src/public/image'
    _do_copy(KG_IMAGES,targ)

def _k_copy():
    for part, dest in zip(PARTS, DESTS):
        targ, source = KG_DEST + dest, KG_ORIGIN +part
        _do_copy(source, targ)

def kgdep():
    ktest()
    _k_copy()
    #kzip()
