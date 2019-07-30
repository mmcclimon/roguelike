import random
from srl.screens.base_window import BaseWindow

# This is a janky wrapper around curses.window, since it doesn't seem like I
# can rebless the curses.window object into my class.
class MapWindow(BaseWindow):
    def draw(self, ctx, refresh=True):
        self.window.erase()

        for thing in ctx.drawables:
            thing.draw(ctx)

        if refresh:
            self.window.refresh()

    def random_coords(self):
        max_y, max_x = self.window.getmaxyx()
        return random.randrange(max_y), random.randrange(max_x)
