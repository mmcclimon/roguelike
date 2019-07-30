class BaseWindow:
    def __init__(self, window):
        self.window = window

    def __getattr__(self, name):
        return getattr(self.window, name)

    def draw(self, ctx, refresh=True):
        pass

