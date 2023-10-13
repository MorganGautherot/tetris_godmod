#!/usr/bin/env python
import pygame
from pygame import Rect, Surface
import random
import os
import src.kezmenu
from src.env_constant import *
from src.tetrominoes import list_of_tetrominoes
from src.tetrominoes import rotate

from src.scores import load_score, write_score

class GameOver(Exception):
    """Exception used for its control flow properties"""

def get_sound(filename):
    return pygame.mixer.Sound(
        os.path.join(os.path.dirname(__file__), "resources", filename)
    )

class Tetris(object):
    def __init__(self, screen):
        self.surface = screen.subsurface(
            Rect(
                (MATRIX_OFFSET + BORDERWIDTH, MATRIX_OFFSET + BORDERWIDTH),
                (MATRIX_WIDTH * BLOCKSIZE, (MATRIX_HEIGHT - 2) * BLOCKSIZE),
            )
        )

        self.matrix = dict()
        for y in range(MATRIX_HEIGHT):
            for x in range(MATRIX_WIDTH):
                self.matrix[(y, x)] = None
        """
        `self.matrix` is the current state of the tetris board, that is, it records which squares are
        currently occupied. It does not include the falling tetromino. The information relating to the
        falling tetromino is managed by `self.set_tetrominoes` instead. When the falling tetromino "dies",
        it will be placed in `self.matrix`.
        """

        self.next_tetromino = random.choice(list_of_tetrominoes)
        self.set_tetrominoes()
        self.tetromino_rotation = 0
        self.downwards_timer = 0
        self.base_downwards_speed = 0.4  # Move down every 400 ms

        self.movement_keys = {"left": 0, "right": 0}
        self.movement_keys_speed = 0.05
        self.movement_keys_timer = (-self.movement_keys_speed) * 2

        self.level = 1
        self.score = 0
        self.lines = 0

        self.combo = 1  # Combo will increase when you clear lines with several tetrominos in a row

        self.paused = False

        self.highscore = load_score()
        self.played_highscorebeaten_sound = False

        self.levelup_sound = get_sound("levelup.wav")
        self.gameover_sound = get_sound("gameover.wav")
        self.linescleared_sound = get_sound("linecleared.wav")
        self.highscorebeaten_sound = get_sound("highscorebeaten.wav")

    def set_tetrominoes(self):
        """
        Sets information for the current and next tetrominos
        """
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = random.choice(list_of_tetrominoes)
        self.surface_of_next_tetromino = self.construct_surface_of_next_tetromino()
        self.tetromino_position = (
            (0, 4) if len(self.current_tetromino.shape) == 2 else (0, 3)
        )
        self.tetromino_rotation = 0
        self.tetromino_block = self.block(self.current_tetromino.color)
        self.shadow_block = self.block(self.current_tetromino.color, shadow=True)

    def hard_drop(self):
        """
        Instantly places tetrominos in the cells below
        """
        amount = 0
        while self.request_movement("down"):
            amount += 1
        self.score += 10 * amount

        self.lock_tetromino()

    def update(self, timepassed, move):
        """
        Main game loop
        """
        self.needs_redraw = False

        pressed = lambda key: event.type == pygame.KEYDOWN and event.key == key
        unpressed = lambda key: event.type == pygame.KEYUP and event.key == key

        events = pygame.event.get()
        # Controls pausing and quitting the game.
        for event in events:
            if pressed(pygame.K_p):
                self.surface.fill((0, 0, 0))
                self.needs_redraw = True
                self.paused = not self.paused
            elif event.type == pygame.QUIT:
                self.gameover(full_exit=True)
            elif pressed(pygame.K_ESCAPE):
                self.gameover()

        if self.paused:
            return self.needs_redraw

        for event in events:
            # Controls movement of the tetromino
            if pressed(pygame.K_SPACE):
                self.hard_drop()
            elif pressed(pygame.K_UP) or pressed(pygame.K_w):
                self.request_rotation()
            elif pressed(pygame.K_LEFT) or pressed(pygame.K_a):
                self.request_movement("left")
                self.movement_keys["left"] = 1
            elif pressed(pygame.K_RIGHT) or pressed(pygame.K_d):
                self.request_movement("right")
                self.movement_keys["right"] = 1

            elif unpressed(pygame.K_LEFT) or unpressed(pygame.K_a):
                self.movement_keys["left"] = 0
                self.movement_keys_timer = (-self.movement_keys_speed) * 2
            elif unpressed(pygame.K_RIGHT) or unpressed(pygame.K_d):
                self.movement_keys["right"] = 0
                self.movement_keys_timer = (-self.movement_keys_speed) * 2

        if move == "space":
            self.hard_drop()
        elif move == "rotation":
            self.request_rotation()
        elif move == "left":
            self.request_movement("left")
            self.movement_keys["left"] = 1
            self.movement_keys["left"] = 0
            self.movement_keys_timer = (-self.movement_keys_speed) * 2
        elif move == "right":
            self.request_movement("right")
            self.movement_keys["right"] = 1
            self.movement_keys["right"] = 0
            self.movement_keys_timer = (-self.movement_keys_speed) * 2

        self.downwards_speed = self.base_downwards_speed ** (1 + self.level / 10.0)

        self.downwards_timer += timepassed
        downwards_speed = (
            self.downwards_speed * 0.10
            if any(
                [
                    pygame.key.get_pressed()[pygame.K_DOWN],
                    pygame.key.get_pressed()[pygame.K_s],
                ]
            )
            else self.downwards_speed
        )
        if self.downwards_timer > downwards_speed:
            if not self.request_movement(
                "down"
            ):  # Places tetromino if it cannot move further down
                self.lock_tetromino()

            self.downwards_timer %= downwards_speed

        if any(self.movement_keys.values()):
            self.movement_keys_timer += timepassed
        if self.movement_keys_timer > self.movement_keys_speed:
            self.request_movement("right" if self.movement_keys["right"] else "left")
            self.movement_keys_timer %= self.movement_keys_speed

        return self.needs_redraw

    def draw_surface(self):
        """
        Draws the image of the current tetromino
        """
        with_tetromino = self.blend(matrix=self.place_shadow())

        for y in range(MATRIX_HEIGHT):
            for x in range(MATRIX_WIDTH):
                #                                       I hide the 2 first rows by drawing them outside of the surface
                block_location = Rect(
                    x * BLOCKSIZE, (y * BLOCKSIZE - 2 * BLOCKSIZE), BLOCKSIZE, BLOCKSIZE
                )
                if with_tetromino[(y, x)] is None:
                    self.surface.fill(BGCOLOR, block_location)
                else:
                    if with_tetromino[(y, x)][0] == "shadow":
                        self.surface.fill(BGCOLOR, block_location)

                    self.surface.blit(with_tetromino[(y, x)][1], block_location)

    def gameover(self, full_exit=False):
        """
        Gameover occurs when a new tetromino does not fit after the old one has died, either
        after a "natural" drop or a hard drop by the player. That is why `self.lock_tetromino`
        is responsible for checking if it's game over.
        """

        write_score(self.score)

        if full_exit:
            exit()
        else:
            raise GameOver("Sucker!")

    def place_shadow(self):
        """
        Draws shadow of tetromino so player can see where it will be placed
        """
        posY, posX = self.tetromino_position
        while self.blend(position=(posY, posX)):
            posY += 1

        position = (posY - 1, posX)

        return self.blend(position=position, shadow=True)

    def fits_in_matrix(self, shape, position):
        """
        Checks if tetromino fits on the board
        """
        posY, posX = position
        for x in range(posX, posX + len(shape)):
            for y in range(posY, posY + len(shape)):
                if (
                    self.matrix.get((y, x), False) is False
                    and shape[y - posY][x - posX]
                ):  # outside matrix
                    return False

        return position

    def request_rotation(self):
        """
        Checks if tetromino can rotate
        Returns the tetromino's rotation position if possible
        """
        rotation = (self.tetromino_rotation + 1) % 4
        shape = self.rotated(rotation)

        y, x = self.tetromino_position

        position = (
            self.fits_in_matrix(shape, (y, x))
            or self.fits_in_matrix(shape, (y, x + 1))
            or self.fits_in_matrix(shape, (y, x - 1))
            or self.fits_in_matrix(shape, (y, x + 2))
            or self.fits_in_matrix(shape, (y, x - 2))
        )
        # ^ That's how wall-kick is implemented

        if position and self.blend(shape, position):
            self.tetromino_rotation = rotation
            self.tetromino_position = position

            self.needs_redraw = True
            return self.tetromino_rotation
        else:
            return False

    def request_movement(self, direction):
        """
        Checks if teteromino can move in the given direction and returns its new position if movement is possible
        """
        posY, posX = self.tetromino_position
        if direction == "left" and self.blend(position=(posY, posX - 1)):
            self.tetromino_position = (posY, posX - 1)
            self.needs_redraw = True
            return self.tetromino_position
        elif direction == "right" and self.blend(position=(posY, posX + 1)):
            self.tetromino_position = (posY, posX + 1)
            self.needs_redraw = True
            return self.tetromino_position
        elif direction == "up" and self.blend(position=(posY - 1, posX)):
            self.needs_redraw = True
            self.tetromino_position = (posY - 1, posX)
            return self.tetromino_position
        elif direction == "down" and self.blend(position=(posY + 1, posX)):
            self.needs_redraw = True
            self.tetromino_position = (posY + 1, posX)
            return self.tetromino_position
        else:
            return False

    def rotated(self, rotation=None):
        """
        Rotates tetromino
        """
        if rotation is None:
            rotation = self.tetromino_rotation
        return rotate(self.current_tetromino.shape, rotation)

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

        border = Surface((BLOCKSIZE, BLOCKSIZE), pygame.SRCALPHA, 32)
        border.fill(list(map(lambda c: c * 0.5, colors[color])) + end)

        borderwidth = 2

        box = Surface(
            (BLOCKSIZE - borderwidth * 2, BLOCKSIZE - borderwidth * 2),
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
        border.blit(box, Rect(borderwidth, borderwidth, 0, 0))

        return border

    def lock_tetromino(self):
        """
        This method is called whenever the falling tetromino "dies". `self.matrix` is updated,
        the lines are counted and cleared, and a new tetromino is chosen.
        """
        self.matrix = self.blend()

        lines_cleared = self.remove_lines()
        self.lines += lines_cleared

        if lines_cleared:
            if lines_cleared >= 4:
                self.linescleared_sound.play()
            self.score += 100 * (lines_cleared**2) * self.combo

            if not self.played_highscorebeaten_sound and self.score > self.highscore:
                if self.highscore != 0:
                    self.highscorebeaten_sound.play()
                self.played_highscorebeaten_sound = True

        if self.lines >= self.level * 10:
            self.levelup_sound.play()
            self.level += 1

        self.combo = self.combo + 1 if lines_cleared else 1

        self.set_tetrominoes()

        if not self.blend():
            self.gameover_sound.play()
            self.gameover()

        self.needs_redraw = True

    def remove_lines(self):
        """
        Removes lines from the board
        """
        lines = []
        for y in range(MATRIX_HEIGHT):
            # Checks if row if full, for each row
            line = (y, [])
            for x in range(MATRIX_WIDTH):
                if self.matrix[(y, x)]:
                    line[1].append(x)
            if len(line[1]) == MATRIX_WIDTH:
                lines.append(y)

        for line in sorted(lines):
            # Moves lines down one row
            for x in range(MATRIX_WIDTH):
                self.matrix[(line, x)] = None
            for y in range(0, line + 1)[::-1]:
                for x in range(MATRIX_WIDTH):
                    self.matrix[(y, x)] = self.matrix.get((y - 1, x), None)

        return len(lines)

    def blend(self, shape=None, position=None, matrix=None, shadow=False):
        """
        Does `shape` at `position` fit in `matrix`? If so, return a new copy of `matrix` where all
        the squares of `shape` have been placed in `matrix`. Otherwise, return False.

        This method is often used simply as a test, for example to see if an action by the player is valid.
        It is also used in `self.draw_surface` to paint the falling tetromino and its shadow on the screen.
        """
        if shape is None:
            shape = self.rotated()
        if position is None:
            position = self.tetromino_position

        copy = dict(self.matrix if matrix is None else matrix)
        posY, posX = position
        for x in range(posX, posX + len(shape)):
            for y in range(posY, posY + len(shape)):
                if (
                    copy.get((y, x), False) is False
                    and shape[y - posY][x - posX]  # shape is outside the matrix
                    or copy.get(  # coordinate is occupied by something else which isn't a shadow
                        (y, x)
                    )
                    and shape[y - posY][x - posX]
                    and copy[(y, x)][0] != "shadow"
                ):
                    return (
                        False  # Blend failed; `shape` at `position` breaks the matrix
                    )

                elif shape[y - posY][x - posX]:
                    copy[(y, x)] = (
                        ("shadow", self.shadow_block)
                        if shadow
                        else ("block", self.tetromino_block)
                    )

        return copy

    def construct_surface_of_next_tetromino(self):
        """
        Draws the image of the next tetromino
        """
        shape = self.next_tetromino.shape
        surf = Surface(
            (len(shape) * BLOCKSIZE, len(shape) * BLOCKSIZE), pygame.SRCALPHA, 32
        )

        for y in range(len(shape)):
            for x in range(len(shape)):
                if shape[y][x]:
                    surf.blit(
                        self.block(self.next_tetromino.color),
                        (x * BLOCKSIZE, y * BLOCKSIZE),
                    )
        return surf
    
    def count_hole_number(self):
        """ 
        Count the nuber of hole in the tetris matrix. 
        A hole is an empty space cover by a tetrominoes
        """
        number_hole = 0
        for width in range(MATRIX_WIDTH):
            hole = False
            for height in range(MATRIX_HEIGHT-1, -1, -1):
                if self.matrix[height, width] == None and not(hole) :
                    hole = True
                if self.matrix[height, width] != None and self.matrix[height, width][0] == 'block' and hole:
                    number_hole +=1
                    hole = False

        return number_hole