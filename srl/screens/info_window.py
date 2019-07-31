from srl.screens.base_window import BaseWindow

class InfoWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)
        self.text = ''

    def draw(self, ctx, refresh=True):
        self.window.erase()
        self.window.addstr(0, 0, self.text)

        if refresh:
            self.window.refresh()

    def write_text(self, ctx, text):
        self.text = text
        self.draw(ctx, refresh=False)
