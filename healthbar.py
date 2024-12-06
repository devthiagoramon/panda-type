import pygame

class HealthBar:
    def __init__(self, max_health, position, size):
        self.max_health = max_health
        self.current_health = max_health
        self.position = position
        self.size = size
        self.red_color = (255, 0, 0)
        self.green_color = (0, 255, 0)

    def reduce_health(self, amount):
        self.current_health -= amount
        self.current_health = max(0, self.current_health)

    def draw(self, screen):
        x, y = self.position
        width, height = self.size
        health_ratio = self.current_health / self.max_health
        pygame.draw.rect(screen, self.red_color, (x, y, width, height))
        pygame.draw.rect(screen, self.green_color, (x, y, width * health_ratio, height))
