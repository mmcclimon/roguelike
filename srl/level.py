from srl.things import StairsDown, StairsUp
from srl.util import random_coords

class Level:
    def __init__(self, n=1):
        self.n = n
        self.drawables = set()

    def generate(self, ctx):
        # make a level-down and a level-up
        self.place_randomly(ctx, StairsDown)
        self.place_randomly(ctx, StairsUp)

    def draw(self, ctx):
        for thing in self.drawables:
            thing.draw(ctx)

    def post_loop_hook(self, ctx):
        pass

    def place_randomly(self, ctx, cls):
        y, x = random_coords(ctx)
        thing = cls(x=x, y=y)
        self.drawables.add(thing)
