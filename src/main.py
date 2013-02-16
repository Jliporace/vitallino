"""
############################################################
Vitallino - Criador de Jogos Simplificado
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/02/09  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase http://labase.nce.ufrj.br/`__
:Copyright: 2011, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2013/02/09 $Date$"
"""
SIMPLE = ('..$$$&...'+'.'*10+('\n'+'.'*19)*12)
#p = [['%s%d%d'%(p,x,y) for x, p in enumerate(' %s '%row)] for y, row in enumerate(border)]
#ES,FS = NullSprite, Sprite


def main(pn, gui, spr = None, plan= SIMPLE):
    import builder
    builder = builder.Builder()
    return builder.build(pn, gui, builder.build_inventory(FS=spr), plan)

def web_main(pn, gui, spr = None, plan= SIMPLE):
    #from kwarwp_factory import Sprite
    builder = Builder()
    return builder.build(pn, gui, builder.build_inventory(FS = Sprite), plan)
