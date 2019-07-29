class Drawable():
    def __init__(self, *args, **kwargs):
        self._x = kwargs['x']
        self._y = kwargs['y']
        self._glyph = kwargs['glyph']

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def glyph(self):
        return self._glyph

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
        ctx.screen.addstr(*self.coords(), self.glyph)
