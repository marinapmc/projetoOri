# quadtree.py
from config import WIDTH, HEIGHT

class Rect:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def contains(self, obj):
        bx, by, bw, bh = obj.bounds
        return (bx >= self.x and by >= self.y
                and bx + bw <= self.x + self.w
                and by + bh <= self.y + self.h)

    def intersects(self, other):
        return not (other.x > self.x + self.w or
                    other.x + other.w < self.x or
                    other.y > self.y + self.h or
                    other.y + other.h < self.y)

class QuadTree:
    def __init__(self, boundary: Rect, capacity: int = 4):
        self.boundary = boundary
        self.capacity = capacity
        self.objects = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h
        hw, hh = w / 2, h / 2
        self.northeast = QuadTree(Rect(x + hw, y, hw, hh), self.capacity)
        self.northwest = QuadTree(Rect(x, y, hw, hh), self.capacity)
        self.southeast = QuadTree(Rect(x + hw, y + hh, hw, hh), self.capacity)
        self.southwest = QuadTree(Rect(x, y + hh, hw, hh), self.capacity)
        self.divided = True

    def insert(self, obj):
        if not self.boundary.contains(obj):
            return False
        if len(self.objects) < self.capacity:
            self.objects.append(obj)
            return True
        if not self.divided:
            self.subdivide()
        return (
            self.northeast.insert(obj) or
            self.northwest.insert(obj) or
            self.southeast.insert(obj) or
            self.southwest.insert(obj)
        )

    def query(self, range_rect: Rect, found=None):
        if found is None:
            found = []
        if not self.boundary.intersects(range_rect):
            return found
        for obj in self.objects:
            obj_rect = Rect(*obj.bounds)
            if range_rect.intersects(obj_rect):
                found.append(obj)
        if self.divided:
            self.northeast.query(range_rect, found)
            self.northwest.query(range_rect, found)
            self.southeast.query(range_rect, found)
            self.southwest.query(range_rect, found)
        return found