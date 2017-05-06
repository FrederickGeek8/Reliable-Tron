from Player import Player
import game_config as gc
import random
import pygame
import math


class World():
    def __init__(self, display):
        self.players = {}
        self.trails = []
        self.started = False
        self.display = display
        self.dimensions = (self.display.get_size()[0] // (gc.GRID_SIZE + 1),
                           self.display.get_size()[1] // (gc.GRID_SIZE + 1))

    def addPlayer(self, name, color):
        if name not in self.players:
            numplayers = len(self.players) + 1
            dist = math.ceil(numplayers / 2)
            if numplayers % 2 == 0:
                self.players[name] = Player(5, dist * 5, color)
            else:
                self.players[name] = Player(5, self.dimensions[1] - (dist * 5),
                                            color)

    def start(self):
        self.started = True

    def reset(self):
        self.trails = []
        self.players = {}
        self.started = False
        for key in self.players:
            self.players[key].reset()

    def getWinner(self):
        livingPlayers = []
        for key in self.players:
            if not self.players[key].isDead():
                livingPlayers.append(key)

        if len(livingPlayers) == 1 and self.started:
            return livingPlayers[0]

        if len(livingPlayers) == 0 and self.started:
            return "No one"  # No one wins!

        return None

    def interpretPos(self, myname, posdict):
        self.players = {}
        for key in posdict:
            x, y = posdict[key]
            if key == myname:
                color = (0, 191, 255)
            else:
                color = (random.randint(1, 255), random.randint(1, 255),
                         random.randint(1, 255))
            self.players[key] = Player(x, y, color)

    def tick(self):
        if self.started:
            self.trails = []

            for key in self.players:
                self.players[key].tick()
                self.trails += self.players[key].getSteps()

            # Check for collisions
            for key in self.players:
                if ((self.players[key].x, self.players[key].y) in self.trails
                        or self.players[key].x < 0 or
                        self.players[key].y < 0 or
                        self.players[key].x > self.dimensions[0] or
                        self.players[key].y > self.dimensions[1]):
                    self.players[key].die()

    def draw(self):
        for key in self.players:
            for step in self.players[key].getSteps():
                x, y = step
                rect = pygame.Rect(x * (gc.GRID_SIZE + 1), y * (
                    gc.GRID_SIZE + 1), gc.GRID_SIZE, gc.GRID_SIZE)
                pygame.draw.rect(self.display, self.players[key].color, rect)

            rect = pygame.Rect(self.players[key].x * (gc.GRID_SIZE + 1),
                               self.players[key].y * (gc.GRID_SIZE + 1),
                               gc.GRID_SIZE, gc.GRID_SIZE)
            pygame.draw.rect(self.display, self.players[key].color, rect)
