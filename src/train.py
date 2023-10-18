import pygame
from src.game import *
from src.bot import random_bot, system_expert, count_total_height, count_hole_number
from src.images import construct_background_image

class Train(object):
    def main(self, screen):
        """
        Main loop for game
        Redraws scores and next tetromino each time the loop is passed through
        """
        clock = pygame.time.Clock()

        self.tetris = Tetris(screen)
        
        screen.blit(construct_background_image(screen.get_size()), (0, 0))

        tetris_border = Surface(
            (
                MATRIX_WIDTH * BLOCKSIZE + BORDERWIDTH * 2,
                VISIBLE_MATRIX_HEIGHT * BLOCKSIZE + BORDERWIDTH * 2,
            )
        )
        tetris_border.fill(BORDERCOLOR)
        screen.blit(tetris_border, (MATRIX_OFFSET, MATRIX_OFFSET))

        needs_redraw = True

        while True:
            try:
                timepassed = clock.tick(50)
                if needs_redraw :
                    self.redraw(screen)
                
                system_expert(self.tetris)
                #print(count_hole_number(self.tetris.matrix))
                #print(count_total_height(self.tetris.matrix))
                #random_bot(self.tetris)
                #print(count_total_height(self.tetris.matrix))

                needs_redraw = self.tetris.update(
                    (timepassed / 1000.0) if not self.tetris.paused else 0)
                    
            except GameOver:
                return

    def redraw(self, screen):
        """
        Redraws the information panel and next termoino panel
        """
        if not self.tetris.paused:
            self.blit_next_tetromino(self.tetris.surface_of_next_tetromino, screen)
            self.blit_info(screen)

            self.tetris.draw_surface()

        pygame.display.flip()

    def blit_info(self, screen):
        """
        Draws information panel
        """
        textcolor = (255, 255, 255)
        font = pygame.font.Font(None, 30)
        width = (
            WIDTH - (MATRIX_OFFSET + BLOCKSIZE * MATRIX_WIDTH + BORDERWIDTH * 2)
        ) - MATRIX_OFFSET * 2

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
        scoresurf = renderpair("Score", self.tetris.score)
        levelsurf = renderpair("Level", self.tetris.level)
        linessurf = renderpair("Lines", self.tetris.lines)
        combosurf = renderpair("Combo", "x{}".format(self.tetris.combo))

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
            area, area.get_rect(bottom=HEIGHT - MATRIX_OFFSET, centerx=TRICKY_CENTERX)
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

        screen.blit(area, area.get_rect(top=MATRIX_OFFSET, centerx=TRICKY_CENTERX))
