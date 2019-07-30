import curses
from srl.screens import MapWindow, InfoWindow, DebugWindow

class ScreenCollection:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()

        # draw map window
        map_win = curses.newwin(25, 80, 0, 0)
        self.map = MapWindow(map_win)

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

    def refresh(self):
        self.debug.refresh()
        self.info.refresh()
        self.map.refresh()
