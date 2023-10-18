import pygame
import src.config as config
import random

class windows():

    def __init__(self, score)->None:
        """Initialize the windows of the game"""

        # get game score information
        self.tetris_score = score

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

        self.surface = self.screen.subsurface(
            pygame.Rect(
                (config.MATRIX_OFFSET + config.BORDERWIDTH, config.MATRIX_OFFSET + config.BORDERWIDTH),
                (config.MATRIX_WIDTH * config.BLOCKSIZE, (config.MATRIX_HEIGHT - 2) * config.BLOCKSIZE),
            )
        )

        tetris_border.fill(config.BORDERCOLOR)


        self.screen.blit(tetris_border, (config.MATRIX_OFFSET, config.MATRIX_OFFSET))

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

    def redraw(self, 
               screen,
               matrix,
               next_tetromino)->None:
        """
        Redraws the information panel and next termoino panel
        """
        
        next_tetromino_surface = self.construct_surface_of_next_tetromino(next_tetromino)
        self.blit_next_tetromino(next_tetromino_surface, screen)

        self.blit_info(screen)

        self.draw_surface(matrix)

        pygame.display.flip()

    def draw_surface(self, matrix):
        """
        Draws the image of the current tetromino
        """

        for y in range(config.MATRIX_HEIGHT):
            for x in range(config.MATRIX_WIDTH):
                #                                       I hide the 2 first rows by drawing them outside of the surface
                block_location = pygame.Rect(
                    x * config.BLOCKSIZE, (y * config.BLOCKSIZE - 2 * config.BLOCKSIZE), config.BLOCKSIZE, config.BLOCKSIZE
                )

                if matrix[(y, x)] is None:
                    self.surface.fill(config.BGCOLOR, block_location)
                else:

                    if matrix[(y, x)][0] == "shadow":

                        self.surface.fill(config.BGCOLOR, block_location)
                    tetromino_block = self.block(matrix[(y, x)][1].tetromino_color)
                    self.surface.blit(tetromino_block, block_location)

    def block(self, color, shadow=False):
        """
        Sets visual information for tetromino
        """
        colors = {
            "blue": (105, 105, 255),
            "yellow": (225, 242, 41),
            "pink": (242, 41, 195),
            "green": (22, 181, 64),
            "red": (204, 22, 22),
            "orange": (245, 144, 12),
            "cyan": (10, 255, 226),
        }

        if shadow:
            end = [90]  # end is the alpha value
        else:
            end = (
                []
            )  # Adding this to the end will not change the array, thus no alpha value

        border = pygame.Surface((config.BLOCKSIZE, config.BLOCKSIZE), pygame.SRCALPHA, 32)
        border.fill(list(map(lambda c: c * 0.5, colors[color])) + end)

        borderwidth = 2

        box = pygame.Surface(
            (config.BLOCKSIZE - borderwidth * 2, config.BLOCKSIZE - borderwidth * 2),
            pygame.SRCALPHA,
            32,
        )
        boxarr = pygame.PixelArray(box)
        for x in range(len(boxarr)):
            for y in range(len(boxarr)):
                boxarr[x][y] = tuple(
                    list(
                        map(
                            lambda c: min(255, int(c * random.uniform(0.8, 1.2))),
                            colors[color],
                        )
                    )
                    + end
                )

        del boxarr  # deleting boxarr or else the box surface will be 'locked' or something like that and won't blit.
        border.blit(box, pygame.Rect(borderwidth, borderwidth, 0, 0))

        return border

    def construct_surface_of_next_tetromino(self, next_tetromino):
        """
        Draws the image of the next tetromino
        """
        shape = next_tetromino.tetromino_shape
        surf = pygame.Surface(
            (len(shape) * config.BLOCKSIZE, len(shape) * config.BLOCKSIZE), pygame.SRCALPHA, 32
        )

        for y in range(len(shape)):
            for x in range(len(shape)):
                if shape[y][x]:
                    surf.blit(
                        self.block(next_tetromino.tetromino_color),
                        (x * config.BLOCKSIZE, y * config.BLOCKSIZE),
                    )
        return surf
    
    def blit_next_tetromino(self, tetromino_surf, screen):
        """
        Draws the next tetromino in a box to the side of the board
        """
        area = pygame.Surface((config.BLOCKSIZE * 5, config.BLOCKSIZE * 5))
        area.fill(config.BORDERCOLOR)
        area.fill(
            config.BGCOLOR,
            pygame.Rect(
                config.BORDERWIDTH,
                config.BORDERWIDTH,
                config.BLOCKSIZE * 5 - config.BORDERWIDTH * 2,
                config.BLOCKSIZE * 5 - config.BORDERWIDTH * 2,
            ),
        )

        areasize = area.get_size()[0]
        tetromino_surf_size = tetromino_surf.get_size()[0]
        # ^^ I'm assuming width and height are the same

        center = areasize / 2 - tetromino_surf_size / 2
        area.blit(tetromino_surf, (center, center))

        screen.blit(area, area.get_rect(top=config.MATRIX_OFFSET, centerx=config.TRICKY_CENTERX))

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
        scoresurf = self.renderpair("Score", self.tetris_score.score, font, width)
        levelsurf = self.renderpair("Level", self.tetris_score.level, font, width)
        linessurf = self.renderpair("Lines", self.tetris_score.lines, font, width)
        combosurf = self.renderpair("Combo", "x{}".format(self.tetris_score.combo), font, width)

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