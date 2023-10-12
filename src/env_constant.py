BGCOLOR = (15, 15, 20)
BORDERCOLOR = (140, 140, 140)

BLOCKSIZE = 30
BORDERWIDTH = 10

MATRIX_OFFSET = 20

MATRIX_WIDTH = 10
MATRIX_HEIGHT = 22

LEFT_MARGIN = 340

WIDTH = MATRIX_WIDTH * BLOCKSIZE + BORDERWIDTH * 2 + MATRIX_OFFSET * 2 + LEFT_MARGIN
HEIGHT = (MATRIX_HEIGHT - 2) * BLOCKSIZE + BORDERWIDTH * 2 + MATRIX_OFFSET * 2

TRICKY_CENTERX = (
    WIDTH - (WIDTH - (MATRIX_OFFSET + BLOCKSIZE * MATRIX_WIDTH + BORDERWIDTH * 2)) / 2
)

VISIBLE_MATRIX_HEIGHT = MATRIX_HEIGHT - 2