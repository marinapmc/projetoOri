# main.py
import pygame
import random

from config import (
    BUILDING_SLOT_TYPES, GREEN, WIDTH, HEIGHT, FPS, TITLE, BUILDING_SLOTS, STARTING_MONEY,
    BUS_PATH, TIME_START, TIME_END, TIME_SPEED,
    BUS_SPAWN_SCHEDULE, TOTAL_DAY_SECONDS, MAX_BUILDING_RANGE, BUILDING_TYPES, GRAY, BLACK
)
from quadtree import QuadTree, Rect
from entities import Building, Bus

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(TITLE)
pygame.font.init()

clock = pygame.time.Clock()

# Fontes
FONT_HUD  = pygame.font.SysFont(None, 24)
FONT_SLOT = pygame.font.SysFont(None, 18)
FONT_BUS  = pygame.font.SysFont(None, 20)

# Função para obter o intervalo de spawn de ônibus com base no horário
# Retorna o intervalo em segundos ou None se não puder spawnar
# durante aquele horário
def get_spawn_params(hour):
    for start, end, interval, min_p, max_p in BUS_SPAWN_SCHEDULE:
        if start <= hour < end:
            return interval, min_p, max_p
    
    return None, None, None

def main():
    # Variáveis do jogo
    money = {'amount': STARTING_MONEY} # Inicializa o dinheiro do jogador
    score = {'amount': 100}  # Inicializa a vida do jogador
    boundary = Rect(0, 0, WIDTH, HEIGHT)
    qt = QuadTree(boundary)  # Inicializar o quadtree
    buildings = {} # Dicionário para armazenar as construções
    slots = [pygame.Rect(x, y, h, w) for x, y, h, w in BUILDING_SLOTS] 
    buses = [] # Lista para armazenar os ônibus
    spawn_timer = 0 # temporizador para spawn de ônibus
    time_of_day = TIME_START  # Guardar o horário do jogo

    running = True
    while running:
        dt = clock.tick(FPS) / 1000 # Tempo delta em segundos

        # Atualizar horário do jogo
        time_of_day += dt * TIME_SPEED

        # Se o horário ultrapassar o fim do dia, encerra o jogo
        if time_of_day >= TIME_END:
            # TODO: Implementar lógica de fim de dia
            print("Fim do dia!")
            running = False

        # Detecta hover em slots
        mx, my = pygame.mouse.get_pos()

        hovered_slot = None

        for i, slot in enumerate(slots):
            if slot.collidepoint(mx, my):
                hovered_slot = i
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                break
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Eventos
        for e in pygame.event.get():
            # Se aplicativo for fechado
            if e.type == pygame.QUIT: 
                running = False
            
            # Se clicou com o botão esquerdo do mouse
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and hovered_slot is not None:
                idx = hovered_slot
                btype = BUILDING_SLOT_TYPES[idx]

                # Verifica se o slot já tem um prédio construído
                if idx not in buildings:
                    cost = BUILDING_TYPES[btype]['base_cost']

                    # Se tem dinheiro suficiente, constrói o prédio
                    if money['amount'] >= cost:
                        money['amount'] -= cost
                        b = Building(btype, slots[idx], money)
                        buildings[idx] = b
                        qt.insert(b)
                else:
                    buildings[idx].upgrade()

        # spawn de ônibus com número de passageiros aleatório
        if TIME_START <= time_of_day < TIME_END:
            spawn_timer += dt
            interval, min_p, max_p = get_spawn_params(time_of_day)
            if interval and spawn_timer >= interval:
                count = random.randint(min_p, max_p)
                bus = Bus(BUS_PATH)
                bus.passengers = count
                buses.append(bus)
                spawn_timer = 0

        # Atualiza os ônibus
        for bus in list(buses):
            bus.update(dt) # Atualiza a posição do ônibus

            if bus.finished: # Se o ônibus chegou ao final
                buses.remove(bus) # Remove o ônibus da lista
                
                if bus.passengers > 0: # Se o ônibus tem passageiros
                    print("Chegou ao destino com passageiros!")
                    score['amount'] -= int(bus.passengers) # Perde um ponto por passageiro
                else: # Se o ônibus chegou vazio
                    print("Chegou ao destino vazio!")
                    money['amount'] += 100  # Ganha 100 pontos por ônibus vazio

        if score['amount'] <= 0: # Se perdeu todos os pontos
            print("Game Over! Você perdeu todos os pontos!")
            running = False

        # Ataque das torres
        for bus in buses:
            attack_rect = Rect(
                bus.bounds[0] - MAX_BUILDING_RANGE,
                bus.bounds[1] - MAX_BUILDING_RANGE,
                bus.bounds[2] + 2 * MAX_BUILDING_RANGE,
                bus.bounds[3] + 2 * MAX_BUILDING_RANGE
            )

            for b in qt.query(attack_rect):
                if b.can_attack(bus):
                    bus.passengers -= b.damage * dt

        # Desenha os elementos na tela
        screen.fill(GRAY)

        # Desenha slots
        for i, slot in enumerate(slots):
            color = GREEN if i == hovered_slot else BLACK
            pygame.draw.rect(screen, color, slot, 2)
            txt = FONT_SLOT.render(BUILDING_SLOT_TYPES[i], True, BLACK)
            tx = slot.x + slot.w//2 - txt.get_width()//2
            ty = slot.y + slot.h//2 - txt.get_height()//2
            screen.blit(txt, (tx, ty))

        for b in buildings.values():
            b.draw(screen)
            
        for bus in buses:
            bus.draw(screen, FONT_BUS)

        # HUD
        h = int(time_of_day)
        m = int((time_of_day - h) * 60)
        time_str = f"{h}:{m:02d}"
        txt = FONT_HUD.render(
            f"Money: {int(money['amount'])} | Horário: {time_str} | Vida: {score['amount']}", True, BLACK
        )

        screen.blit(txt, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
