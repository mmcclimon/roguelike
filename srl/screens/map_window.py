import curses
import random
from srl.screens.base_window import BaseWindow

# This is a janky wrapper around curses.window, since it doesn't seem like I
# can rebless the curses.window object into my class.
class MapWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)
        max_y, max_x = self.window.getmaxyx()
        self.max_y = max_y - 2
        self.max_x = max_x
        self.refresh_args = [0,0, 1,0, self.max_y, self.max_x]

    def draw(self, ctx, refresh=True):
        self.window.erase()

        for thing in ctx.drawables:
            thing.draw(ctx)

        if refresh:
            self.window.refresh(*self.refresh_args)

    def random_coords(self):
        return random.randrange(self.max_y), random.randrange(self.max_x)

    # Can we actually draw a thing at y,x?
    def contains(self, y, x):
        if y < 0 or y >= self.max_y: return False
        if x < 0 or x >= self.max_x: return False
        return True
