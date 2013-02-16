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
        self.m.thing = PLACE #self.place
    def get_position(self,x=0,y=0):
        return self.place.get_position(x=x,y=y)
    def enter(self,entry, action, position=None):
        self._action, thing, x, y = action, self.thing, self.x,self.y
        def _move(x, y, entry, act = action, me=self.m):
            print( '%s._move, position %d %d thing, sthing %s %s'%(me, x, y, me.thing, self.thing ))
            act( self.x, self.y, me)
        thing.enter(entry, action=_move, position = position)
        print( '%s.enter,thing %s self %s position %s'%(self.m, self.thing, self, position))
    def leave(self,entry, action, reverse =0):
        def _left(x, y, loc, act = action, me=self.m):
            act( x, y, loc)
        self.place.leave(entry, action = _left, reverse=reverse)
    def pushed(self,entry, action, position=None, reverse=0):
        self._action, thing, x, y = action, self.thing, self.x,self.y
        def _tpushed(x, y, entry, act = action, me=self.m):
            print( '%s._tpushed, position %d %d thing %s'%(me, x, y, me.thing))
            act( self.x, self.y, me)
        thing.pushed(entry, action=_tpushed, position = position, reverse=reverse)
        print( '%s.pushed,thing %s self %s position %s'%(self.m, self.thing, self, position))
    def push(self,entry, action, reverse =0):
        def _pusher_moved(x, y, loc, move_pusher = action, me=self.m):
            move_pusher( x, y, loc)
        print( '%s.push entry %s lpos %d %d'%('Place', entry, self.x,self.y))
        self.place.push(entry, action = _pusher_moved, reverse=reverse)

class Actor:
    def get_entry(self):
        return self
    def get_direction(self):
        return self.avatar.get_direction()
    def get_position(self):
        return (self.x, self.y)
    def move(self, x, y, loc = None):
        self.place.clear()
        self.x, self.y, loc.thing, self.thing = x, y, self, loc or self.thing
        self.place = loc
        ##print( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.thing.get_position(x=x, y=y)
        print( 'actor.move, position %d %d  entry%s real %d %d'%(x, y, loc, mx, my))
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
        self.thing.push(self, action=self.move, reverse=2)
    def go_push(self):
        self.thing.push(self, action=self.move)
    def __init__(self, avatar, place, x, y, **kw):
        print( 'actor,init',avatar, place, x, y)
        self.avatar, self.place, self.x, self.y = avatar, place, x, y
        self.thing = place
        print( 'actor,init %d %d %s'%(self.x, self.y, dir(self.thing)))
    
class Place:
    def clear(self):
        print( 'ERROR, SHOUlD NOT CALL')
        pass
    def get_position(self,x=0,y=0):
        return (x * 32 + 100 - 32, y * 32 + 100 -32)
    def get_next(self,thing, reverse =0):
        x, y = thing.get_position()
        dx, dy = WIND[thing.get_direction() - reverse]
        self.pos = (x+dx, y+dy)
        px, py = self.pos
        locus = self.plan[py][px]
        return locus
    def pushed(self,thing, action, position=None,reverse =0):
        ##print( 'place,enter,thing position %s %s'%(thing, position))
        x,y = position #or (self.x, self.y)
        ##print( 'place,enter, position %d %d'%(x, y))
        action( x, y, thing)
    def enter(self,thing, action, position=None):
        ##print( 'place,enter,thing position %s %s'%(thing, position))
        x,y = position #or (self.x, self.y)
        ##print( 'place,enter, position %d %d'%(x, y))
        action( x, y, thing)
    def leave(self,entry, action, reverse =0):
        locus = self.get_next(entry,reverse =reverse)
        def _left(x, y, entry, act = action, loc = locus):
            act( x, y,  loc = loc)
        print( '%s.leave to locus: %s lpos %d %d'%('Place', locus, locus.x,locus.y))
        locus.enter(entry, action =_left, position =(locus.x,locus.y))
    def push(self,entry, action, reverse =0):
        locus = self.get_next(entry,reverse =reverse)
        def _ppushed(x, y, entry, act = action, loc = locus):
            act( x, y,  loc = loc)
        print( '%s.push locus %s entry %s lpos %d %d'%('Place', locus, entry, locus.x,locus.y))
        locus.pushed(entry, action =_ppushed, position =(locus.x,locus.y),reverse =reverse)
    def __init__(self, plan):
        global PLACE
        PLACE = self
        self.plan = plan
