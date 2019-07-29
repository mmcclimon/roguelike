from srl.drawable import Drawable

class Player(Drawable):
    def __init__(self, x=0, y=0, trace=False):
        super().__init__(x=x, y=y, glyph='@')
        self.trace = trace


    # also move the cursor position to ourselves
    def draw(self, ctx):
        super().draw(ctx)

    # a player cannot collide with themselves
    def handle_collisions(self, ctx):
        pass

    def post_loop_hook(self, ctx):
        if not self.trace:
            return

        ctx.screen.addch(self._last_y, self._last_x, '.')
