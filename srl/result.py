class Result:
    def __init__(self, ctx):
        self.ctx = ctx

    def print(self):
        if self.ctx.level_idx < 0:
            print('You won!')
            return

        if self.ctx.player.is_alive:
            print('You quit, like a coward')
        else:
            print('You died. :(')
