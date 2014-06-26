"""
############################################################
Vitallino - Criador de Jogos Simplificado
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/02/27  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.4 $
:Home: `Labase http://labase.nce.ufrj.br/`__
:Copyright: 2011, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.4 $Revision$"[10:-1]
__date__    = "2014/02/19 $Date$"
"""
from parts import Cell, Place
#import sys
#import parts


def _logger(*a):
    print(a)

logger = _logger
ZL = []


def execution(code):
    exec(code)


class Way(Cell):
    def __init__(self, avatar, place, x, y, name='', talk='', **kw):
        Cell.__init__(self, avatar, place, x, y, self)
        self.avatar, self.place, self.name = avatar, place, name
        self.thing, self.x, self.y, self.m = place, x, y, self


class Tar(Cell):
    def leave(self, thing, action, reverse=0):
        self.place.talk('Youre STUCK!!!')
        logger('Youre STUCK!!!')

    def __init__(self, avatar, place, x, y, name='', talk='', **kw):
        Cell.__init__(self, avatar, place, x, y, self)
        self.avatar, self.place, self.name = avatar, place, name


class Door(Cell):
    def __init__(self, avatar, place, x, y, name='', talk='', **kw):
        Cell.__init__(self, avatar, place, x, y, self)
        logger(dir(self))
        self.thing, self.x, self.y, self.name = place, x, y, name
        place.x, place.y = x, y


class Entry:
    def __init__(self, thing, entry, x, y):
        self.x, self.y, self.entry, self.thing = x, y, entry, thing

    def get_entry(self):
        return self.thing

    def get_direction(self):
        return self.entry.get_direction()

    def get_position(self):
        return self.x, self.y


class Trunk(Cell):
    def clear(self, load=None):
        logger('%s.clear, position %d %d thing %s load %s' % (
            self.m, self.x, self.y, self.thing, load))
        self.thing = load or Place()  # self.place

    def reset(self):
        self.move_entry = self.null_move_entry
        self.entry.reset()

    def get_direction(self):
        return self.entry.get_direction()

    def get_position(self, x=0, y=0):
        return self.x, self.y

    def enter(self, entry, destination):
        self.place.talk('It is HEAVY!!')
        logger('It is HEAVY!!')
        entry.reset()

    def take(self, entry, direction):
        self.place.talk('Hands Busy!!')
        logger('Hands Busy!!')
        entry.reset()

    def _move(self, loc):
        self.place.clear()
        self.x, self.y = loc.x, loc.y
        self.place = loc
        loc.clear(self)
        ##logger( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.thing.get_real_position(x=loc.x, y=loc.y)
        logger('%s(trunk).move, position %d %d  entry%s real %d %d' % (
            self.m, loc.x, loc.y, loc, mx, my))
        avatar.move(mx, my)

    def move_entry(self, loc):
        pass

    def null_move_entry(self, loc):
        pass

    def move(self, loc):
        place = self.place
        self._move(loc)
        self.move_entry(place)

    def given(self, entry, destination):
        self.place.talk('No space to drop here!!')
        entry.reset()
        #self._move(destination)
        #self.thing.give(self, destination)

    def give(self, entry, direction):
        self.thing.give(self, direction)

    def taken(self, entry, destination):
        entry.take(self)

    def pushed(self, entry, destination):
        def _move_entry(loc, entry=entry, self=self):
            entry.move(loc)
            self.move_entry = self.null_move_entry

        self.move_entry = _move_entry
        self.heading = entry.heading
        self.entry = entry
        logger('%s(trunk).pushed,thing %s entry %s destination %s direction %s' % (
            self.m, self.thing, entry, destination, entry.heading))
        self.thing.push(self, entry)

    def __init__(self, avatar, place, x, y, name='', talk='', **kw):
        Cell.__init__(self, avatar, place, x, y, self)
        self.heading = self.entry = None
        self.avatar, self.place, self.name = avatar, place, name
        self.thing, self.x, self.y, self.m = place, x, y, self

    def rebase(self, base):
        place = Way(None, self, self.x, self.y)
        base[self.y][self.x] = place
        place.place = self.place
        place.thing = self
        self.place = place


class Rock(Cell):
    def clear(self, load=None):
        logger('%s.clear, position %d %d thing %s load %s' % (
            self.m, self.x, self.y, self.thing, load))
        self.thing = load or Place()  # self.place

    def reset(self):
        self.move_entry = self.null_move_entry
        self.entry.reset()

    def get_direction(self):
        return self.entry.get_direction()

    def get_position(self, x=0, y=0):
        return self.x, self.y

    def _move(self, loc):
        self.place.clear()
        self.x, self.y = loc.x, loc.y
        self.place = loc
        loc.clear(self)
        ##logger( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.thing.get_real_position(x=loc.x, y=loc.y)
        logger('%s(rock).move, position %d %d  entry%s real %d %d' % (
            self.m, loc.x, loc.y, loc, mx, my))
        avatar.move(mx, my)

    def move_entry(self, loc):
        pass

    def null_move_entry(self, loc):
        pass

    def move(self, loc):
        place = self.place
        self._move(loc)
        self.move_entry(place)

    def given(self, entry, destination):
        self.place.talk('No space to drop here!!')
        entry.reset()

    def taken(self, entry, destination):
        self.place.talk('Too much heavy to take!!')
        logger('Too much Heavy to take!!')
        entry.reset()

    def enter(self, entry, destination):
        logger('It is HEAVY!!')
        self.place.talk('It is HEAVY!!')
        entry.reset()

    def pushed(self, entry, destination):
        def _move_entry(loc, entry=entry, self=self):
            entry.move(loc)
            self.move_entry = self.null_move_entry

        self.move_entry = _move_entry
        self.heading = entry.heading
        self.entry = entry
        logger('%s(rock).pushed,thing %s entry %s destination %s direction %s' % (
            self.m, self.thing, entry, destination, entry.heading))
        self.thing.push(self, entry)

    def __init__(self, avatar, place, x, y, name='', talk='', **kw):
        Cell.__init__(self, avatar, place, x, y, self)
        self.move_entry = self.heading = self.entry = None
        self.avatar, self.place, self.name = avatar, place, name
        self.thing, self.x, self.y, self.m = place, x, y, self

    def rebase(self, base):
        place = Way(None, self, self.x, self.y)
        base[self.y][self.x] = place
        place.place = self.place
        place.thing = self
        self.place = place


class Border(Cell):
    def enter(self, entry, destination):
        self.place.talk('Cant go this way!!')
        logger('Cant go this way!!')
        entry.reset()

    def pushed(self, entry, destination):
        self.place.talk('Cant go this way!!')
        logger('Cant go this way!!')
        entry.reset()

    def given(self, entry, destination):
        self.place.talk('Cant give this way!!')
        logger('Cant give this way!!')
        entry.reset()

    def __init__(self, avatar, place, x, y, name='', talk='', **kw):
        Cell.__init__(self, avatar, place, x, y, self)
        self.thing, self.x, self.y, self.m = place, x, y, self
        self.avatar, self.place, self.name = avatar, place, name


class cons_out:
    def __init__(self):
        self.value = ''

    def write(self, data):
        self.value += str(data)
        #logger('self.value %s'%self.value)


class Talker(Rock):
    def enter(self, entry, destination):
        self.challenge.start(entry, self.world, self)
        logger('Bumped into Talker!!')
        entry.reset()

    def pushed(self, entry, destination):
        self.place.talk('Cant go this way!!')
        logger('Cant go this way!!')
        entry.reset()

    def given(self, entry, destination):
        self.place.talk('Cant give this way!!')
        logger('Cant give this way!!')
        entry.reset()

    def replace(self, x=0, y=0):
        self.move(self.world.plan[x][y])

    def __init__(self, avatar, place, x, y, name='', talk=None, **kw):
        self.value = self.entry = self._response = self.dialog = None
        Cell.__init__(self, avatar, place, x, y, self)
        self.challenge = talk
        self.thing, self.x, self.y, self.m = place, x, y, self
        self.avatar, self.place, self.name = avatar, place, name
        self.world = self.place
