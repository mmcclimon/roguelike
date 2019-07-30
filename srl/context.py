import curses
from srl.player import Player
from srl.keymap import Keymap
from srl.level  import Level
from srl.outcome import Outcome
from srl.screen import Screen

class Context:
    def __init__(self, stdscr):
        # draw our windows
        self.screen = Screen(stdscr)
        self.map_win = self.screen.map_win
        self.cmd_win = self.screen.cmd_win
        self.info_win = self.screen.info_win

        self._is_running = True
        self.outcome = Outcome(self, success=False)

        self.player = Player()
        self.keymap = Keymap()

        self.levels = []
        self.level_idx = 0

        # generate the first level
        self.create_level()
        self.player.move_to(*self.current_level.way_up.coords())

        self.screen.refresh()

    def create_level(self):
        l = Level(self, self.level_idx)
        self.levels.append(l)

    def loop_once(self):
        self.draw_map()
        self.draw_info()

        self.relocate_cursor()

        self.handle_input()
        self.handle_collisions()

        # I'm not thrilled about this, but hey
        for thing in self.drawables:
            thing.post_loop_hook(self)

    def draw_map(self):
        self.map_win.clear()

        for thing in self.drawables:
            thing.draw(self)

        self.map_win.refresh()

    def draw_info(self):
        self.cmd_win.clear()

        level_str = 'Level {}'.format(self.level_idx)
        self.info_win.addstr(0, 0, level_str)
        self.info_win.refresh()

    def relocate_cursor(self):
        self.map_win.move(*self.player.coords())

    def handle_input(self):
        k = self.map_win.getkey()
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
        self.map_win.clear()

    def set_info(self, lines):
        self.info = lines

    def ascend(self):
        self.level_idx -= 1
        if self.level_idx < 0:
            self.outcome = Outcome(self, success=True)
            self.mark_done()

        self.player.move_to(*self.current_level.way_down.coords())
        self.map_win.clear()

