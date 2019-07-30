import random

# return y, x, because curses
def random_coords(ctx):
    max_y, max_x = ctx.map_win.getmaxyx()
    return random.randrange(max_y), random.randrange(max_x)


