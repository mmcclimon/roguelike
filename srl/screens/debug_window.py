from srl.screens.base_window import BaseWindow

class DebugWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)

        self.text = ''
        self.window.addstr(0, 0, '[debug]')

    def draw(self, ctx, refresh=True):
        self.window.erase()
        debug_str = '[debug] {}'.format(self.text)
        self.window.addstr(0, 0, debug_str)

        if refresh:
            self.window.refresh()

    def write_text(self, ctx, text):
        self.text = text
        self.draw(ctx, refresh=True)
