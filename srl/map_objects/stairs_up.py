from srl.drawable import Drawable

class StairsUp(Drawable):
    def __init__(self, x=0, y=0):
        super().__init__(
                x=x,
                y=y,
                glyph='<',
                desc='a ladder down',
                )

    def on_collision(self, ctx):
        ctx.ascend()
