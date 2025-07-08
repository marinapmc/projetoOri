# entities.py
import math
import pygame
from config import BUILDING_TYPES, BUS_PATH, GREEN, MAX_BUILDING_RANGE, RED

class Building:
    def __init__(self, btype, slot_rect, money_ref, image_dict):
        self.type = BUILDING_TYPES[btype]
        self.bounds = slot_rect
        self.range = min(self.type['range'], MAX_BUILDING_RANGE)
        self.damage = self.type['damage']
        self.fire_rate = self.type['fire_rate']
        self.fire_timer = 0.0
        self.level = 1
        self.money = money_ref
        self.image_dict = image_dict
        self.center = (slot_rect[0] + slot_rect[2] // 2,
                       slot_rect[1] + slot_rect[3] // 2)
        self.upgrade_cost = self.type['upgrade_cost']

    def update(self, dt):
        self.fire_timer += dt

    def can_upgrade(self):
        return (self.level < self.type['max_level'] and
                self.money['amount'] >= self.upgrade_cost)

    def upgrade(self):
        if self.can_upgrade():
            self.money['amount'] -= self.upgrade_cost
            self.level += 1
            self.range = self.type['range'] + 50
            self.fire_rate = self.type['fire_rate'] / 2

    
    def try_attack(self, bus):
        if self.fire_timer < self.fire_rate:
            return False
        if bus.is_destroyed() or bus.student_count <= 0:
            return False


        sx, sy, sw, sh = self.bounds
        cx, cy = sx + sw // 2, sy + sh // 2
        bx, by = bus.get_position()

        if math.hypot(bx - cx, by - cy) <= self.range:
            bus.take_damage(self.damage)
            self.fire_timer = 0
            return True
       
        return False

    def draw(self, surface):
        bx, by, bw, bh = self.bounds
        b_left = bx
        b_bottom = by + bh

        cx = bx + bw // 2
        cy = by + bh // 2
        radius = self.range 
        
        img = self.image_dict.get(f"{self.type['name']}_{self.level}", None)

        if img:
            img_w, img_h = img.get_size()

            draw_x = b_left
            draw_y = b_bottom - img_h

            surface.blit(img, (draw_x, draw_y))
        else:
            pygame.draw.rect(surface, GREEN, self.bounds)
            
        # pygame.draw.circle(surface, GREEN, (cx, cy), radius, width=1)

class Bus:
    def __init__(self, image_dict, student_count=10, speed=40):
        self.image_dict = image_dict
        self.path = BUS_PATH
        self.speed = speed
        self.index = 0
        self.x, self.y = self.path[0]
        self.target = self.path[1]
        self.student_count = student_count
        self.destroyed = False
        self.font = pygame.font.SysFont(None, 20)

    def update(self, dt):
        if self.destroyed:
            return

        tx, ty = self.target
        dx = tx - self.x
        dy = ty - self.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < 1:
            self.index += 1
            if self.index + 1 >= len(self.path):
                self.destroyed = True  # Chegou ao fim
                return
            self.target = self.path[self.index + 1]
        else:
            norm = self.speed * dt / distance
            self.x += dx * norm
            self.y += dy * norm

    def get_direction(self):
        if self.index + 1 < len(self.path):
            tx, ty = self.path[self.index + 1]
            dx = tx - self.x
            dy = ty - self.y
            return dx, dy
        return 0, 0

    def draw(self, surface, font):
        if not self.destroyed:
            x, y = self.get_direction()

            x, y = int(x), int(y)

            image = "BUS_1"

            if x == 0: # Vertical
                if y > 0:
                    image = "BUS_3"
                elif y < 0:
                    image = "BUS_1"

            if y == 0: # Horizontal
                if x > 0:
                    image = "BUS_2"
                elif x < 0:
                    image = "BUS_4"

            rect = self.image_dict[image].get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image_dict[image], rect)

            # Desenha o número de passageiros acima do ônibus
            text = font.render(str(max(0, self.student_count)), True, (255, 255, 255))
            text_rect = text.get_rect(center=(int(self.x), int(self.y) - rect.height // 2 - 10))
            surface.blit(text, text_rect)

    def get_position(self):
        return self.x, self.y

    def take_damage(self, amount):
        self.student_count -= amount
        self.student_count = max(0, self.student_count)  # evita ficar negativo

    def is_destroyed(self):
        return self.destroyed
    
class StudentProjectile:
    def __init__(self, start_pos, end_pos, duration=0.8):
        self.start_x, self.start_y = start_pos
        self.end_x, self.end_y = end_pos
        self.duration = duration
        self.elapsed = 0
        self.finished = False

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.finished = True

    def draw(self, surface):
        t = self.elapsed / self.duration
        t = min(max(t, 0), 1)

        # Interpolação linear
        x = self.start_x + (self.end_x - self.start_x) * t
        y = self.start_y + (self.end_y - self.start_y) * t

        # Altura da parábola (ajuste o valor 100 se quiser mais/menos curva)
        parabola_height = -20 * (4 * (t - 0.5)**2 - 1)
        y += parabola_height

        pygame.draw.rect(surface, RED, (x - 3, y - 3, 6, 6))  # quadradinho vermelho