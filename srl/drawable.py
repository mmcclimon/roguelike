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
    def __init__(self, desc='', is_passable=True, **kwargs):
        self._x = kwargs['x']
        self._y = kwargs['y']
        self.glyph = kwargs['glyph']

        self._desc  = desc
        self.is_passable = is_passable

        self._last_x = self.x
        self._last_y = self.y

    @property
    def x(self): return self._x

    @property
    def y(self): return self._y

    @property
    def description(self): return self._desc

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
