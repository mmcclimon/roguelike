from srl.context_drawable import ContextDrawable
from srl.util import Direction

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

    def move_to(self, y, x):
        self._x = x
        self._y = y

    def move_left(self, ctx):
        self.move_to(*self.coords_for(Direction.left))

    def move_right(self, ctx):
        self.move_to(*self.coords_for(Direction.right))

    def move_up(self, ctx):
        self.move_to(*self.coords_for(Direction.up))

    def move_down(self, ctx):
        self.move_to(*self.coords_for(Direction.down))

    def try_move(self, ctx, direction):
        ctx.debug('moving {} to {}'.format(self.description, direction))
        self.move_to(*self.coords_for(direction))

    # return y, x to pass directly to curses
    def coords(self):
        return self.y, self.x

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
