import itertools
import random
from srl.drawable import Drawable

# Objects

class StairsDown(Drawable):
    def __init__(self, x=0, y=0):
        super().__init__(
                x=x,
                y=y,
                glyph='>',
                description='a ladder down',
                )

    def on_collision(self, ctx):
        ctx.descend()

class StairsUp(Drawable):
    def __init__(self, x=0, y=0):
        super().__init__(
                x=x,
                y=y,
                glyph='<',
                description='a ladder down',
                )

    def on_collision(self, ctx):
        ctx.ascend()



class Boulder(Drawable):
    def __init__(self, x=0, y=0):
        super().__init__(
                x=x,
                y=y,
                glyph='`',
                description='boulder',
                is_passable=False
                )

# Monsters
class Monster(Drawable):
    def __init__(self, **kwargs):
        kwargs['glyph'] = kwargs.get('glyph', 'X')
        super().__init__(**kwargs)

        self.hp = kwargs['hp']
        self.damage = kwargs['damage']
        self.hit_pct = kwargs['hit_pct']
        self.is_alive = True
        self.mvmt = itertools.cycle(kwargs.get('movement', ['.']))

    def on_collision(self, ctx):
        if self.is_alive:
            self.fight(ctx)

    # we move!
    def on_tick(self, ctx):
        direction = next(self.mvmt)
        if direction != '.':
            self.try_move(ctx, direction)

    def fight(self, ctx):
        if random.random() < self.hit_pct:
            ctx.info('You were hit by a {}!'.format(self.description))
            ctx.player.take_damage(ctx, self.damage)
        else:
            self.take_damage(ctx)

    # TODO damage depends on player attributes (somehow)
    def take_damage(self, ctx):
        ctx.debug('taking damage')
        self.hp -= 1
        if self.hp <= 0:
            self.die(ctx)

    # XXX this is bad
    def die(self, ctx):
        # remove ourselves from our level
        ctx.current_level.drawables.remove(self)
        self.is_alive = False

        ctx.info('You killed a {}.'.format(self.description), expire_after=2)


class GridBug(Monster):
    def __init__(self, x=0, y=0):
        super().__init__(
                x=x,
                y=y,
                glyph='X',
                description='grid bug',
                movement=['up', '.', 'down', '.'],
                hp=1,
                damage=1,
                hit_pct=0.35,
                )

