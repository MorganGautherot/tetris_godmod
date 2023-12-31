from MaTris.matris import *
import pygame
import numpy as np


BLOCKSIZE = 30
BORDERWIDTH = 10

MATRIS_OFFSET = 20

MATRIX_WIDTH = 10
MATRIX_HEIGHT = 22

LEFT_MARGIN = 340

WIDTH = MATRIX_WIDTH * BLOCKSIZE + BORDERWIDTH * 2 + MATRIS_OFFSET * 2 + LEFT_MARGIN
HEIGHT = (MATRIX_HEIGHT - 2) * BLOCKSIZE + BORDERWIDTH * 2 + MATRIS_OFFSET * 2


def random_move() -> str:
    """Make a random action for the block"""
    choice = np.random.randint(3)

    if choice == 0:
        move = "left"
    elif choice == 1:
        move = "right"
    elif choice == 2:
        move = "rotation"

    return move


class Train(object):
    def main(self, screen):
        """
        Main loop for game
        Redraws scores and next tetromino each time the loop is passed through
        """
        clock = pygame.time.Clock()

        self.matris = Matris(screen)
        screen.blit(construct_nightmare(screen.get_size()), (0, 0))

        matris_border = Surface(
            (
                MATRIX_WIDTH * BLOCKSIZE + BORDERWIDTH * 2,
                VISIBLE_MATRIX_HEIGHT * BLOCKSIZE + BORDERWIDTH * 2,
            )
        )
        matris_border.fill(BORDERCOLOR)
        screen.blit(matris_border, (MATRIS_OFFSET, MATRIS_OFFSET))

        self.redraw(screen)

        while True:
            try:
                timepassed = clock.tick(50)
                move = randommove()
                if self.matris.update(
                    (timepassed / 1000.0) if not self.matris.paused else 0, move
                ):
                    self.redraw(screen)
            except GameOver:
                return

    def redraw(self, screen):
        """
        Redraws the information panel and next termoino panel
        """
        if not self.matris.paused:
            self.blit_next_tetromino(self.matris.surface_of_next_tetromino, screen)
            self.blit_info(screen)

            self.matris.draw_surface()

        pygame.display.flip()

    def blit_info(self, screen):
        """
        Draws information panel
        """
        textcolor = (255, 255, 255)
        font = pygame.font.Font(None, 30)
        width = (
            WIDTH - (MATRIS_OFFSET + BLOCKSIZE * MATRIX_WIDTH + BORDERWIDTH * 2)
        ) - MATRIS_OFFSET * 2

        def renderpair(text, val):
            text = font.render(text, True, textcolor)
            val = font.render(str(val), True, textcolor)

            surf = Surface(
                (width, text.get_rect().height + BORDERWIDTH * 2), pygame.SRCALPHA, 32
            )

            surf.blit(text, text.get_rect(top=BORDERWIDTH + 10, left=BORDERWIDTH + 10))
            surf.blit(
                val,
                val.get_rect(top=BORDERWIDTH + 10, right=width - (BORDERWIDTH + 10)),
            )
            return surf

        # Resizes side panel to allow for all information to be display there.
        scoresurf = renderpair("Score", self.matris.score)
        levelsurf = renderpair("Level", self.matris.level)
        linessurf = renderpair("Lines", self.matris.lines)
        combosurf = renderpair("Combo", "x{}".format(self.matris.combo))

        height = 20 + (
            levelsurf.get_rect().height
            + scoresurf.get_rect().height
            + linessurf.get_rect().height
            + combosurf.get_rect().height
        )

        # Colours side panel
        area = Surface((width, height))
        area.fill(BORDERCOLOR)
        area.fill(
            BGCOLOR,
            Rect(
                BORDERWIDTH,
                BORDERWIDTH,
                width - BORDERWIDTH * 2,
                height - BORDERWIDTH * 2,
            ),
        )

        # Draws side panel
        area.blit(levelsurf, (0, 0))
        area.blit(scoresurf, (0, levelsurf.get_rect().height))
        area.blit(
            linessurf, (0, levelsurf.get_rect().height + scoresurf.get_rect().height)
        )
        area.blit(
            combosurf,
            (
                0,
                levelsurf.get_rect().height
                + scoresurf.get_rect().height
                + linessurf.get_rect().height,
            ),
        )

        screen.blit(
            area, area.get_rect(bottom=HEIGHT - MATRIS_OFFSET, centerx=TRICKY_CENTERX)
        )

    def blit_next_tetromino(self, tetromino_surf, screen):
        """
        Draws the next tetromino in a box to the side of the board
        """
        area = Surface((BLOCKSIZE * 5, BLOCKSIZE * 5))
        area.fill(BORDERCOLOR)
        area.fill(
            BGCOLOR,
            Rect(
                BORDERWIDTH,
                BORDERWIDTH,
                BLOCKSIZE * 5 - BORDERWIDTH * 2,
                BLOCKSIZE * 5 - BORDERWIDTH * 2,
            ),
        )

        areasize = area.get_size()[0]
        tetromino_surf_size = tetromino_surf.get_size()[0]
        # ^^ I'm assuming width and height are the same

        center = areasize / 2 - tetromino_surf_size / 2
        area.blit(tetromino_surf, (center, center))

        screen.blit(area, area.get_rect(top=MATRIS_OFFSET, centerx=TRICKY_CENTERX))


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MaTris")
    Train().main(screen)
