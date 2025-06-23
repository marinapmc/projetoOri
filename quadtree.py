# quadtree.py
import pygame

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary
        hw, hh = w // 2, h // 2
        self.nw = QuadTree(pygame.Rect(x, y, hw, hh), self.capacity)
        self.ne = QuadTree(pygame.Rect(x + hw, y, hw, hh), self.capacity)
        self.sw = QuadTree(pygame.Rect(x, y + hh, hw, hh), self.capacity)
        self.se = QuadTree(pygame.Rect(x + hw, y + hh, hw, hh), self.capacity)
        self.divided = True

    def insert(self, building):
        if not self.boundary.collidepoint(building.x, building.y):
            return False
        if len(self.points) < self.capacity:
            self.points.append(building)
            return True
        if not self.divided:
            self.subdivide()
        return (self.nw.insert(building) or self.ne.insert(building) or
                self.sw.insert(building) or self.se.insert(building))

    def query(self, range_rect, found):
        if not self.boundary.colliderect(range_rect):
            return
        for b in self.points:
            if range_rect.collidepoint(b.x, b.y):
                found.append(b)
        if self.divided:
            self.nw.query(range_rect, found)
            self.ne.query(range_rect, found)
            self.sw.query(range_rect, found)
            self.se.query(range_rect, found)
