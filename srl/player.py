from srl.drawable import Drawable

class Player(Drawable):
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y, glyph='@')

    # also move the cursor position to ourselves
    def draw(self, ctx):
        super().draw(ctx)
        ctx.screen.move(*self.coords())
