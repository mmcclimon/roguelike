import curses
from srl.player import Player
from srl.keymap import Keymap
from srl.level  import Level

class UserQuit(Exception):
    pass

class Context:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(trace=True)
        self.keymap = Keymap()
        self._is_running = True

        self.drawables = set([ self.player ])
        self.screen.clear()

        # draw our lil debugging window
        self.cmd_win = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
        self.cmd_win.addstr(0, 0, '[debug]')

        self.level = Level(n=1)
        self.level.generate(self)
        self.drawables.add(self.level)

        self.refresh_all()

    def refresh_all(self):
        self.screen.refresh()
        self.cmd_win.refresh()

    def loop_once(self):
        # draw it.
        for thing in self.drawables:
            thing.draw(self)

        self.screen.refresh()
        self.handle_input()

        # I'm not thrilled about this, but hey
        for thing in self.drawables:
            thing.post_loop_hook(self)


    def handle_input(self):
        k = self.screen.getkey()
        self.keymap.handle_key(self, k)

    def debug(self, msg):
        self.cmd_win.clear()
        self.cmd_win.addstr(0, 0, '[debug] ' + msg)
        self.cmd_win.refresh()

    def is_running(self):
        return self._is_running

    def mark_done(self):
        self._is_running = False

    def place_randomly(self, cls):
        y, x = random_coords(ctx)
