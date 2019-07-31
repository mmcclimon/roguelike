from srl.monster  import Monster

class GridBug(Monster):
    def __init__(self, x=0, y=0):
        super().__init__(
                x=x,
                y=y,
                glyph='X',
                desc='boulder',
                # is_passable=False
                hp=1,
                damage=1,
                hit_pct=0.35,
                )

