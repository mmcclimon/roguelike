from srl.drawable import Drawable

class Boulder(Drawable):
    def __init__(self, x=0, y=0):
        super().__init__(
                x=x,
                y=y,
                glyph='`',
                desc='boulder',
                is_passable=False
                )
