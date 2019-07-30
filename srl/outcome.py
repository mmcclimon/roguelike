class Outcome:
    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        self.success = kwargs['success']

    def dump(self):
        if self.success:
            print("You won!")
        else:
            print("You lost!")

        print("goodbye")
