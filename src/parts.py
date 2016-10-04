"""
############################################################
Vitallino - Criador de Jogos Simplificado
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/02/27  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.3 $
:Home: `Labase http://labase.nce.ufrj.br/`__
:Copyright: 2013, `GPL http://is.gd/3Udt`__. 
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br) $Author: carlo $"
__version__ = "0.3 $Revision$"[10:-1]
__date__    = "2014/02/06 $Date$"
"""
WIND = [(0, -1), (1, 0), (0, 1), (-1, 0)]
# Place() = None
NOTHING = None


def _logger(*a):
    print(a)


logger = _logger


class Cell:
    def __init__(self, avatar, place, x, y, me=None, **kw):
        # inherit(Entrance(place, x, y),self)
        self.avatar, self.place = avatar, Place()
        self.thing, self.x, self.y, self.m = place, x, y, me or self

    def talk(self, message):
        Place().talk(message)

    def rebase(self, base):
        return None

    def move(self, loc):
        logger('nothing here, just dust!')

    def clear(self, load=None):
        logger('%s.clear, position %d %d thing %s load %s' % (
            self.m, self.x, self.y, self.thing, load))
        self.thing = load or Place()  # self.place
        self.m.thing = load or Place()  # self.place

    def get_real_position(self, x=0, y=0):
        return self.place.get_position(x=x, y=y)

    def get_position(self, x=0, y=0):
        return self.place.get_position(x=x, y=y)

    def enter(self, entry, destination):
        self.thing.enter(entry, destination)
        logger('%s.enter,thing %s self %s destination %s' % (self.m, self.thing, self, destination))

    def leave(self, entry, direction):
        self.place.leave(entry, direction)

    def pushed(self, entry, destination):
        logger('%s.pushed,thing %s entry %s destination %s' % (self.m, self.thing, entry, destination))
        self.thing.pushed(entry, destination)

    def push(self, entry, direction):
        self.place.push(entry, direction)

    def taken(self, entry, destination):
        logger('%s.taken,thing %s self %s destination %s' % (self.m, self.thing, self, destination))
        self.thing.taken(entry, destination)

    def take(self, entry, direction):
        self.place.take(entry, direction)

    def given(self, entry, destination):
        logger('%s.given,thing %s entry %s self %s destination %s' % (
            self.m, self.thing, entry, self, destination))
        self.thing.given(entry, destination)

    def give(self, entry, direction):
        self.place.give(entry, direction)


class Queuer:
    def __init__(self, actor=None):
        self.queue = []
        self.actor = actor

    def run_command(self, command, **keyword_parameters):
        # logger(command, keyword_parameters)
        self.queue.append([command, keyword_parameters])

    def step(self):
        command, keyword_parameters = self.queue.pop(0)
        # command,keyword_parameters = self.queue[0]
        logger(command, keyword_parameters)
        Place().talk('')
        command(**keyword_parameters)
        if not self.queue:
            logger('New stepper: ', self.actor)
            self.actor.stop()


class Actor:
    def reset(self):
        pass

    def talk(self, message):
        Place().talk(message)

    def leave(self, entry, direction):
        self.place.leave(entry, direction)

    def clear(self, load=None):
        logger('%s.clear, position %d %d thing, load %s %s' % (
            self, self.x, self.y, self.thing, load))
        self.thing = load or Nothing()

    def get_entry(self):
        return self

    def get_direction(self, back=False):
        self.heading = (self.avatar.get_direction() + int(self.back) * 2) % 4
        return self.heading

    def set_direction(self, back=False):
        self.back = back
        return self

    def get_real_position(self, x=0, y=0):
        return self.place.get_position(x=x, y=y)

    def get_position(self):
        return self.x, self.y

    def take(self, loc):
        loc.move(self)

    def give(self, loc):
        # self.thing = self.thing.thing = self.thing.place = self.place.place
        self.thing.move(loc)

    def move(self, loc):
        self.place.clear()
        # self.x, self.y, loc.thing, self.thing = loc.x, loc.y, self, loc or self.thing
        self.x, self.y = loc.x, loc.y
        loc.clear(self)
        self.place = loc
        # logger( 'actor,move, position thing %d %d %s'%(x, y, self.thing))
        avatar = self.avatar
        mx, my = self.place.get_real_position(x=loc.x, y=loc.y)
        logger('actor.move, position %d %d  entry%s real %d %d thing %s' % (loc.x, loc.y, loc, mx, my, self.thing))
        avatar.move(mx, my)
        self.thing.move(self)

    def run_command(self, command, **keyword_parameters):
        Place().talk('')
        command(**keyword_parameters)

    def stop(self):
        logger('Now stepper is : ', self)
        self.stepper = self

    def _backward(self, a=0):
        self.thing.leave(entry=self, direction=self.set_direction(back=True))

    def _forward(self, a=0):
        logger('_forward %s' % self.thing)
        self.thing.leave(entry=self, direction=self.set_direction())

    def _left(self, a=0):
        self.avatar.go_left()

    def _right(self, a=0):
        self.avatar.go_right()

    def _take(self, a=0):
        self.thing.take(entry=self, direction=self.set_direction())

    def _give(self, a=0):
        self.thing.give(entry=self, direction=self.set_direction())

    def _pull(self, a=0):
        self.thing.push(entry=self, direction=self.set_direction(back=True))

    def _push(self, a=0):
        self.thing.push(entry=self, direction=self.set_direction())

    def go_steped(self):
        logger('Stepper : %s' % self.stepper)
        self.stepper.step()

    def go_backward(self, a=0):
        self.stepper.run_command(self._backward)

    def go_forward(self, a=0):
        self.stepper.run_command(self._forward)

    def go_left(self, a=0):
        self.stepper.run_command(self._left)

    def go_right(self, a=0):
        self.stepper.run_command(self._right)

    def go_take(self, a=0):
        self.stepper.run_command(self._take)

    def go_give(self, a=0):
        self.stepper.run_command(self._give)

    def go_pull(self, a=0):
        self.stepper.run_command(self._pull)

    def go_push(self, a=0):
        self.stepper.run_command(self._push)

    def go_step(self, a=0):
        self.do_step()
        self.do_step = self.stepper.step

    def step(self):
        me = self

        class nQueuer:
            def __init__(self, actor=me):
                self.queue = []
                self.actor = actor

            def run_command(self, command, **keyword_parameters):
                # logger(command, keyword_parameters)
                self.queue.append([command, keyword_parameters])

            def step(self, a=0):
                command, keyword_parameters = self.queue.pop(0)
                # command,keyword_parameters = self.queue[0]
                logger(command, keyword_parameters)
                Place().talk('')
                command(**keyword_parameters)
                if not self.queue:
                    logger('New stepper: %s stepper %s' % (self.actor, self.actor.stepper))
                    self.actor.stepper = self.actor
                    self.actor.stop()

        self.stepper = Queuer()
        self.stepper.actor = self
        logger('New stepper: %s stepper %s' % (self.stepper, self.stepper.actor))
        Place().solver(self)

    def __init__(self, avatar, place, x, y, **kw):
        logger('actor,init', avatar, place, x, y)
        self.do_step = self.step
        self.queue = self.actor = self.heading = self.back = None
        self.avatar, self.place, self.x, self.y = avatar, place, x, y
        self.thing = Nothing()
        self.stepper = self
        logger('actor,init %d %d %s' % (self.x, self.y, self.place))


class Place:
    def set_plan(self, plan, gui, iv, solver, sprite):
        def line(y, row, me):
            # x = ['%s%d%d'%(p,x,y) for x, p in enumerate(' %s '%row)]
            PART, IMGE, NAME, TALK = 0, 1, 2, 3
            enum_row = enumerate(' %s ' % row)
            # print("Place.set_plan(self, plan, gui, iv):", iv)
            IV = iv
            x = [IV[p][PART](
                sprite(gui, IV[p][IMGE], me, x, y), me, x, y, IV[p][NAME], IV[p][TALK])
                 for x, p in enum_row]
            return x

        w = len(plan.split('\n')[0])
        border = [' ' * w]
        border.extend(plan.split('\n'))
        border.extend([' ' * w])
        self.plan = []
        logger('self.plan = []')
        """
        for y, row in enumerate(border):
            self.plan += [line(y, row, self)]
            for x, cell in enumerate(self.plan[y]):
                cell.rebase(self.plan)
                # logger(self.plan)
        plan = self.plan
        self.solver = solver
        # Place().plan = self.place.plan = plan
        logger('self.place.plan = plan, len of plan: %d' % len(self.plan))
        self.legend = gui.text('Welcome to Kuarup!', x=350, y=45,
                               font_size=20, text_anchor="middle",
                               style={"stroke": "gold", 'fill': "gold"})
        logger([(p[1], p[1].x) for p in plan])"""
        self.dialog = gui.dialog
        return self

    def clear(self, load=None):
        logger('ERROR, SHOUlD NOT CALL')
        pass

    def get_position(self, x=0, y=0):
        return x * 32 + 100 - 32, y * 32 + 100 - 32

    def get_real_position(self, x=0, y=0):
        return self.get_position(x=x, y=y)

    def get_next(self, thing, direction):
        x, y = thing.get_position()
        dx, dy = WIND[direction.get_direction()]
        self.pos = (x + dx, y + dy)
        px, py = self.pos
        locus = self.plan[py][px]
        return locus

    def taken(self, entry, destination):
        # logger('nothing here!')
        entry.take(destination)

    def take(self, entry, direction):
        locus = self.get_next(entry, direction)
        logger('%s.take locus %s entry %s dir %d lpos %d %d' % (
            'Place', locus, entry, direction.get_direction(), locus.x, locus.y))
        locus.taken(entry, locus)

    def given(self, entry, destination):
        logger('place.given entry %s destination %s' % (entry, destination))
        # entry.given(entry, destination)
        entry.move(destination)

    def give(self, entry, direction):
        locus = self.get_next(entry, direction)
        logger('%s.give locus %s entry %s dir %d lpos %d %d' % (
            'Place', locus, entry, direction.get_direction(), locus.x, locus.y))
        locus.given(entry, locus)

    def pushed(self, entry, destination):
        entry.move(destination)

    def enter(self, entry, destination):
        entry.move(destination)

    def leave(self, entry, direction):
        locus = self.get_next(entry, direction)
        logger('%s.leave locus %s entry %s dir %d lpos %d %d' % (
            'Place', locus, entry, direction.get_direction(), locus.x, locus.y))
        locus.enter(entry, locus)

    def push(self, entry, direction):
        locus = self.get_next(entry, direction)
        logger('%s.push locus %s entry %s thing %s lpos %d %d' % (
            'Place', locus, entry, locus.thing, locus.x, locus.y))
        locus.pushed(entry, locus)

    def talk(self, message):
        self.legend.text = message
        # logger(self.legend.textContent)

    def __init__(self, plan=None, solver=None):
        if hasattr(self, "plan"):
            return
        # global Place()
        self.dialog = None
        self.pos = self.x = self.y = 0
        # PLACE = self
        self.plan = self.plan if hasattr(self, "plan") else plan
        nosolver = lambda *a: None
        self.solver = solver if solver else nosolver
        self.legend = self
        self.nothing = Nothing(self)
        print("Place.__init", hasattr(self, "plan"), self.nothing)

    def move(self, loc):
        print("@@@@@ SHOULD NOT CALL THIS MOVE @@@@@")

    __INSTANCE = None

    def __new__(cls, *args, **kwargs):
        cls.__INSTANCE = super(Place, cls).__new__(cls, *args, **kwargs)
        print("Place __new__")
        # cls.__new__ = cls.__init
        cls.__new__ = lambda *args, **kwargs: cls.__INSTANCE
        return cls.__INSTANCE


class Nothing(Place):
    def give(self, entry, direction):
        logger('nothing here, bare!')
        # entry.give(destination)

    def move(self, loc):
        pass

    __NOINSTANCE = None

    def __new__(cls, place=None):
        self = cls.__NOINSTANCE = object.__new__(cls)
        # self = cls.__NOINSTANCE = super(Nothing, cls).__new__(cls)
        self.place = place  # or Place()
        # self.plan = self.place.plan
        print("Nothing __new__")
        cls.__new__ = lambda *args, **kwargs: cls.__NOINSTANCE
        return cls.__NOINSTANCE
