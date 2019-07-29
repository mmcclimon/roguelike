import curses
from srl.player import Player
from srl.keymap import Keymap
from srl.level  import Level

class Context:
    def __init__(self, screen):
        self.screen = screen
        self._is_running = True

        # draw our lil debugging window
        self.cmd_win = curses.newwin(1, curses.COLS, curses.LINES-1, 0)
        self.cmd_win.addstr(0, 0, '[debug]')

        self.player = Player(trace=True)
        self.keymap = Keymap()

        self.levels = []
        self.level_idx = 0

        # generate the first level
        self.create_level()

        self.screen.clear()
        self.refresh_all()

    def create_level(self):
        l = Level(self, self.level_idx)
        self.levels.append(l)

    def refresh_all(self):
        self.screen.refresh()
        self.cmd_win.refresh()

    def loop_once(self):
        # draw it.
        for thing in self.drawables:
            thing.draw(self)

        self.relocate_cursor()
        self.screen.refresh()
        self.handle_input()
        self.handle_collisions()

        # I'm not thrilled about this, but hey
        for thing in self.drawables:
            thing.post_loop_hook(self)

    def relocate_cursor(self):
        self.screen.move(*self.player.coords())

    def handle_input(self):
        k = self.screen.getkey()
        self.keymap.handle_key(self, k)

    def handle_collisions(self):
        for thing in self.drawables:
            thing.handle_collisions(self)

    def debug(self, msg):
        self.cmd_win.clear()
        self.cmd_win.addstr(0, 0, '[debug] ' + msg)
        self.cmd_win.refresh()

    def is_running(self):
        return self._is_running

    def mark_done(self):
        self._is_running = False

    @property
    def current_level(self):
        return self.levels[ self.level_idx ]

    @property
    def drawables(self):
        return [ self.current_level, self.player ]

    def descend(self):
        if self.current_level == self.levels[-1]:
            self.create_level()

        self.level_idx += 1
        self.player.move_to(*self.current_level.way_up.coords())
        self.screen.clear()

    def ascend(self):
        self.level_idx -= 1
        if self.level_idx < 0:
            self.mark_done()

        self.player.move_to(*self.current_level.way_down.coords())
        self.screen.clear()

