from srl.drawable import Drawable

class Player(Drawable):
    def __init__(self, x=0, y=0, trace=False):
        super().__init__(x=x, y=y, glyph='@')
        self.trace = trace

    # a player cannot collide with themselves
    def handle_collisions(self, ctx):
        pass

    def attract_cursor(self, ctx):
        ctx.map.move(*self.coords())
