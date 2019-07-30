import curses

# a Screen is a collection of windows.
class Screen:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()

        # draw map window
        self.map_win = curses.newwin(25, 80, 0, 0)

        stdscr.hline(25, 0, curses.ACS_HLINE, 80)
        stdscr.vline(0, 80, curses.ACS_VLINE, 25)
        stdscr.addch(25, 80, curses.ACS_LRCORNER)
        stdscr.refresh()

        # draw info window
        self.info_win = curses.newwin(25, 80, 27, 0)

        # draw our lil debugging window
        self.cmd_win = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
        self.cmd_win.addstr(0, 0, '[debug]')

    def refresh(self):
        self.map_win.refresh()
        self.cmd_win.refresh()

