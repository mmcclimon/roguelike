from srl.things import StairsDown, StairsUp
from srl.util import random_coords
from srl.context_drawable import ContextDrawable

class Level(ContextDrawable):
    def __init__(self, ctx, idx):
        self.number = idx
        self.drawables = set()
        self.generate(ctx)

    def generate(self, ctx):
        # make a level-down and a level-up
        self.place_randomly(ctx, StairsDown)
        self.place_randomly(ctx, StairsUp)

    def draw(self, ctx):
        for thing in self.drawables:
            thing.draw(ctx)

    def handle_collisions(self, ctx):
        for thing in self.drawables:
            thing.handle_collisions(ctx)

    def place_randomly(self, ctx, cls):
        y, x = random_coords(ctx)
        thing = cls(x=x, y=y)
        self.drawables.add(thing)
