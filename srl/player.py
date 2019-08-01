from srl.drawable import Drawable

class Player(Drawable):
    def __init__(self, x=0, y=0, hp=10):
        super().__init__(x=x, y=y, glyph='@')
        self.hp = hp
        self.is_alive = True

    # a player cannot collide with themselves
    def handle_collisions(self, ctx):
        pass

    def attract_cursor(self, ctx):
        ctx.map.move(*self.coords())

    def can_move_to(self, ctx, y, x):
        if not ctx.map.contains(y,x):
            return (False, 'wall')

        thing = ctx.current_level.thing_at(y, x)
        if not thing:
            return (True, None)

        if thing.is_passable:
            return (True, None)

        return (False, thing.description)

    def _move_direction(self, ctx, dir_str, func):
        can_move, what = self.can_move_to(ctx, *self.coords_for(dir_str))
        if can_move:
            func(ctx)
        else:
            ctx.info('Your progress is blocked by a {}.'.format(what))

    def move_left(self, ctx):
        return self._move_direction(ctx, 'left', super().move_left)

    def move_right(self, ctx):
        return self._move_direction(ctx, 'right', super().move_right)

    def move_up(self, ctx):
        return self._move_direction(ctx, 'up', super().move_up)

    def move_down(self, ctx):
        return self._move_direction(ctx, 'down', super().move_down)

    def take_damage(self, ctx, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.die(ctx)

    def die(self, ctx):
        self.is_alive = False
        ctx.mark_done()

