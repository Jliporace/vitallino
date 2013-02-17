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
if '__package__' in dir():
    #from parts import Actor, Place
    #from elements import *
    pass
    
class NullSprite:
    def move(self, place,x,y):
        pass
    def __init__(self, *a):
        pass

class Builder:

    def build_actor(self, gui, place, x, y):
        #x, y = self.x, self.y
        door = place.plan[y][x]
        actor = Actor(gui.avatar(), door, x, y )
        place.actor = actor
        print( 'place,init xy %s actor %s door %s'%((x,y), actor, door))
        actor.move(door)
        #actor.place = door
        #actor.thing = door
        gui.handler(38, actor.go_forward)
        gui.handler(40, actor.go_backward)
        gui.handler(34, actor.go_pull)
        gui.handler(33, actor.go_push)
        gui.handler(35, actor.go_take)
        gui.handler(36, actor.go_give)

    def build_place(self,plan, gui, IV):
        def line(y, row, me):
            #x = ['%s%d%d'%(p,x,y) for x, p in enumerate(' %s '%row)]
            PART, ICON, IMGE  = 0, 1, 2
            #me = self.place
            x = [IV[p][PART](IV[p][ICON](gui, IV[p][IMGE],me,x,y),me,x,y)
                for x, p in enumerate(' %s '%row)]
            return x
        self.place = Place([])
        w = len(plan.split('\n')[0])
        border =[' '*w]
        border.extend(plan.split('\n'))
        border.extend([' '*w])
        self.plan = []
        for y,row in enumerate(border):
            self.plan += [line(y,row, self.place)]
            for x,cell in enumerate(self.plan[y]):
                cell.rebase(self.plan)
        ##print(self.plan)
        plan = self.plan
        self.place.plan = plan
        print ([(p[1],p[1].x) for p in plan])
        return self.place

    def build_land(self, gui):
        # Setup main scenario background
        image = gui.rect(x=10,y=10, width=780, height=580,style={'fill':'forestgreen'})
        image = gui.rect(x=100,y=100, width=600, height=400,style={'fill':'navajowhite'})
        legend = gui.text('Welcome to Kuarup!',x=350,y=45,
            font_size=20,text_anchor="middle",
            style={"stroke":"gold", 'fill':"gold"})

    def build(self, pn, gui, inventory, plan):
        # Setup main scenario
        self.build_land(gui)
        place = self.build_place(plan, gui, inventory)
        self.build_actor(gui, place, place.x, place.y)
        return place
    
    def build_inventory(self, FS = NullSprite):
        ES = NullSprite
        return {'.':[Way,ES,None], ' ': [Border,ES,None], '&':[Door,ES,None]
        , '@':[Tar,FS,'piche.gif'], '$':[Trunk,FS,'tronco.gif']}
    
