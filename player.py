import pygame
import os
from settings import *

class Player():
    width  = 60
    height = 45

    def __init__(self, startx, starty, playerNum):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.image = pygame.transform.scale(pygame.image.load(f"./assets/p{playerNum}t/p{playerNum}t_r.png"), (self.width, self.height))
        self.playerNum = playerNum


    def draw(self, g):
        #pygame.draw.rect(g, self.image ,(self.x, self.y, self.width, self.height), 0)
        g.blit(self.image, (self.x, self.y))


    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity
