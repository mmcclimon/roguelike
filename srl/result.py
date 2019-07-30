class Result:
    def __init__(self, ctx):
        self.ctx = ctx

    def print(self):
        if self.ctx.level_idx < 0:
            print('You won!')
        else:
            print('You lost. :(')
        print('goodbye')
