from srl.context_drawable import ContextDrawable

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

    def move_left(self, ctx, dist=1):
        self._x -= dist

    def move_right(self, ctx, dist=1):
        self._x += dist

    def move_up(self, ctx, dist=1):
        self._y -= dist

    def move_down(self, ctx, dist=1):
        self._y += dist

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

