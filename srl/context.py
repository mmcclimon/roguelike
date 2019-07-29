# Janky
class UserQuit(Exception):
    pass

class Context:
    PLAYER_CHAR = '@'

    def __init__(self, screen):
        self._s = screen
        self.player_x = 0
        self.player_y = 0

        self._s.clear()

    def loop_once(self):
        screen = self._s

        this_x, this_y = self.player_x, self.player_y
        screen.addch(this_y, this_x, self.PLAYER_CHAR)
        screen.move(this_y, this_x)

        k = screen.getkey()

        if k == 'j':
            self.player_y += 1
        if k == 'k':
            self.player_y -= 1
        if k == 'l':
            self.player_x += 1
        if k == 'h':
            self.player_x -= 1

        if k == 'q':
            raise UserQuit

        # eventually this will be a clear, but for now let's put a dot.
        screen.addch(this_y, this_x, '.')
