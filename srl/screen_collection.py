import curses
from srl.screens import MapWindow, InfoWindow, DebugWindow, StatusWindow

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
        debug_win = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
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
