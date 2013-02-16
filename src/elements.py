"""
############################################################
Vitallino - Criador de Jogos Simplificado
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/01/09  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.2 $
:Home: `Labase http://labase.nce.ufrj.br/`__
:Copyright: 2011, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.2 $Revision$"[10:-1]
__date__    = "2013/02/09 $Date$"
"""
if '__package__' in dir():
    from parts import Cell
    pass
    
def inherit(base, child):
    overriden, inherited = dir(child), dir(base)
    for member in inherited:
        if member not in overriden:
            setattr(child, member, getattr(base,member))
    #child.m =  str(child.__class__)
    return base

class Way:
    def __init__(self, avatar, place, x, y, me=None, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)
        self.avatar,self.place = avatar, place
        self.thing, self.x, self.y, self.m = place, x, y, self

class Tar:
    def leave(self,thing, action, reverse =0):
        print('Youre STUCK!!!')
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)

class Door:
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)
        place.x, place.y =  x, y

class Entry:
    def __init__(self, thing, entry, x, y):
        self.x, self.y, self.entry, self.thing = x, y, entry, thing
    def get_entry(self):
        return self.thing
    def get_direction(self):
        return self.entry.get_direction()
    def get_position(self):
        return (self.x, self.y)

class Trunk:
    def get_direction(self):
        return self.avatar.get_direction()
    def get_position(self,x=0, y=0):
        return (self.x, self.y)
    def enter(self,entry, action, position=None):
        print('It is HEAVY!!')
    def move(self, x, y, loc = None):
        self.place.clear()
        self.x, self.y, loc.thing, self.thing = x, y, self, loc or self.thing
        self.place = loc
        ##print( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.place.get_position(x=x, y=y)
        print( 'trunk.move, position %d %d  entry%s real %d %d'%(x, y, loc, mx, my))
        avatar.move(mx, my)
    def pushed(self,entry, action, position=None, reverse=1):
        def _trunk_pushed(x, y, loc, move_pusher = action, me=self.m):
            place = self.place
            self.move(x,y,loc)
            place.enter(entry, action=move_pusher, position = position)
        print( '%s.pushed,thing %s entry %s position %s'%(
            self.m, self.thing, entry, position))
        self.place.place.push(self, action=_trunk_pushed, reverse = reverse)
        
    def _pushed(self,entry, action, position=None, reverse=1):
        def _trunk_pushed(x, y, loc, move_pusher = action, me=self.m):
            self.x, self.y, self.thing = x, y, loc or self.thing
            self.place, previous_location = loc or self.place, self.place
            previous_location.thing= entry
            mx, my = self.thing.get_position(x=x, y=y)
            px,py = previous_location.get_position(x=x, y=y)
            print( 'trunk.pushed, me %s position %d %d  entry%s real %d %d'%(me, x, y, loc, mx, my))
            me.avatar.move(me, x, y)
            #move_pusher(px,py, previous_location)
            previous_location.place.enter(entry, action=move_pusher, position = position)
        theentry = Entry(self.m, entry, self.x, self.y)
        print( '%s.pushed,thing %s entry %s position %s'%(
            self.m, self.thing, theentry, position))
        self.place.place.push(theentry, action=_trunk_pushed, reverse = reverse)
        
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)
        self.avatar,self.place = avatar, place
        self.thing, self.x, self.y, self.m = place, x, y, self
    def rebase(self,base):
        place = Way(None,self, self.x, self.y)
        base[self.y][self.x]= place
        place.place = self.place
        self.place = place

class Border:
    def enter(self,entry, action, position=None):
        print('Cant go this way!!')
    def pushed(self,entry, action, position=None):
        print('Cant go this way!!')
    def __init__(self, avatar, place, x, y, **kw):
        inherit(Cell(avatar, place, x, y, me=self),self)
        self.thing, self.x, self.y, self.m = place, x, y, self
        self.place = Way(None,place, self.x, self.y)
        #self.avatar,self.place, self.x, self.y = avatar, place, x, y

