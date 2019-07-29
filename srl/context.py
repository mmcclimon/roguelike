from srl.player import Player
# Janky
class UserQuit(Exception):
    pass

class Context:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(trace=True)
        self.drawables = set([ self.player ])

        self.screen.clear()

    def loop_once(self):
        for thing in self.drawables:
            thing.draw(self)

        self.handle_input()

        # I'm not thrilled about this, but hey
        for thing in self.drawables:
            thing.post_loop_hook(self)



    # eventually: some abstraction.
    def handle_input(self):
        k = self.screen.getkey()

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

