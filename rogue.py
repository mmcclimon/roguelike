import curses

PLAYER_CHAR = '@'

def quit():
    print("goodbye")
    exit()

def main(screen):
    screen.clear()

    # this is y, x, because curses.
    player_y = 0
    player_x = 0

    while True:
        # Draw our at-sign
        this_x, this_y = player_x, player_y
        screen.addch(this_y, this_x, PLAYER_CHAR)
        screen.move(this_y, this_x)

        k = screen.getkey()

        if k == 'j':
            player_y += 1
        if k == 'k':
            player_y -= 1
        if k == 'l':
            player_x += 1
        if k == 'h':
            player_x -= 1

        if k == 'q':
            return

        # eventually this will be a clear, but for now let's put a dot.
        screen.addch(this_y, this_x, '.')

try:
    curses.wrapper(main)
except KeyboardInterrupt:
    pass

quit()
