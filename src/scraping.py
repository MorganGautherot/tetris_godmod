import numpy as np
import cv2
from PIL import ImageGrab

class dataframe_creation():
    def __init__(self):
        self.number_screenshot = 0

    def screenshot(self, folder:str, current_tetromino):



        tetromino_name = current_tetromino.tetromino_name.replace('_', '-') 
        screen = ImageGrab.grab(bbox=(651,190,1250,830))

        screen.save(f'{folder}/{self.number_screenshot}_{tetromino_name}.png', 'PNG') 

        if folder=='Y':
            self.number_screenshot += 1