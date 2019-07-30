from srl.context_drawable import ContextDrawable

class Drawable(ContextDrawable):
    def __init__(self, *args, **kwargs):
        self._x = kwargs['x']
        self._y = kwargs['y']
        self._glyph = kwargs['glyph']

        self._last_x = self.x
        self._last_y = self.y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def glyph(self):
        return self._glyph

    def move_to(self, y, x):
        self._x = x
        self._y = y

    def move_left(self, dist=1):
        self._x -= dist

    def move_right(self, dist=1):
        self._x += dist

    def move_up(self, dist=1):
        self._y -= dist

    def move_down(self, dist=1):
        self._y += dist

    # return y, x to pass directly to curses
    def coords(self):
        return self.y, self.x

    def draw(self, ctx):
        self._last_y, self._last_x = self.coords()
        ctx.map_win.addstr(*self.coords(), self.glyph)

    def handle_collisions(self, ctx):
        if self.coords() == ctx.player.coords():
            ctx.debug('zomg, a collision with {}'.format(self.glyph))
            self.on_collision(ctx)

