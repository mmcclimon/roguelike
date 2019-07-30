import curses
import random
from srl.screens.base_window import BaseWindow

# This is a janky wrapper around curses.window, since it doesn't seem like I
# can rebless the curses.window object into my class.
class MapWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)
        max_y, max_x = self.window.getmaxyx()
        self.max_y = max_y - 1
        self.max_x = max_x
        self.refresh_args = [0,0, 0,0, self.max_y - 1, self.max_x]

    def draw(self, ctx, refresh=True):
        self.window.erase()

        for thing in ctx.drawables:
            thing.draw(ctx)

        if refresh:
            self.window.refresh(*self.refresh_args)

    def random_coords(self):
        return random.randrange(self.max_y), random.randrange(self.max_x)

    # like enclose(), but returns false for the rightmost edge
    def contains(self, y, x):
        if not self.enclose(y,x):
            return False

        if y == self.max_y:
            return False

        if x == self.max_x:
            return False

        return True
