import pygame


class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.steps = []
        self.direction = "right"

    def getSteps(self):
        return self.steps

    def changeDirection(self, direction):
        self.direction = direction

    def tick(self):
        self.steps.append((self.x, self.y))
        if self.direction == "up":
            self.y -= 1
        elif self.direction == "down":
            self.y += 1
        elif self.direction == "left":
            self.x -= 1
        elif self.direction == "right":
            self.x += 1


    def die(self):
        self.steps = []
        self.x = -1
        self.y = -1
        self.direction = None
