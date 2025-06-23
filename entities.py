# entities.py
import pygame
import math
from pygame import Rect
from config import BUILDING_TYPES, WHITE, GRAY, YELLOW

class Building:
    def __init__(self, x, y, tipo):
        # Cordenadas do centro do predio
        self.x = x
        self.y = y
        
        # Pega o tipo de predio correspondente 
        props = BUILDING_TYPES[tipo] 

        # Retira de props os atributos do onibus
        self.radius = props["radius"]
        self.damage = props["damage"]
        self.cooldown = props["cooldown"]
        self.color = props["color"]
        self.last_attack = 0

    def draw(self, screen):
        # Desenha o objeto na posicao correta com a cor correta
        pygame.draw.circle(screen, self.color, (self.x, self.y), 20)
        pygame.draw.circle(screen, GRAY, (self.x, self.y), self.radius, 1)

    def try_attack(self, bus, current_time):
        # Verifica se o onibus esta dentro do raio de ataque e se o cooldown ja passou
        if current_time - self.last_attack >= self.cooldown:
            # Verifica a distancia entre o onibus e o predio
            if math.hypot(bus.x - self.x, bus.y - self.y) <= self.radius:
                # Se o onibus estiver dentro do raio, causa dano ao onibus
                if bus.passengers > 0:
                    bus.passengers -= self.damage
                    self.last_attack = current_time

class Bus:
    def __init__(self, path, passengers):
        # Inicializa o onibus com um caminho e o numero de passageiros
        self.path = path
        self.index = 0
        self.x, self.y = self.path[0]
        self.speed = 1.5
        self.passengers = passengers

    def update(self):
        # Se o onibus nao chegou ao final do caminho, move para o proximo ponto
        if self.index < len(self.path) - 1:
            target = self.path[self.index + 1]
            dx, dy = target[0] - self.x, target[1] - self.y

            # Calcula a distancia para o proximo ponto e move o onibus
            dist = math.hypot(dx, dy)

            # Se a distancia for menor que a velocidade do onibus, avanca para o proximo ponto
            if dist < self.speed:
                self.index += 1
            else:
                # Move o onibus na direcao do proximo ponto
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed

    def draw(self, screen):
        # Desenha o onibus como um retangulo amarelo
        pygame.draw.rect(screen, YELLOW, Rect(self.x - 10, self.y - 10, 20, 20))
        font = pygame.font.SysFont(None, 20)
        text = font.render(f"{self.passengers}", True, WHITE)
        screen.blit(text, (self.x - 10, self.y - 25))
