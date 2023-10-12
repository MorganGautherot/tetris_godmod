from pygame import Rect, Surface
import pygame
import random

def construct_background_image(size):
    """
    Constructs background image
    """
    surf = Surface(size)

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