import random
import pygame

class Letter:
    def __init__(self, x_range, y_start=0):
        self.letter = chr(random.randint(65, 90))
        self.x = random.randint(*x_range)
        self.y = y_start
        self.hit = False

    def update_position(self, speed):
        self.y += speed

    def draw(self, screen, font, color):
        text = font.render(self.letter, True, color)
        screen.blit(text, (self.x, self.y))
