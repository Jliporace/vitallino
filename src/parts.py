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
:Copyright: 2013, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.1 $Revision$"[10:-1]
__date__    = "2013/02/09 $Date$"
"""
WIND=[(0,-1),(1,0),(0,1),(-1,0)]
PLACE = None

def inherit(base, child):
    overriden, inherited = dir(child), dir(base)
    for member in inherited:
        if member not in overriden:
            setattr(child, member, getattr(base,member))
    #child.m =  str(child.__class__)
    return base

class Cell:
    def __init__(self, avatar, place, x, y, me=None, **kw):
        #inherit(Entrance(place, x, y),self)
        self.avatar,self.place = avatar, place
        self.thing, self.x, self.y, self.m = place, x, y, me or self
    def rebase(self,base):
        return None
    def clear(self):
        print( '%s.clear, position %d %d thing, place %s %s'%(
            self.m, self.x, self.y, self.thing, self.place ))
        self.thing = PLACE #self.place
        self.m.thing = PLACE # self.place
    def get_real_position(self,x=0,y=0):
        return self.place.get_position(x=x,y=y)
    def get_position(self,x=0,y=0):
        return self.place.get_position(x=x,y=y)
    def enter(self,entry, destination ):
        self.thing.enter(entry, destination)
        print( '%s.enter,thing %s self %s destination %s'%(self.m, self.thing, self, destination))
    def leave(self,entry, direction):
        self.place.leave(entry, direction)
    def pushed(self,entry, destination):
        self.thing.pushed(entry, destination)
        print( '%s.pushed,thing %s self %s destination %s'%(self.m, self.thing, self, destination))
    def push(self,entry, direction):
        self.place.push(entry, direction)
    def taken(self,entry, destination):
        self.thing.taken(entry, destination)
        print( '%s.taken,thing %s self %s destination %s'%(self.m, self.thing, self, destination))
    def take(self,entry, direction):
        self.place.take(entry, direction)
    def given(self,entry, destination):
        self.thing.given(entry, destination)
        print( '%s.given,thing %s self %s destination %s'%(self.m, self.thing, self, destination))
    def give(self,entry, direction):
        self.place.give(entry, direction)

class Actor:
    def clear(self):
        print( '%s.clear, position %d %d thing, place %s %s'%(
            self, self.x, self.y, self.thing, self.place ))
        self.thing = self.place.place
    def get_entry(self):
        return self
    def get_direction(self, back= False):
        self.heading = (self.avatar.get_direction()+ int(back)*2)%4
        return self.heading
    def get_real_position(self,x=0,y=0):
        return self.place.get_position(x=x,y=y)
    def get_position(self):
        return (self.x, self.y)
    def take(self, loc):
        loc.move(self)
    def give(self, loc):
        #self.thing = self.thing.thing = self.thing.place = self.place.place
        self.thing.move(loc)
    def move(self, loc):
        self.place.clear()
        #self.x, self.y, loc.thing, self.thing = loc.x, loc.y, self, loc or self.thing
        self.x, self.y, loc.thing = loc.x, loc.y, self
        self.place = loc
        ##print( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.place.get_real_position(x=loc.x, y=loc.y)
        print( 'actor.move, position %d %d  entry%s real %d %d'%(loc.x, loc.y, loc, mx, my))
        avatar.move(mx, my)
    def go_backward(self):
        self.thing.leave(self, direction = self.get_direction(back=True))
    def go_forward(self):
        self.thing.leave(self, direction = self.get_direction())
    def go_take(self):
        self.thing.take(self, direction = self.get_direction())
    def go_give(self):
        self.thing.give(self, direction = self.get_direction())
    def go_pull(self):
        self.thing.push(self, direction = self.get_direction(back=True))
    def go_push(self):
        self.thing.push(self, direction = self.get_direction())
    def __init__(self, avatar, place, x, y, **kw):
        print( 'actor,init',avatar, place, x, y)
        self.avatar, self.place, self.x, self.y = avatar, place, x, y
        self.thing = place.place
        print( 'actor,init %d %d %s'%(self.x, self.y, dir(self.thing)))
    
class Place:
    def clear(self):
        print( 'ERROR, SHOUlD NOT CALL')
        pass
    def get_position(self,x=0,y=0):
        return (x * 32 + 100 - 32, y * 32 + 100 -32)
    def get_next(self, thing, direction):
        x, y = thing.get_position()
        dx, dy = WIND[direction]
        self.pos = (x+dx, y+dy)
        px, py = self.pos
        locus = self.plan[py][px]
        return locus
    def taken(self,entry, destination):
        print('nothing here!')
        #entry.take(destination)
    def take(self,entry, direction):
        locus = self.get_next(entry, direction)
        print( '%s.take locus %s entry %s dir %d lpos %d %d'%(
            'Place', locus, entry, direction, locus.x,locus.y))
        locus.taken(entry, locus)
    def given(self,entry, destination):
        print('nothing here!')
        #entry.give(destination)
    def give(self,entry, direction):
        locus = self.get_next(entry, direction)
        print( '%s.give locus %s entry %s dir %d lpos %d %d'%(
            'Place', locus, entry, direction, locus.x,locus.y))
        locus.given(entry, locus)
    def pushed(self,entry, destination):
        entry.move(destination)
    def enter(self,entry, destination):
        entry.move(destination)
    def leave(self,entry,direction):
        locus = self.get_next(entry, direction)
        print( '%s.leave locus %s entry %s dir %d lpos %d %d'%(
            'Place', locus, entry, direction, locus.x,locus.y))
        locus.enter(entry, locus)
    def push(self,entry,direction):
        locus = self.get_next(entry, direction)
        print( '%s.push locus %s entry %s dir %d lpos %d %d'%(
            'Place', locus, entry, direction, locus.x,locus.y))
        locus.pushed(entry, locus)
    def __init__(self, plan):
        global PLACE
        PLACE = self
        self.plan = plan
