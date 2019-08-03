# __init__.py file for srl
import curses
import logging
import srl.context

logging.basicConfig(
    filename='srl.log',
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S',
    level=logging.DEBUG,
)


def run():
    try:
        res = curses.wrapper(_main)
    except (KeyboardInterrupt):
        pass

    res.print()

def _main(screen):
    ctx = srl.context.Context(screen)

    while ctx.is_running():
        ctx.loop_once()

    # When this is done, it'll set context.outcome
    return ctx.generate_result()

