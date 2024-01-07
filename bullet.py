import pygame
import os
from settings import *
import math


class Bullet:
    def __init__(self, startx, starty, playerNum, targetx, targety, width = B_WIDTH, height = B_HEIGHT):
        self.width = width
        self.height = height
        self.x = startx
        self.y = starty
        self.playerNum = playerNum
        angle = math.atan2(targety - self.y, targetx - self.x) # gets angle to target in radians
        self.dx = math.cos(angle) * B_VEL
        self.dy = math.sin(angle) * B_VEL


    def draw(self, g):
        pygame.draw.rect(g, BLACK ,(self.x, self.y, self.width, self.height), 0)
        #g.blit(BLACK, (self.x, self.y))

    def move(self):
        self.x += self.dx
        self.y += self.dy



    def collision(self, bullets):
        if self.y > S_HEIGHT:
            bullets.remove(self)
        elif self.y < 0:
            bullets.remove(self)
        elif self.x > S_HEIGHT:
            bullets.remove(self)
        elif self.x < 0:
            bullets.remove(self)