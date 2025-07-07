# main.py
import sys
import pygame
import random

from config import (
    BUILDING_SLOT_TYPES, GREEN, WIDTH, HEIGHT, FPS, TITLE, BUILDING_SLOTS, STARTING_MONEY,
    BUS_PATH, TIME_START, TIME_END, TIME_SPEED,
    BUS_SPAWN_SCHEDULE, TOTAL_DAY_SECONDS, MAX_BUILDING_RANGE, BUILDING_TYPES, GRAY, BLACK
)
from quadtree import QuadTree, Rect
from entities import Building, Bus

# Estados do jogo
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_HELP = "help"

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("assets/background.png").convert()

building_images = {
    "AT4_1": pygame.image.load("assets/AT4_1.png").convert_alpha(),
    "AT4_2": pygame.image.load("assets/AT4_2.png").convert_alpha(),
    "AT5_1": pygame.image.load("assets/AT5_1.png").convert_alpha(),
    "AT5_2": pygame.image.load("assets/AT5_2.png").convert_alpha(),
    "AT7_1": pygame.image.load("assets/AT7_1.png").convert_alpha(),
    "AT7_2": pygame.image.load("assets/AT7_2.png").convert_alpha(),
    "AT10_1": pygame.image.load("assets/AT10_1.png").convert_alpha(),
    "AT10_2": pygame.image.load("assets/AT10_2.png").convert_alpha(),
    "DEMA_1": pygame.image.load("assets/DEMA_1.png").convert_alpha(),
    "DEMA_2": pygame.image.load("assets/DEMA_2.png").convert_alpha(),
    "DEMA_3": pygame.image.load("assets/DEMA_3.png").convert_alpha(),
    "DEF_1": pygame.image.load("assets/DEF_1.png").convert_alpha(),
    "DEF_2": pygame.image.load("assets/DEF_2.png").convert_alpha(),
    "DEF_3": pygame.image.load("assets/DEF_3.png").convert_alpha(),
    "BCO_1": pygame.image.load("assets/BCO_1.png").convert_alpha(),
    "BCO_2": pygame.image.load("assets/BCO_2.png").convert_alpha(),
    "BCO_3": pygame.image.load("assets/BCO_3.png").convert_alpha(),
    "BCO_4": pygame.image.load("assets/BCO_4.png").convert_alpha(),
}

bus_images = {
    "BUS_1": pygame.image.load("assets/BUS_1.gif").convert_alpha(),
    "BUS_2": pygame.image.load("assets/BUS_2.gif").convert_alpha(),
    "BUS_3": pygame.image.load("assets/BUS_3.gif").convert_alpha(),
    "BUS_4": pygame.image.load("assets/BUS_4.gif").convert_alpha(),
}

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

def update_game(dt, state):
    # Atualizar horário do jogo
    state["time_of_day"] += dt * TIME_SPEED

    # spawn de ônibus com número de passageiros aleatório
    if TIME_START <= state["time_of_day"] < TIME_END:
        state["spawn_timer"] += dt

        interval, min_p, max_p = get_spawn_params(state["time_of_day"])

        if interval and state["spawn_timer"] >= interval:
            count = random.randint(min_p, max_p)

            bus = Bus(image_dict=bus_images, student_count=count)
            
            state["buses"].append(bus)
            state["spawn_timer"] = 0

    # Atualiza os ônibus
    for bus in list(state["buses"]):
        bus.update(dt) # Atualiza a posição do ônibus

        if bus.finished: # Se o ônibus chegou ao final
            state["buses"].remove(bus) # Remove o ônibus da lista
            
            if bus.passengers > 0: # Se o ônibus tem passageiros
                print("Chegou ao destino com passageiros!")
                state["score"]['amount'] -= int(bus.passengers) # Perde um ponto por passageiro
            else: # Se o ônibus chegou vazio
                print("Chegou ao destino vazio!")
                state["money"]['amount'] += 100  # Ganha 100 pontos por ônibus vazio
    
    for building in state["buildings"].values():
        building.update(dt)

    # Cria uma quadtree com os prédios
    qt = QuadTree(Rect(0, 0, WIDTH, HEIGHT))
    for building in state["buildings"].values():
        x, y, w, h = building.bounds
        cx = x + w // 2
        cy = y + h // 2
        r = building.range
        qt.insert(building)

    # Para cada ônibus, verifica se há prédios dentro do alcance
    for bus in state["buses"]:
        if bus.is_destroyed():
            continue

        bx, by = bus.get_position()

        range_box = Rect(bx - MAX_BUILDING_RANGE, by - MAX_BUILDING_RANGE,
                 MAX_BUILDING_RANGE * 2, MAX_BUILDING_RANGE * 2)
        candidates = qt.query(range_box)


        for building in candidates:
            if building.try_attack(bus):
                break  # só sai do loop de prédios se ataque foi bem-sucedido
            
def draw_game(screen, state):
        # Desenha o background
        screen.blit(background, (0, 0)) 

        # Desenha slots
        for i, slot in enumerate(state["slots"]):
            color = GREEN # if i == hovered_slot else BLACK TODO: Implementar hover
            
            pygame.draw.rect(screen, color, slot, 2)

            txt = FONT_SLOT.render(BUILDING_SLOT_TYPES[i], True, BLACK)

            tx = slot.x + slot.w//2 - txt.get_width()//2
            ty = slot.y + slot.h//2 - txt.get_height()//2

            screen.blit(txt, (tx, ty))

        for b in state["buildings"].values():
            b.draw(screen)
            
        for bus in state["buses"]:
            bus.draw(screen, FONT_BUS)

        # HUD
        h = int(state["time_of_day"])
        m = int((state["time_of_day"] - h) * 60)
        time_str = f"{h}:{m:02d}"
        txt = FONT_HUD.render(
            f"Money: {int(state['money']['amount'])} | Horário: {time_str} | Vida: {state['score']['amount']}", True, BLACK
        )

        screen.blit(txt, (10, 10))

# Criar retângulos para os botões
def create_button(text, x, y, w, h, font):
    rect = pygame.Rect(x, y, w, h)
    surface = font.render(text, True, (255, 255, 255))
    return {"rect": rect, "text": text, "surface": surface}

def draw_button(screen, button):
    pygame.draw.rect(screen, (100, 100, 100), button["rect"])
    text_rect = button["surface"].get_rect(center=button["rect"].center)
    screen.blit(button["surface"], text_rect)

def reset_game_state():
    return {
        "money": {'amount': STARTING_MONEY},
        "score": {'amount': 100},
        "time_of_day": TIME_START,
        "buildings": {},
        "buses": [],
        "qt": QuadTree(Rect(0, 0, WIDTH, HEIGHT)),
        "slots": [pygame.Rect(x, y, h, w) for x, y, h, w in BUILDING_SLOTS],
        "spawn_timer": 0
    }

def main():
    # Variáveis da HUD    
    screen_state = STATE_MENU

    # Botões do jogo
    buttons_menu = [
        create_button("Jogar", WIDTH//2 - 75, 200, 150, 50, FONT_HUD),
        create_button("Ajuda", WIDTH//2 - 75, 270, 150, 50, FONT_HUD),
        create_button("Sair", WIDTH//2 - 75, 340, 150, 50, FONT_HUD)
    ]
    button_help_back = create_button("Voltar", WIDTH//2 - 75, HEIGHT - 80, 150, 50, FONT_HUD)
    button_exit_to_menu = create_button("Sair", 800, 580, 150, 50, FONT_HUD)

    # Estado do jogo
    game_state = {
        "money": {'amount': STARTING_MONEY},
        "score": {'amount': 100},
        "time_of_day": TIME_START,
        "buildings": {},
        "buses": [],
        "qt": QuadTree(Rect(0, 0, WIDTH, HEIGHT)),
        "slots": [pygame.Rect(x, y, h, w) for x, y, h, w in BUILDING_SLOTS],
        "spawn_timer": 0
    }
    
    running = True

    while running:
        dt = clock.tick(FPS) / 1000 # Tempo delta em segundos

        screen.fill((0, 0, 0))  # fundo preto por padrão

        # Detecta hover em slots
        mx, my = pygame.mouse.get_pos()

        #print(f"Mouse position: {mx}, {my}")

        # Eventos
        for e in pygame.event.get():
            # Se aplicativo for fechado
            if e.type == pygame.QUIT: 
                running = False
            
            # Se clicou com o botão esquerdo do mouse
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                # Se estiver no menu
                if screen_state == STATE_MENU:
                        if buttons_menu[0]["rect"].collidepoint((mx, my)):
                            screen_state = STATE_GAME
                            game_state = reset_game_state()  # Reseta o estado do jogo

                        elif buttons_menu[1]["rect"].collidepoint((mx, my)):
                            screen_state = STATE_HELP
                            
                        elif buttons_menu[2]["rect"].collidepoint((mx, my)):
                            pygame.quit()
                            sys.exit()

                # Se estiver na tela de ajuda
                elif screen_state == STATE_HELP:
                    if button_help_back["rect"].collidepoint((mx, my)):
                        screen_state = STATE_MENU

                # Se estiver no jogo
                elif screen_state == STATE_GAME:
                    hovered_slot = None

                    for i, slot in enumerate(game_state["slots"]):
                        if slot.collidepoint(mx, my):
                            hovered_slot = i
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            break
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                    if button_exit_to_menu["rect"].collidepoint((mx, my)):
                        screen_state = STATE_MENU

                    if hovered_slot is not None:
                        idx = hovered_slot
                        btype = BUILDING_SLOT_TYPES[idx]

                        # Verifica se o slot já tem um prédio construído
                        if idx not in game_state["buildings"]:
                            cost = BUILDING_TYPES[btype]['base_cost']

                            # Se tem dinheiro suficiente, constrói o prédio
                            if game_state["money"]['amount'] >= cost:
                                game_state["money"]['amount'] -= cost

                                b = Building(btype, game_state["slots"][idx], game_state["money"], building_images)
                                
                                game_state["buildings"][idx] = b
                                game_state["qt"].insert(b)
                        else:
                            game_state["buildings"][idx].upgrade()
               
        # Desenha tudo na tela
        if screen_state == STATE_MENU:
            title = FONT_HUD.render("Tower Defense na UFSCar", True, (255, 255, 255))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

            for b in buttons_menu:
                draw_button(screen, b)

        elif screen_state == STATE_HELP:
            help_lines = [
                "Objetivo: impedir que os onibus cheguem ao final",
                "Coloque torres nos slots do mapa",
                "Cada torre reduz o número de alunos nos ônibus",
                "Você perde pontos com os alunos que passam",
                "O dia acaba após certo tempo.",
            ]
            for i, line in enumerate(help_lines):
                text = FONT_HUD.render(line, True, (255, 255, 255))
                screen.blit(text, (50, 50 + i*40))

            draw_button(screen, button_help_back)

        elif screen_state == STATE_GAME:
            update_game(dt, game_state)  # Atualiza o estado do jogo
            draw_game(screen, game_state) # Desenha o estado do jogo

            # Se o horário ultrapassar o fim do dia, encerra o jogo
            if game_state["time_of_day"] >= TIME_END:
                # TODO: Implementar lógica de fim de dia
                print("Fim do dia!")
                running = False

            if game_state["score"]['amount'] <= 0: # Se perdeu todos os pontos
                # TODO: Implementar lógica de fim de jogo
                print("Game Over! Você perdeu todos os pontos!")
                running = False

            draw_button(screen, button_exit_to_menu)

        pygame.display.flip()

    input("Pressione Enter para sair...")

    # Finaliza o Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
