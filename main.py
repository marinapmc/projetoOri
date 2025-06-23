# main.py
import pygame
import sys
import math
from pygame import Rect

from config import *
from entities import Building, Bus
from quadtree import QuadTree

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Campus Defense")
    clock = pygame.time.Clock()

    def reset_game():
        return [], True, "AT", Bus(BUS_PATH, passengers=20)

    buildings, placing, current_type, bus = reset_game()

    while True:
        screen.fill(GREEN)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if placing and event.type == pygame.MOUSEBUTTONDOWN:
                for sx, sy in BUILDING_SLOTS:
                    if math.hypot(event.pos[0] - sx, event.pos[1] - sy) < 20:
                        if not any(math.hypot(b.x - sx, b.y - sy) < 5 for b in buildings):
                            buildings.append(Building(sx, sy, current_type))
            if placing and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    placing = False
                elif event.key == pygame.K_1:
                    current_type = "AT"
                elif event.key == pygame.K_2:
                    current_type = "Especial"
            if not placing and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    buildings, placing, current_type, bus = reset_game()

        qt = QuadTree(Rect(0, 0, WIDTH, HEIGHT), capacity=4)
        for b in buildings:
            qt.insert(b)

        if not placing:
            bus.update()
            nearby_buildings = []
            qt.query(Rect(bus.x - 120, bus.y - 120, 240, 240), nearby_buildings)
            for b in nearby_buildings:
                b.try_attack(bus, current_time)

        pygame.draw.lines(screen, WHITE, False, BUS_PATH, 4)
        for slot in BUILDING_SLOTS:
            pygame.draw.circle(screen, WHITE, slot, 20, 2)
        for b in buildings:
            b.draw(screen)
        bus.draw(screen)

        if bus.index >= len(bus.path) - 1 or bus.passengers <= 0:
            font = pygame.font.SysFont(None, 48)
            msg = "Vitória!" if bus.passengers <= 0 else "Fim da fase"
            text = font.render(msg + " (aperte R para reiniciar)", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
