class BaseWindow:
    def __init__(self, window):
        self.window = window

        # compute max/min coordinates
        start_y, start_x = window.getbegyx()
        max_y, max_x = window.getmaxyx()
        self.min_x = start_x
        self.min_y = start_y
        self.max_x = max_x
        self.max_y = max_y

    def __getattr__(self, name):
        return getattr(self.window, name)

    def draw(self, ctx, refresh=True):
        pass

    def contains(self, y, x):
        return self.min_y <= y <= self.max_y and self.min_x <= x <= self.max_x

