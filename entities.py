# entities.py
import pygame
import math
from pygame import Rect
from config import BUILDING_TYPES, WHITE, GRAY, YELLOW

class Building:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        props = BUILDING_TYPES[tipo]
        self.radius = props["radius"]
        self.damage = props["damage"]
        self.cooldown = props["cooldown"]
        self.color = props["color"]
        self.last_attack = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 20)
        pygame.draw.circle(screen, GRAY, (self.x, self.y), self.radius, 1)

    def try_attack(self, bus, current_time):
        if current_time - self.last_attack >= self.cooldown:
            if math.hypot(bus.x - self.x, bus.y - self.y) <= self.radius:
                if bus.passengers > 0:
                    bus.passengers -= self.damage
                    self.last_attack = current_time

class Bus:
    def __init__(self, path, passengers):
        self.path = path
        self.index = 0
        self.x, self.y = self.path[0]
        self.speed = 1.5
        self.passengers = passengers

    def update(self):
        if self.index < len(self.path) - 1:
            target = self.path[self.index + 1]
            dx, dy = target[0] - self.x, target[1] - self.y
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.index += 1
            else:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, Rect(self.x - 10, self.y - 10, 20, 20))
        font = pygame.font.SysFont(None, 20)
        text = font.render(f"{self.passengers}", True, WHITE)
        screen.blit(text, (self.x - 10, self.y - 25))
