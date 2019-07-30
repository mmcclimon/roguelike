import curses
from srl.player import Player
from srl.keymap import Keymap
from srl.level  import Level
from srl.outcome import Outcome
from srl.screen_collection import ScreenCollection

class Context:
    def __init__(self, stdscr):
        # draw our windows
        self.screens = ScreenCollection(stdscr)
        self.map = self.screens.map

        self._is_running = True
        self.outcome = Outcome(self, success=False)

        self.player = Player()
        self.keymap = Keymap()

        self.levels = []
        self.level_idx = 0

        # generate the first level
        self.create_level()
        self.player.move_to(*self.current_level.way_up.coords())

        self.screens.refresh()

    def create_level(self):
        l = Level(self, self.level_idx)
        self.levels.append(l)

    def loop_once(self):
        self.screens.map.draw(self, refresh=False)
        self.screens.info.draw(self, refresh=False)
        self.relocate_cursor()
        self.screens.refresh()

        self.handle_input()
        self.handle_collisions()

        # I'm not thrilled about this, but hey
        for thing in self.drawables:
            thing.post_loop_hook(self)

    def relocate_cursor(self):
        self.map.move(*self.player.coords())

    def handle_input(self):
        k = self.screens.stdscr.getkey()
        self.keymap.handle_key(self, k)

    def handle_collisions(self):
        for thing in self.drawables:
            thing.handle_collisions(self)

    def debug(self, msg):
        self.screens.debug.write_text(self, msg)

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

    def ascend(self):
        self.level_idx -= 1
        if self.level_idx < 0:
            self.outcome = Outcome(self, success=True)
            self.mark_done()

        self.player.move_to(*self.current_level.way_down.coords())
        self.map.clear()

