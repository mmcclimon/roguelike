from srl.context_drawable import ContextDrawable
from srl.map_objects import StairsDown, StairsUp

class Level(ContextDrawable):
    def __init__(self, ctx, idx):
        self.number = idx
        self.drawables = set()
        self.locs = set()
        self.way_down = None
        self.way_up = None

        self.generate(ctx)

    def generate(self, ctx):
        # make a level-down and a level-up
        self.way_down = self.place_randomly(ctx, StairsDown)
        self.way_up   = self.place_randomly(ctx, StairsUp)

    def draw(self, ctx):
        for thing in self.drawables:
            thing.draw(ctx)

    def handle_collisions(self, ctx):
        for thing in self.drawables:
            thing.handle_collisions(ctx)

    def place_randomly(self, ctx, cls):
        y, x = ctx.map.random_coords()
        while self.has_object_at(y, x):
            y, x = ctx.map.random_coords()

        thing = cls(x=x, y=y)
        self.drawables.add(thing)
        self.locs.add((y, x))
        return thing

    def has_object_at(self, y, x):
        return (y, x) in self.locs
