import curses
from srl.player import Player
from srl.keymap import Keymap
from srl.level  import Level
from srl.result  import Result
from srl.screen_collection import ScreenCollection

class Context:
    def __init__(self, stdscr):
        # draw our windows
        self.screens = ScreenCollection(stdscr)
        self.map = self.screens.map

        self._is_running = True
        self.ticks = 0

        self.player = Player()
        self.keymap = Keymap()

        self.levels = []
        self.level_idx = 0

        # generate the first level
        self.create_level()
        self.player.move_to(*self.current_level.way_up.coords())

        self.info_expires_at = None
        self.screens.refresh()

    def loop_once(self):
        '''The main run loop.
        Draw all of our screens, wait for input, then do something about it.
        '''
        self.ticks += 1

        # draw
        self.check_info_expiration()
        self.screens.draw(self, refresh=False)
        self.current_level.on_tick(self)
        self.player.attract_cursor(self)
        self.screens.refresh()

        # act
        self.handle_input()
        self.handle_collisions()

    def handle_input(self):
        k = self.screens.stdscr.getkey()
        self.keymap.handle_key(self, k)

    def handle_collisions(self):
        for thing in self.drawables:
            thing.handle_collisions(self)

    def debug(self, msg):
        self.screens.debug.write_text(self, msg)

    def info(self, msg, expire_after=1):
        self.screens.info.write_text(self, msg)
        self.info_expires_at = self.ticks + expire_after + 1

    def check_info_expiration(self):
        if self.info_expires_at == self.ticks:
            self.screens.info.write_text(self, '')
            self.info_expires_at = None

    def generate_result(self):
        return Result(self)

    @property
    def drawables(self):
        return [ self.current_level, self.player ]

    # Loop control plumbing
    # ---------------------
    def is_running(self):
        return self._is_running

    def mark_done(self):
        self._is_running = False

    # Level management code
    # ---------------------
    def create_level(self):
        l = Level(self, self.level_idx)
        self.levels.append(l)

    @property
    def current_level(self):
        return self.levels[ self.level_idx ]

    def descend(self):
        if self.current_level == self.levels[-1]:
            self.create_level()

        self.level_idx += 1
        self.player.move_to(*self.current_level.way_up.coords())

    def ascend(self):
        self.level_idx -= 1
        self.debug('set level index to {}'.format(self.level_idx))
        if self.level_idx < 0:
            self.mark_done()
            return

        self.player.move_to(*self.current_level.way_down.coords())
        self.map.clear()

