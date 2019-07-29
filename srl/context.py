from srl.player import Player
# Janky
class UserQuit(Exception):
    pass

class Context:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()

        self.screen.clear()

    def loop_once(self):
        this_y, this_x = self.player.coords()   # temporary

        self.player.draw(self)

        k = self.screen.getkey()
        self.handle_key(k)

        self.screen.addch(this_y, this_x, '.')  # temporary


    # eventually: some abstraction.
    def handle_key(self, k):
        if k == 'j':
            self.player.move_down()
        if k == 'k':
            self.player.move_up()
        if k == 'l':
            self.player.move_right()
        if k == 'h':
            self.player.move_left()

        if k == 'q':
            raise UserQuit

