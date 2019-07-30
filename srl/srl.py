import curses
from srl.context import Context
from srl.exceptions import UserQuit

class SRL:
    @classmethod
    def run(cls):
        try:
            res = curses.wrapper(cls.main)
        except (KeyboardInterrupt):
            pass

        res.print()

    def main(screen):
        ctx = Context(screen)

        while ctx.is_running():
            ctx.loop_once()

        # When this is done, it'll set context.outcome
        return ctx.generate_result()

