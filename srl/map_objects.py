import itertools
import logging
import random
from srl.drawable import Drawable

# Objects


class StairsDown(Drawable):
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y, glyph=">", description="a ladder down")

    def on_collision(self, ctx):
        ctx.descend()


class StairsUp(Drawable):
    def __init__(self, x=0, y=0):
        super().__init__(x=x, y=y, glyph="<", description="a ladder down")

    def on_collision(self, ctx):
        ctx.ascend()


class Boulder(Drawable):
    def __init__(self, x=0, y=0):
        super().__init__(
            x=x, y=y, glyph="`", description="boulder", color="gray", is_passable=False
        )


# Monsters
class Monster(Drawable):
    def __init__(self, **kwargs):
        kwargs["glyph"] = kwargs.get("glyph", "X")
        super().__init__(**kwargs)

        # TODO: implement nethack logic for monsters
        self.hit_pct = 0.25
        self.damage = 1
        self.attack = (kwargs.get("atk_dcount"), kwargs.get("atk_dtype"))
        self.hp = kwargs.get("level", 1)

        self.is_alive = True
        self.mvmt = itertools.cycle(kwargs.get("movement", ["_"]))

    def on_collision(self, ctx):
        if self.is_alive:
            self.fight(ctx)

    # we move!
    def on_tick(self, ctx):
        direction = next(self.mvmt)
        self.try_move(ctx, direction)

    def fight(self, ctx):
        if random.random() < self.hit_pct:
            ctx.info("You were hit by a {}!".format(self.description))
            dmg = self.roll_damage()
            ctx.player.take_damage(ctx, dmg)
        else:
            self.take_damage(ctx)

    def roll_damage(self):
        num_dice, die_type = self.attack
        return sum([random.randint(1, die_type) for _ in range(num_dice)])

    # TODO damage depends on player attributes (somehow)
    def take_damage(self, ctx):
        ctx.debug("taking damage")
        self.hp -= 1
        if self.hp <= 0:
            self.die(ctx)

    # XXX this is bad
    def die(self, ctx):
        # remove ourselves from our level
        ctx.current_level.drawables.remove(self)
        self.is_alive = False

        ctx.info("You killed a {}.".format(self.description), expire_after=2)
