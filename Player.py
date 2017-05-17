import pygame


class Player():
    def __init__(self, x, y, color):
        self.initialX = x
        self.initialY = y
        self.x = x
        self.y = y
        self.steps = []
        self.direction = "right"
        self.color = color

    def getSteps(self):
        return self.steps

    def changeDirection(self, direction):
        # We want to disable turning back on yourself
        directions = {
            "left": "right",
            "right": "left",
            "up": "down",
            "down": "up"
        }
        if self.direction == direction or directions[
                direction] == self.direction:
            return False
        elif direction in directions:
            self.direction = direction
            return True
        return False

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

    def isDead(self):
        return self.direction is None

    def die(self):
        self.steps = []
        self.x = -1
        self.y = -1
        self.direction = None

    def reset(self):
        self.x = self.initialX
        self.y = self.initialY
        self.steps = []
        self.direction = "left"
