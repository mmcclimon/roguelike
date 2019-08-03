import toml
from srl.map_objects import Monster

class MonsterCollection:
    def __init__(self, filename):
        raw = toml.load(filename)
        self.templates = {}

        for key, kwargs in raw.items():
            self.templates[key] = kwargs

    def random_monster(self):
        tmpl = self.templates.get('grid_bug')
        return Monster(**tmpl)
