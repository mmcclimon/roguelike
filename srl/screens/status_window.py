from srl.screens.base_window import BaseWindow

class StatusWindow(BaseWindow):
    def __init__(self, window):
        super().__init__(window)

        max_y, max_x = self.window.getmaxyx()
        self.max_x = max_x
        self.refresh_args = [0,0, 0,0, 1,self.max_x]


    def draw(self, ctx, refresh=True):
        self.window.erase()
        fmt = 'Lvl:{} HP:{}'
        line = fmt.format(
                ctx.level_idx,
                ctx.player.hp
                )

        self.window.addstr(0, 0, line)

        if refresh:
            self.window.refresh(*self.refresh_args)
