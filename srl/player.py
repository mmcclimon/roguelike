from srl.drawable import Drawable


class Player(Drawable):
    def __init__(self, x=0, y=0, hp=10):
        super().__init__(x=x, y=y, glyph="@", desc="you")
        self.hp = hp
        self.is_alive = True

    # a player cannot collide with themselves
    def handle_collisions(self, ctx):
        pass

    def attract_cursor(self, ctx):
        ctx.map.move(*self.coords())

    def try_move(self, ctx, dir_str):
        did_move, what = super().try_move(ctx, dir_str)

        if what:
            ctx.info("Your progress is blocked by a {}.".format(what))

    def take_damage(self, ctx, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.die(ctx)

    def die(self, ctx):
        self.is_alive = False
        ctx.mark_done()
