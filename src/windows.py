import pygame
import src.config as config
from src.scores import load_score, write_score
import random

class windows():

    def __init__(self)->None:
        """Initialize the windows of the game"""

        self.level = 1
        self.score = 0
        self.lines = 0

        self.combo = 1  # Combo will increase when you clear lines with several tetrominos in a row


        clock = pygame.time.Clock()

        pygame.init()

        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

        pygame.display.set_caption("Tetris")

        self.screen.blit(self.construct_background_image(self.screen.get_size()), (0, 0))

        tetris_border = pygame.Surface(
            (
                config.MATRIX_WIDTH * config.BLOCKSIZE + config.BORDERWIDTH * 2,
                config.VISIBLE_MATRIX_HEIGHT * config.BLOCKSIZE + config.BORDERWIDTH * 2,
            )
        )

        tetris_border.fill(config.BORDERCOLOR)


        self.screen.blit(tetris_border, (config.MATRIX_OFFSET, config.MATRIX_OFFSET))


    def draw_windows(self):

        while True:
            pressed = lambda key: event.type == pygame.KEYDOWN and event.key == key
            events = pygame.event.get()
            # Controls pausing and quitting the game.
            for event in events:
                self.redraw(self.screen)
                if pressed(pygame.K_p):
                    print('p')

                    


    def construct_background_image(self, size)->pygame.surface.Surface:
        """
        Constructs background image
        """
        surf = pygame.Surface(size)

        boxsize = 8
        bordersize = 1
        vals = "1235"  # only the lower values, for darker colors and greater fear
        arr = pygame.PixelArray(surf)
        for x in range(0, len(arr), boxsize):
            for y in range(0, len(arr[x]), boxsize):
                color = int(
                    "".join([random.choice(vals) + random.choice(vals) for _ in range(3)]),
                    16,
                )

                for LX in range(x, x + (boxsize - bordersize)):
                    for LY in range(y, y + (boxsize - bordersize)):
                        if LX < len(arr) and LY < len(arr[x]):
                            arr[LX][LY] = color
        del arr
        return surf

    def redraw(self, screen):
        """
        Redraws the information panel and next termoino panel
        """
        
        #self.blit_next_tetromino(self.tetris.surface_of_next_tetromino, screen)
        self.blit_info(screen)

        #self.tetris.draw_surface()

        pygame.display.flip()

    def renderpair(self, text, val, font, width):
        text = font.render(text, True, config.TEXTCOLOR)
        val = font.render(str(val), True, config.TEXTCOLOR)

        surf = pygame.Surface(
            (width, text.get_rect().height + config.BORDERWIDTH * 2), pygame.SRCALPHA, 32
        )

        surf.blit(text, text.get_rect(top=config.BORDERWIDTH + 10, left=config.BORDERWIDTH + 10))
        surf.blit(
            val,
            val.get_rect(top=config.BORDERWIDTH + 10, right=width - (config.BORDERWIDTH + 10)),
        )
        return surf


    def blit_info(self, screen):
        """
        Draws information panel
        """
        
        font = pygame.font.Font(None, 30)
        width = (
            config.WIDTH - (config.MATRIX_OFFSET + config.BLOCKSIZE * config.MATRIX_WIDTH + config.BORDERWIDTH * 2)
        ) - config.MATRIX_OFFSET * 2


        # Resizes side panel to allow for all information to be display there.
        scoresurf = self.renderpair("Score", self.score, font, width)
        levelsurf = self.renderpair("Level", self.level, font, width)
        linessurf = self.renderpair("Lines", self.lines, font, width)
        combosurf = self.renderpair("Combo", "x{}".format(self.combo), font, width)

        height = 20 + (
            levelsurf.get_rect().height
            + scoresurf.get_rect().height
            + linessurf.get_rect().height
            + combosurf.get_rect().height
        )

        # Colours side panel
        area = pygame.Surface((width, height))
        area.fill(config.BORDERCOLOR)
        area.fill(
            config.BGCOLOR,
            pygame.Rect(
                config.BORDERWIDTH,
                config.BORDERWIDTH,
                width - config.BORDERWIDTH * 2,
                height - config.BORDERWIDTH * 2,
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
            area, area.get_rect(bottom=config.HEIGHT - config.MATRIX_OFFSET, centerx=config.TRICKY_CENTERX)
        )