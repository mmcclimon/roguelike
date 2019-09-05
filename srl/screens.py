import curses
import random
from srl.drawable import Palette


class ScreenCollection:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()

        # status line
        status_win = curses.newpad(2, 80)
        self.status = StatusWindow(status_win)

        # draw map window
        map_win = curses.newpad(26, 80)
        self.map = MapWindow(map_win)

        # Map border
        stdscr.hline(25, 0, curses.ACS_HLINE, 80)
        stdscr.vline(0, 80, curses.ACS_VLINE, 25)
        stdscr.addch(25, 80, curses.ACS_LRCORNER)
        stdscr.refresh()

        # draw info window
        info_win = curses.newwin(25, 80, 26, 0)
        self.info = InfoWindow(info_win)

        # draw our lil debugging window
        debug_win = curses.newwin(1, curses.COLS, curses.LINES - 1, 0)
        self.debug = DebugWindow(debug_win)

    def draw(self, ctx, refresh=False):
        self.status.draw(ctx, refresh)
        self.info.draw(ctx, refresh)
        self.map.draw(ctx, refresh)

    def refresh(self):
        # map needs to come last here so that the visible cursor winds up there
        self.status.noutrefresh(*self.status.refresh_args)
        self.info.noutrefresh()
        self.debug.noutrefresh()
        self.map.noutrefresh(*self.map.refresh_args)
        curses.doupdate()


# This is a janky wrapper around curses.window, since it doesn't seem like I
# can rebless the curses.window object into my class.
class BaseWindow:
    def __init__(self, window):
        self.window = window

    def __getattr__(self, name):
        return getattr(self.window, name)

    def draw(self, ctx, refresh=True):
        pass


class StatusWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)

        max_y, max_x = self.window.getmaxyx()
        self.max_x = max_x
        self.refresh_args = [0, 0, 0, 0, 1, self.max_x]

    def draw(self, ctx, refresh=True):
        self.window.erase()
        fmt = "Lvl:{} HP:{}"
        line = fmt.format(ctx.level_idx, ctx.player.hp)

        self.window.addstr(0, 0, line)

        if refresh:
            self.window.refresh(*self.refresh_args)


class MapWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)
        max_y, max_x = self.window.getmaxyx()
        self.max_y = max_y - 2
        self.max_x = max_x
        self.refresh_args = [0, 0, 1, 0, self.max_y, self.max_x]

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
        if y < 0 or y >= self.max_y:
            return False
        if x < 0 or x >= self.max_x:
            return False
        return True


class InfoWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)
        self.text = ""

    def draw(self, ctx, refresh=True):
        self.window.erase()
        self.window.addstr(0, 0, self.text, Palette.yellow)

        if refresh:
            self.window.refresh()

    def write_text(self, ctx, text):
        self.text = text
        self.draw(ctx, refresh=False)


class DebugWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)

        self.text = ""
        self.window.addstr(0, 0, "[debug]")

    def draw(self, ctx, refresh=True):
        self.window.erase()
        debug_str = "[debug] {}".format(self.text)
        self.window.addstr(0, 0, debug_str, Palette.red)

        if refresh:
            self.window.refresh()

    def write_text(self, ctx, text):
        self.text = text
        self.draw(ctx, refresh=True)
