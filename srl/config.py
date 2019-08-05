import logging
import random
import toml

from srl.drawable import Direction
from srl.map_objects import Monster

class MonsterCollection:
    _directions = list(Direction)

    def __init__(self, filename):
        raw = toml.load(filename)
        self.templates = {}
        self.keys = []

        for key, kwargs in raw.items():
            self.templates[key] = kwargs
            self.keys.append(key)

    def random_monster(self):
        tmpl = self.templates.get(random.choice(self.keys))
        tmpl['movement'] = self.generate_movement()
        m = Monster(**tmpl)
        logging.debug('created monster: %s', tmpl)
        return m

    def generate_movement(self):
        # random sequence of movements in some cycle-length
        cycle_len = random.randint(2,8)
        return [ random.choice(self._directions) for _ in range(cycle_len)]
