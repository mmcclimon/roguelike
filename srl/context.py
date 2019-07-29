from srl.player import Player
from srl.keymap import Keymap

class UserQuit(Exception):
    pass

class Context:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(trace=True)
        self.keymap = Keymap()

        self.drawables = set([ self.player ])
        self.screen.clear()

    def loop_once(self):
        for thing in self.drawables:
            thing.draw(self)

        self.handle_input()

        # I'm not thrilled about this, but hey
        for thing in self.drawables:
            thing.post_loop_hook(self)


    def handle_input(self):
        k = self.screen.getkey()
        self.keymap.handle_key(self, k)


