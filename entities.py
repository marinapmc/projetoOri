# entities.py
import pygame
from config import BUILDING_TYPES, MAX_BUILDING_RANGE, GREEN, RED

class Building:
    def __init__(self, btype, slot_rect, money_ref):
        self.type = BUILDING_TYPES[btype]
        self.level = 1
        self.bounds = slot_rect
        self.center = (slot_rect[0] + slot_rect[2] // 2,
                       slot_rect[1] + slot_rect[3] // 2)
        self.range = self.type['range']
        self.damage = self.type['damage']
        self.upgrade_cost = self.type['upgrade_cost']
        self.money = money_ref

    def can_upgrade(self):
        return (self.level < self.type['max_level'] and
                self.money['amount'] >= self.upgrade_cost)

    def upgrade(self):
        if self.can_upgrade():
            self.money['amount'] -= self.upgrade_cost
            self.level += 1

    def can_attack(self, bus):
        bx, by, bw, bh = bus.bounds
        cx, cy = self.center
        px = max(bx, min(cx, bx + bw))
        py = max(by, min(cy, by + bh))
        dx = px - cx
        dy = py - cy
        return dx*dx + dy*dy <= self.range*self.range

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.bounds)

class Bus:
    def __init__(self, path, speed=100):
        self.path = path
        self.speed = speed
        self.current = 0
        self.position = list(path[0])
        self.bounds = (*self.position, 20, 20)
        self.passengers = 10
        self.finished = False

    def update(self, dt):
        if self.current < len(self.path) - 1:
            sx, sy = self.path[self.current]
            tx, ty = self.path[self.current + 1]
            dx, dy = tx - sx, ty - sy
            dist = (dx*dx + dy*dy)**0.5
            if dist > 0:
                ux, uy = dx/dist, dy/dist
                self.position[0] += ux * self.speed * dt
                self.position[1] += uy * self.speed * dt
                self.bounds = (self.position[0], self.position[1], 20, 20)
                if ((ux>0 and self.position[0]>=tx) or
                    (ux<0 and self.position[0]<=tx) or
                    (uy>0 and self.position[1]>=ty) or
                    (uy<0 and self.position[1]<=ty)):
                    self.current += 1
        else:
            self.finished = True

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.bounds)