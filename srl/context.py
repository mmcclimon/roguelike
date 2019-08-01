import curses
from srl.player import Player
from srl.keymap import Keymap
from srl.level  import Level
from srl.screens import ScreenCollection

class Context:
    def __init__(self, stdscr):
        # draw our windows
        self.screens = ScreenCollection(stdscr)
        self.map = self.screens.map
        self.info_expires_at = None

        self._is_running = True
        self.ticks = 0

        self.player = Player()
        self.keymap = Keymap()

        self.levels = []
        self.level_idx = -1

        # We begin...
        self.info('Slowly I turned... step by step...', expire_after=3)
        self.descend()

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
        k = self.screens.stdscr.getkey()
        self.keymap.handle_key(self, k)

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
    def create_level(self, idx):
        if len(self.levels) > idx:
            return

        l = Level(self, idx)
        self.levels.append(l)

    @property
    def current_level(self):
        return self.levels[ self.level_idx ]

    def descend(self):
        if self.level_idx < len(self.levels):
            self.create_level(self.level_idx + 1)

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


# Eventually this will encapsulate how the game turned out.
class Result:
    def __init__(self, ctx):
        self.ctx = ctx

    def print(self):
        if self.ctx.level_idx < 0:
            print('You won!')
            return

        if self.ctx.player.is_alive:
            print('You quit, like a coward')
        else:
            print('You died. :(')
