import random
import warnings;
from srl.drawable import Drawable

class Monster(Drawable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hp = kwargs['hp']
        self.damage = kwargs['damage']
        self.hit_pct = kwargs['hit_pct']
        self.is_alive = True

    def on_collision(self, ctx):
        if self.is_alive:
            self.fight(ctx)

    def fight(self, ctx):
        if random.random() < self.hit_pct:
            ctx.debug('hit!')
            ctx.player.do_damage(ctx, self.damage)
        else:
            self.take_damage(ctx)

    # TODO damage depends on player attributes (somehow)
    def take_damage(self, ctx):
        self.hp -= 1

        if self.hp <= 0:
            ctx.debug('gonna die')
            self.die(ctx)

    # XXX this is bad
    def die(self, ctx):
        # remove ourselves from our level
        me = ctx.current_level.objects[ self.coords() ]
        del ctx.current_level.objects[ self.coords() ]
        ctx.current_level.drawables.remove(me)
        self.is_alive = False

        ctx.info('You killed a {}.'.format(self.description))

