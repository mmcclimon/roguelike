class Key:
    def __init__(self, name, func, doc):
        self.name = name
        self.func = func
        self.doc  = doc

    def call(self, *args):
        self.func(*args)

class Keymap:
    def __init__(self):
        self._keys = {}
        self.build_keymap()

    def build_keymap(self):
        self.add_key('h', lambda ctx, key: ctx.player.move_left(ctx),  'move left one step')
        self.add_key('j', lambda ctx, key: ctx.player.move_down(ctx),  'move down one step')
        self.add_key('k', lambda ctx, key: ctx.player.move_up(ctx),    'move up one step')
        self.add_key('l', lambda ctx, key: ctx.player.move_right(ctx), 'move right one step')
        self.add_key('q', lambda ctx, key: ctx.mark_done(),            'quit')

    def add_key(self, key_name, func, doc):
        key_obj = Key(key_name, func, doc)
        self._keys[key_name] = key_obj

    def handle_key(self, ctx, key):
        ctx.debug('handling {}'.format(key))
        try:
            obj = self._keys[key]
            obj.call(ctx, key)
        except KeyError:
            pass
