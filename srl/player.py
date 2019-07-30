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

    def can_move_to(self, ctx, y, x):
        if not ctx.map.contains(y,x):
            return False

        thing = ctx.current_level.thing_at(y, x)
        if not thing:
            return True

        if thing.is_passable:
            return True

        return False

    def move_left(self, ctx, dist=1):
        this_y, this_x = self.coords()
        if self.can_move_to(ctx, this_y, this_x - dist):
            super().move_left(ctx, dist)
        else:
            ctx.debug('cannot move left!')
