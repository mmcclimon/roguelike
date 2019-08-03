import logging
import random
import toml

from srl.map_objects import Monster

class MonsterCollection:
    def __init__(self, filename):
        raw = toml.load(filename)
        self.templates = {}
        self.keys = []

        for key, kwargs in raw.items():
            self.templates[key] = kwargs
            self.keys.append(key)

    def random_monster(self):
        tmpl = self.templates.get(random.choice(self.keys))
        m = Monster(**tmpl)
        logging.debug('created monster: %s', m.description)
        return m
