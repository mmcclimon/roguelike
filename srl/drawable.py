from abc import ABC, abstractmethod
import enum

class Direction(enum.Enum):
    left  = enum.auto()
    right = enum.auto()
    up    = enum.auto()
    down  = enum.auto()

class ContextDrawable(ABC):
    @abstractmethod
    def draw(self, ctx):
        pass

    @abstractmethod
    def handle_collisions(self, ctx):
        pass

    def on_collision(self, ctx):
        pass

    def on_tick(self, ctx):
        pass

class Drawable(ContextDrawable):
    def __init__(self, **kwargs):
        self._x = kwargs.get('x', -1)
        self._y = kwargs.get('y', -1)
        self.glyph = kwargs['glyph']

        self.description = kwargs.get('description', '')
        self.is_passable = kwargs.get('is_passable', True)

        self._last_x = self.x
        self._last_y = self.y

    @property
    def x(self): return self._x

    @property
    def y(self): return self._y

    # return y, x to pass directly to curses
    def coords(self):
        return self.y, self.x

    def move_to(self, y, x):
        self._x = x
        self._y = y

    def try_move(self, ctx, direction):
        y, x = self.coords_for(direction)
        can_move, what = self.can_move_to(ctx, y, x)

        if can_move:
            self.move_to(y, x)
            return (True, None)
        else:
            return (False, what)

    # This interface sucks
    def can_move_to(self, ctx, y, x):
        if not ctx.map.contains(y,x):
            return (False, 'wall')

        thing = ctx.current_level.thing_at(y, x)
        if not thing:
            return (True, None)

        if thing.is_passable:
            return (True, None)

        return (False, thing.description)

    def draw(self, ctx):
        self._last_y, self._last_x = self.coords()
        ctx.map.addstr(*self.coords(), self.glyph)

    def handle_collisions(self, ctx):
        if self.coords() == ctx.player.coords():
            ctx.debug('zomg, a collision with {}'.format(self.glyph))
            self.on_collision(ctx)

    # direction is maybe a string, or maybe an enum
    def coords_for(self, direction):
        """Return the y, x coordinates for a cell next to this one.
        You can pass a string, *left*, *right*, *up*, *down*, or an instance
        of the Direction enum"""

        if type(direction) == str:
            direction = Direction[direction]

        if direction == Direction.left:
            return self.y, self.x - 1

        if direction == Direction.right:
            return self.y, self.x + 1

        if direction == Direction.up:
            return self.y - 1, self.x

        if direction == Direction.down:
            return self.y + 1, self.x

        raise ValueError("unknown direction {}".format(direction))


# curses.init_pair() must be done _after_ curses.initscr() is called, which
# means that we can't just run it when the class evaluates. I also want to
# call these things as class methods, which means that we need to define them
# as properties on the metaclass. See https://stackoverflow.com/a/15226813.
class MetaPalette(type):
    def _color_pair(cls, color):
        if getattr(cls, '_color_pairs', None) is None:
            import curses
            cls._color_pairs = {}

            curses.init_pair(1, curses.COLOR_RED, 0)
            cls._color_pairs['red'] = curses.color_pair(1)

            curses.init_pair(2, curses.COLOR_YELLOW, 0)
            cls._color_pairs['yellow'] = curses.color_pair(2)

        return cls._color_pairs[color]

    @property
    def red(cls): return cls._color_pair('red')

    @property
    def yellow(cls): return cls._color_pair('yellow')

# with this metaclass, Palette.red just calls MetaPalette.red(), which will
# lazy-load the colors into curses and do what we want!
class Palette(metaclass=MetaPalette):
    pass
