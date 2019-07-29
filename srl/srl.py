import curses
from srl.context import Context
from srl.exceptions import UserQuit

class SRL:
    @classmethod
    def run(cls):
        try:
            curses.wrapper(cls.main)
        except (KeyboardInterrupt, UserQuit):
            pass

        print('goodbye')

    def main(screen):
        ctx = Context(screen)

        while True:
            # Draw our at-sign
            ctx.loop_once()
