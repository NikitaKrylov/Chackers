import pygame
from config import BLACK, WHITE, display_width, display_height, SIZE, PADDING
import os


class Checker:
    def __init__(self, coll, row, color):
        self.coll = coll
        self.row = row
        self.select = False
        self.king = False
        self.color = color
        self.can_eat = False

        if color == 'WHITE':
            self.checker = pygame.image.load(os.getcwd()+'\img\white.png')
            self.crawn = pygame.image.load(os.getcwd()+'\img\white_crawn.png')
        elif color == "BLACK":
            self.checker = pygame.image.load(os.getcwd()+r'\img\black.png')
            self.crawn = pygame.image.load(os.getcwd()+r'\img\black_crawn.png')

    def make_king(self):
        self.king = True
        self.checker = self.crawn

