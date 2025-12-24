import pygame, math
class Player:
    def __init__(self, name, health=100, position=(0, 0, 0)):
        self.name = name
        self.health = health
        self.position = position # (x, y, r) where r is rotation angle in degrees

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def move(self, dx, dy):
        x, y, r = self.position
        self.position = (x + dx, y + dy, r)

    def rotate(self, angle):
        x, y, r = self.position
        self.position = (x, y, (r + angle) % 360)