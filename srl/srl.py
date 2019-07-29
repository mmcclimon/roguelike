import curses
from srl.context import Context, UserQuit

class SRL:
    def run():
        try:
            curses.wrapper(SRL.main)
        except (KeyboardInterrupt, UserQuit):
            pass

        print('goodbye')

    def main(screen):
        ctx = Context(screen)

        while True:
            # Draw our at-sign
            ctx.loop_once()
