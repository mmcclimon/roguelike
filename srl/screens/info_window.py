from srl.screens.base_window import BaseWindow

class InfoWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)
        self.text = ''

    def draw(self, ctx, refresh=True):
        self.window.erase()

        level_str = 'Level {}'.format(ctx.level_idx)
        self.window.addstr(0, 0, level_str)

        if refresh:
            self.window.refresh()
