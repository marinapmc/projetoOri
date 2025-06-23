# main.py
import pygame
import sys
import math
from pygame import Rect

from config import *
from entities import Building, Bus
from quadtree import QuadTree

def main():
    # Inicializa o Pygame e cria a janela
    pygame.init()
    
    # Define a tela e o relogio
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pygame.display.set_caption("Campus Defense")

    # Função para reiniciar o jogo
    def reset_game():
        return [], True, "AT", Bus(BUS_PATH, passengers=20)

    buildings, placing, current_type, bus = reset_game()

    while True:
        screen.fill(GREEN) # Limpa a tela com a cor verde
        current_time = pygame.time.get_ticks() # Obtém o tempo atual em milissegundos

        for event in pygame.event.get(): # Processa os eventos
            if event.type == pygame.QUIT: # Se o evento for de sair, fecha o jogo
                pygame.quit()
                sys.exit()

            # Se estiver colocando um edifício e o evento for de clique do mouse
            if placing and event.type == pygame.MOUSEBUTTONDOWN:
                for sx, sy in BUILDING_SLOTS:
                    # Verifica se o clique está próximo de um slot de construção
                    if math.hypot(event.pos[0] - sx, event.pos[1] - sy) < 20:
                        if not any(math.hypot(b.x - sx, b.y - sy) < 5 for b in buildings):
                            buildings.append(Building(sx, sy, current_type))

            # Se estiver colocando um edifício e o evento for de tecla pressionada
            if placing and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Se a tecla for espaço, para de colocar edifícios
                    placing = False
                elif event.key == pygame.K_1:  # Se a tecla for 1, define o tipo de edifício como AT
                    current_type = "AT"
                elif event.key == pygame.K_2: # Se a tecla for 2, define o tipo de edifício como Departamento
                    current_type = "Especial"

            # Se não estiver colocando edifícios e o evento for de tecla pressionada
            if not placing and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Se a tecla for R, reinicia o jogo
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
