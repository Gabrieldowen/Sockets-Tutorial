import pygame
from network import Network
from settings import *
from player import Player
import math

bullets = []

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



    def collision(self):
        if self.y > S_HEIGHT:
            bullets.remove(self)
        elif self.y < 0:
            bullets.remove(self)
        elif self.x > S_HEIGHT:
            bullets.remove(self)
        elif self.x < 0:
            bullets.remove(self)

class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50, 1)
        self.player2 = Player(100,100, 2)
        self.canvas = Canvas(self.width, self.height, "Testing...")

    def run(self):
        clock = pygame.time.Clock()
        run = True


        while run:
            clock.tick(60)

            keys = pygame.key.get_pressed()
            mx, my = pygame.mouse.get_pos()

            # prints num of bullets on screen
            print(len(bullets))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    b = Bullet(self.player.x + self.player.height/2, self.player.y + self.player.width/2, self.player.playerNum, mx, my)
                    bullets.append(b)

            

            if keys[pygame.K_d]:
                if self.player.x <= self.width - self.player.width:
                    self.player.move(0)

            if keys[pygame.K_a]:
                if  self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_w]:
                if  self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_s]:
                if self.player.y <= self.height - self.player.height:
                    self.player.move(3)


            for b in bullets:
                b.move()
                b.collision()

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            for b in bullets:
                b.draw(self.canvas.get_canvas())
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill(WHITE)
