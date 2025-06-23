# main.py
import pygame
import sys
import math
from pygame import Rect
import random


from config import *
from entities import Building, Bus
from quadtree import QuadTree

def main():
    # Inicializa o Pygame e cria a janela
    pygame.init()
    
    # Define a tela e o relogio
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Configurações do relógio do jogo
    REAL_DAY_DURATION = 6 * 60 * 1000  # 9 minutos em milissegundos
    START_TIME = 6 * 60  # 6:00 AM em minutos
    END_TIME = 19 * 60   # 24:00 (meia-noite) em minutos

    # Intensidade por hora do dia (das 6h às 18h)
    bus_spawn_schedule = {
        6: 1, 7: 3, 8: 1, 9: 2, 10: 1, 11: 2,
        12: 2, 13: 3, 14: 1, 15: 2, 16: 1, 17: 2, 18: 4
    }
    # Faixas de passageiros por intensidade
    passenger_ranges = {
        1: (10, 30),
        2: (30, 60),
        3: (60, 85),
        4: (85, 100)
    }

    # Controle de spawns realizados
    spawned_buses = {}

    clock = pygame.time.Clock()

    pygame.display.set_caption("Campus Defense")

    # Função para reiniciar o jogo
    def reset_game():
        return [], True, "AT", []  # Lista de ônibus vazia

    buildings, placing, current_type, bus = reset_game()
    start_ticks = pygame.time.get_ticks()

    def spawn_buses_for_hour(game_hour, game_minute, buses):
        intensity = bus_spawn_schedule.get(game_hour, 0)
        if intensity == 0:
            return

        key = (game_hour, intensity)
        if key not in spawned_buses:
            spawned_buses[key] = []

        total_spawns = intensity
        interval = 60 / intensity  # intervalo em minutos

        for i in range(total_spawns):
            scheduled_minute = int(i * interval)
            if scheduled_minute == game_minute and scheduled_minute not in spawned_buses[key]:
                min_p, max_p = passenger_ranges[intensity]
                passengers = random.randint(min_p, max_p)
                buses.append(Bus(BUS_PATH, passengers=passengers))
                spawned_buses[key].append(scheduled_minute)

    buses = []

    while True:
        screen.fill(GREEN) # Limpa a tela com a cor verde
        current_time = pygame.time.get_ticks() # Obtém o tempo atual em milissegundos
        # Calcula tempo decorrido e converte para hora do jogo
        elapsed = min(current_time - start_ticks, REAL_DAY_DURATION)
        game_minutes = START_TIME + (elapsed / REAL_DAY_DURATION) * (END_TIME - START_TIME)
        game_hour = int(game_minutes // 60)
        game_minute = int(game_minutes % 60)
        spawn_buses_for_hour(game_hour, game_minute, buses)
        game_clock_text = f"{game_hour:02d}:{game_minute:02d}"


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
        for bus in buses:
            bus.update()
            bus.draw(screen)

        if elapsed == REAL_DAY_DURATION:
            font = pygame.font.SysFont(None, 48)
            msg = "Vitória!"
            text = font.render(msg + " (aperte R para reiniciar)", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))

        # Exibe o relógio na tela
        font = pygame.font.SysFont(None, 36)
        clock_surface = font.render(game_clock_text, True, (255, 255, 255))  # texto branco
        screen.blit(clock_surface, (WIDTH - 100, 10))  # canto superior direito

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
