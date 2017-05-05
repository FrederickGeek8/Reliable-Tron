from Player import Player
import pygame
import random

random.seed(0)

class World():
    def __init__(self, gridSize, display):
        self.players = {}
        self.trails = []
        self.gridSize = gridSize
        self.display = display

    def addPlayer(self, name):
        if name not in self.players:
            self.players[name] = Player(5, random.randint(1, 720 // self.gridSize))

    def tick(self):
        self.trails = []

        for key in self.players:
            self.players[key].tick()
            self.trails += self.players[key].getSteps()

        # Check for collisions
        for key in self.players:
            if (self.players[key].x, self.players[key].y) in self.trails:
                self.players[key].die()


    def draw(self):
        for key in self.players:
            for step in self.players[key].getSteps():
                x, y = step
                rect = pygame.Rect(x * (self.gridSize + 1), y * (
                    self.gridSize + 1), self.gridSize, self.gridSize)
                pygame.draw.rect(self.display, (134, 63, 54), rect)

            rect = pygame.Rect(self.players[key].x *
                               (self.gridSize + 1), self.players[key].y *
                               (self.gridSize + 1
                                ), self.gridSize, self.gridSize)
            pygame.draw.rect(self.display, (134, 63, 54), rect)
