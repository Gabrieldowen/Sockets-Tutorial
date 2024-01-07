import pygame
from network import Network
from settings import *
from player import Player
from bullet import Bullet

# bullets = []

class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 50, 1)
        self.player2 = Player(100,100, 2)
        self.canvas = Canvas(self.width, self.height, "Testing...")
        self.bullets = []
        self.bullets2 = []

    def run(self):
        clock = pygame.time.Clock()
        run = True


        while run:
            clock.tick(60)

            keys = pygame.key.get_pressed()
            mx, my = pygame.mouse.get_pos()

            # prints num of bullets on screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    b = Bullet(self.player.x + self.player.height/2, self.player.y + self.player.width/2, self.player.playerNum, mx, my)
                    self.bullets.append(b)

            # player movement
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

            # bullet movement
            for b in self.bullets:
                b.move()
                b.collision(self.bullets)

            # Send/Recieve Network Stuff
            self.player2.x, self.player2.y, b = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()

            print(f"bullets = {b}")
            print(f"type = {type(b)}")
            '''

                        for i in range(len(bx)):
                b = Bullet(int(bx[i]), int(by[i]), 1, 0, 0)
                b.draw(self.canvas.get_canvas())'''

            for b in self.bullets:
                b.draw(self.canvas.get_canvas())

            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        #Send position to server
        #:return: None
        bulletsX = []
        bulletsY = []

        

        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y) + ":"

        for b in self.bullets:
            data += f"{b.x}, {b.y};"

        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            all = data.split(":")
            d = all[1].split(",")
            b = all[2].split(";")
            b = [i.split(",") for i in b]
            return int(d[0]), int(d[1]), b
        except:
            return 0,0,0


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
