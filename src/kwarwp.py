"""
############################################################
Vitallino - Criador de Jogos Simplificado
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/01/09  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.1 $
:Home: `Labase http://labase.nce.ufrj.br/`__
:Copyright: ©2011, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2013/01/09 $Date$"
"""
REPO = 'public/image/%s'
WIND=[(0,-1),(1,0),(0,1),(-1,0)]
NN,EE,SS,WW = WIND

def inherit(base, child):
    overriden, inherited = dir(child), dir(base)
    for member in inherited:
        if member not in overriden:
            setattr(child, member, getattr(base,member))
    return base

#class Entrance:
#    def __init__(self, place, x, y):
#        self.thing, self.x, self.y, self.m = place, x, y, str(self.__class__)

class Way:
    def __init__(self, avatar, place, x, y, **kw):
        #inherit(Entrance(place, x, y),self)
        self.avatar,self.place = avatar, place
        self.thing, self.x, self.y, self.m = place, x, y, str(self.__class__)
        #self.push = self.leave
    def _move(self, x, y, entry):
        self.thing = entry
        print( '%s.move, position %d %d thing %s'%(self.m, x, y, self.thing))
        self._action( self.x, self.y, self)
    def enter(self,entry, action=noop, position=None):
        self._action, thing, x, y = action, self.thing, self.x,self.y
        pos= (x, y)
        if position != None:
            position = pos
        print( '%s.enter,thing %s entry %s position %s'%(self.m, thing, entry, position))
        thing.enter(entry, action=self._move, position = position)
    def get_position(self,x=0,y=0):
        return self.place.get_position(x=x,y=y)
    def _left(self, x, y , entry):
        self.thing = self.place
        self._leaver( x, y, self.locus)
    def _support(self):
        self.place = Way(None,self.place, self.x, self.y)
    def leave(self,entry, action, reverse =0):
        self._leaver = action
        locus = self.place.get_next(entry,reverse =reverse)
        self.locus = locus
        print( '%s.leave locus %s lpos %d %d'%(self.m, locus, locus.x,locus.y))
        locus.enter(entry, action = self._left, position =(locus.x,locus.y))
    def push(self,entry, action, reverse =0):
        print( '%s.pushway locus %s lpos %d %d'%(self.m, entry, entry.x,entry.y))
        self.leave(entry, action, reverse =reverse)

class Tar:
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Way(avatar, place, x, y),self)
    def leave(self,thing, action=noop, reverse =0):
        print('Youre STUCK!!!')
        pass

class Door:
    def __init__(self, avatar, place, x, y, **kw):
        self.m = str(self.__class__)
        inherit(Way(avatar, place, x, y),self)
        place.x, place.y =  x, y

class Trunk:
    def get_direction(self):
        return self.locus.get_direction()
    def get_position(self):
        return (self.x, self.y)
    def move(self, x, y, entry= None):
        self.x, self.y = x, y
        self.thing = entry or self.thing
        ##print( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.thing.get_position(x=x, y=y)
        print( 'actor,move, position %d %d  entry%s real %d %d'%(x, y, entry, mx, my))
        avatar.move(mx, my)
    def _pushed(self, x, y , entry):
        #self.thing = self.place
        self._pusher( x, y, self.locus)
    def enter(self,entry, action=noop, position=None):
        print('It is HEAVY!!')
    def push(self,entry, action, reverse =0):
        print('It iiiiiiiiiiis HEAVY!!')
        #print( '%s.pushtrunk locus %s lpos %d %d'%(self.m, entry, entry.x,entry.y))
        #self.locus = entry
        #self._pusher = action
        #self.thing.push(self, self._pushed, reverse =reverse)
    def __init__(self, avatar, place, x, y, **kw):
        baser = inherit(Way(avatar, place, x, y),self)
        self.thing, self.x, self.y, self.m = place, x, y, str(self.__class__)
        self.place = Way(None,place, self.x, self.y)
        #self.push = self._push

class Border:
    def enter(self,entry, action=noop, position=None):
        print('Cant go this way!!')
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Way(avatar, place, x, y),self)
        self.thing, self.x, self.y, self.m = place, x, y, str(self.__class__)
        self.place = Way(None,place, self.x, self.y)
        #self.avatar,self.place, self.x, self.y = avatar, place, x, y
        #self.thing = self.place

class Actor:
    def get_direction(self):
        return self.avatar.heading
    def get_position(self):
        return (self.x, self.y)
    def move(self, x, y, entry= None):
        self.x, self.y = x, y
        self.thing = entry or self.thing
        ##print( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.thing.get_position(x=x, y=y)
        print( 'actor,move, position %d %d  entry%s real %d %d'%(x, y, entry, mx, my))
        avatar.move(mx, my)
    def go_backward(self):
        self.thing.leave(self, action=self.move, reverse=2)
    def go_forward(self):
        self.thing.leave(self, action=self.move)
    def go_take(self):
        self.thing.leave(self, action=self.move, reverse=2)
    def go_give(self):
        self.thing.leave(self, action=self.move)
    def go_pull(self):
        self.thing.leave(self, action=self.move, reverse=2)
    def go_push(self):
        self.thing.push(self, action=self.move)
    def __init__(self, avatar, place, x, y, **kw):
        print( 'actor,init',avatar, place, x, y)
        self.avatar, self.place, self.x, self.y = avatar, place, x, y
        self.thing = place
        VKHANDLER[38] = self.go_forward
        VKHANDLER[40] = self.go_backward
        VKHANDLER[34] = self.go_pull
        VKHANDLER[33] = self.go_push
        VKHANDLER[35] = self.go_take
        VKHANDLER[36] = self.go_give
        print( 'actor,init %d %d %s'%(self.x, self.y, dir(self.thing)))
    
class NullSprite:
    def move(self, place,x,y):
        pass
    def __init__(self, *a):
        pass

INVENTORY = {'.':Way, ' ': Border, '&':Door, '@':Tar, '%':Border}
ES,FS = NullSprite, Sprite        
INVENTORY = {'.':[Way,ES,None], ' ': [Border,ES,None], '&':[Door,ES,None]
    , '@':[Tar,FS,'piche.gif'], '%':[Trunk,FS,'tronco.gif']}
SIMPLE = ('@%&......'+'.'*10+('\n'+'.'*19)*12)
#p = [['%s%d%d'%(p,x,y) for x, p in enumerate(' %s '%row)] for y, row in enumerate(border)]

class Place:
    def get_position(self,x=0,y=0):
        return (x * 32 + 100 - 32, y * 32 + 100 -32)
    def get_next(self,thing, reverse =0):
        x, y = thing.get_position()
        dx, dy = WIND[thing.get_direction() - reverse]
        self.pos = (x+dx, y+dy)
        px, py = self.pos
        locus = self.plan[py][px]
        return locus
    def enter(self,thing, action, position=None):
        ##print( 'place,enter,thing position %s %s'%(thing, position))
        x,y = position #or (self.x, self.y)
        ##print( 'place,enter, position %d %d'%(x, y))
        action( x, y, thing)
    def __init__(self, gui, plan =SIMPLE, **kw):
        self._load(plan, gui)
        self.push = self.enter
        x, y = self.x, self.y
        actor = Actor(Avatar(gui), self, x, y )
        door = self.plan[y][x]
        print( 'place,init xy %s actor %s door %s'%((x,y), actor, door))
        actor.move(x,y,self)
        actor.thing = door
    def _load(self,plan, gui):
        def line(y, row):
            #x = ['%s%d%d'%(p,x,y) for x, p in enumerate(' %s '%row)]
            IV, PART, ICON, IMGE  = INVENTORY, 0, 1, 2
            me, av = self, ES
            x = [IV[p][PART](IV[p][ICON](gui, IV[p][IMGE],me,x,y),me,x,y)
                for x, p in enumerate(' %s '%row)]
            return x
        
        w = len(plan.split('\n')[0])
        border =[' '*w]
        border.extend(plan.split('\n'))
        border.extend([' '*w])
        self.plan = []
        for y,row in enumerate(border):
            self.plan += [line(y,row)]
        ##print(self.plan)
        plan = self.plan
        print ([(p[1],p[1].x) for p in plan])

def go(dc, pn, svg):
    # Setup main scenario
    for child in pn: # iteration on child nodes
            pn.remove(child)
    image = svg.rect(x=10,y=10, width=780, height=580,style={'fill':'forestgreen'})
    image = svg.rect(x=100,y=100, width=600, height=400,style={'fill':'navajowhite'})
    legend = svg.text('Welcome to Kuarup!',x=350,y=45,
        font_size=20,text_anchor="middle",
        style={"stroke":"gold", 'fill':"gold"})

def main(dc, pn, asvg):
    go(dc, pn, asvg)
    place= Place(asvg)

main(doc,doc['panel'], GUI(doc['panel']))
