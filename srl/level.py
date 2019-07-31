from srl.context_drawable import ContextDrawable
from srl.map_objects import StairsDown, StairsUp, Boulder, GridBug

class Level(ContextDrawable):
    def __init__(self, ctx, idx):
        self.number = idx
        self.drawables = set()

        # XXX this is keyed by coordinates. That's not great, because things
        # will be able to move. We should key this by thing instead, I think.
        self.objects = dict()
        self.way_down = None
        self.way_up = None

        self.generate(ctx)

    def generate(self, ctx):
        # make a level-down and a level-up
        self.way_down = self.place_randomly(ctx, StairsDown)
        self.way_up   = self.place_randomly(ctx, StairsUp)

        for i in range(3):
            self.place_randomly(ctx, Boulder)

        self.place_randomly(ctx, GridBug)

    def draw(self, ctx):
        for thing in self.drawables:
            thing.draw(ctx)

    def handle_collisions(self, ctx):
        # Take a local copy in case our drawable disappears during iteration
        to_draw = self.drawables.copy()
        for thing in to_draw:
            thing.handle_collisions(ctx)

    def place_randomly(self, ctx, cls):
        y, x = ctx.map.random_coords()
        while self.has_thing_at(y, x):
            y, x = ctx.map.random_coords()

        thing = cls(x=x, y=y)
        self.drawables.add(thing)
        self.objects[(y, x)] = thing
        return thing

    def has_thing_at(self, y, x):
        return (y, x) in self.objects

    def thing_at(self, y, x):
        try:
            return self.objects[(y, x)]
        except KeyError:
            return None
