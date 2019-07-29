import curses
from srl.context import Context
from srl.exceptions import UserQuit

class SRL:
    @classmethod
    def run(cls):
        try:
            curses.wrapper(cls.main)
        except (KeyboardInterrupt):
            pass

        print('goodbye')

    def main(screen):
        ctx = Context(screen)

        while ctx.is_running():
            ctx.loop_once()
