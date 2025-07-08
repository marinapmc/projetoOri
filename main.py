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
from entities import Building, Bus, StudentProjectile

# Estados do jogo
STATE_WAIT = "wait"
STATE_GAME = "game"
STATE_HELP = "help"
STATE_PAUSE = "pause"

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("assets/BACKGROUND.png").convert()
icon_vida = pygame.image.load("assets/LIFE.png").convert_alpha()
icon_dinheiro = pygame.image.load("assets/MONEY.png").convert_alpha()

# Carrega as imagens dos prédios
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
    "DF_1": pygame.image.load("assets/DF_1.png").convert_alpha(),
    "DF_2": pygame.image.load("assets/DF_2.png").convert_alpha(),
    "DF_3": pygame.image.load("assets/DF_3.png").convert_alpha(),
    "BCO_1": pygame.image.load("assets/BCO_1.png").convert_alpha(),
    "BCO_2": pygame.image.load("assets/BCO_2.png").convert_alpha(),
    "BCO_3": pygame.image.load("assets/BCO_3.png").convert_alpha(),
    "BCO_4": pygame.image.load("assets/BCO_4.png").convert_alpha(),
}

# Carrega as imagens dos botões
button_images = {
    "play": pygame.image.load("assets/BUTTON_PLAY.png").convert_alpha(),
    "restart": pygame.image.load("assets/BUTTON_RESTART.png").convert_alpha(),
    "quit": pygame.image.load("assets/BUTTON_QUIT.png").convert_alpha(),
    "help": pygame.image.load("assets/BUTTON_HELP.png").convert_alpha(),
    "back": pygame.image.load("assets/BUTTON_BACK.png").convert_alpha(),
    "resume": pygame.image.load("assets/BUTTON_RESUME.png").convert_alpha(),
    "pause": pygame.image.load("assets/BUTTON_PAUSE.png").convert_alpha(),
}

# Botões de controle do HUD
buttons_ui = {
    "play":    {"image": button_images["play"],    "rect": pygame.Rect(850, 550, 93, 34), "action": "play"},
    "resume":  {"image": button_images["resume"],  "rect": pygame.Rect(850, 510, 93, 34), "action": "resume"},
    "restart": {"image": button_images["restart"], "rect": pygame.Rect(850, 550, 93, 34), "action": "restart"},
    "quit":    {"image": button_images["quit"],    "rect": pygame.Rect(850, 590, 93, 34), "action": "quit"},
    "back":    {"image": button_images["back"],    "rect": pygame.Rect(460, 510, 93, 34), "action": "back"},
    "help":    {"image": button_images["help"],    "rect": pygame.Rect(910, 30, 34, 34),  "action": "help"},
    "pause":   {"image": button_images["pause"],   "rect": pygame.Rect(860, 30, 34, 34),  "action": "pause"},
}

# Carrega as imagens dos ônibus
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
FONT_HUD  = pygame.font.Font("assets/VT323-Regular.ttf", 24)
FONT_SLOT = pygame.font.Font("assets/PressStart2P-Regular.ttf", 9)
FONT_BUS  = pygame.font.Font("assets/PressStart2P-Regular.ttf", 10)

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

    for bus in list(state["buses"]):
        bus.update(dt) # Atualiza a posição do ônibus

        if bus.is_destroyed():
            state["buses"].remove(bus)

            if bus.student_count > 0:
                print("Chegou ao destino com passageiros!")
                state["score"]['amount'] -= int(bus.student_count)  # Perde pontos
            else:
                print("Chegou ao destino vazio!")
                state["money"]['amount'] += 100  # Ganha dinheiro

    
    for building in state["buildings"].values():
        building.update(dt)

    # Atualiza os projéteis (partículas visuais dos estudantes)
    for p in list(state["projectiles"]):
        p.update(dt)

        if p.finished:
            state["projectiles"].remove(p)

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
                # Adiciona um projétil visual da remoção de estudante
                projectile = StudentProjectile(bus.get_position(), building.center)
                state["projectiles"].append(projectile)

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

        for bus in state["buses"]:
            bus.draw(screen, FONT_BUS)

        for b in state["buildings"].values():
            b.draw(screen)

        for p in state["projectiles"]:
            p.draw(screen)

        # HUD
        h = int(state["time_of_day"])
        m = int((state["time_of_day"] - h) * 60)
        time_str = f"{h}:{m:02d}"
        txt = FONT_HUD.render(
            f"Money: {int(state['money']['amount'])} | Horário: {time_str} | Vida: {state['score']['amount']}", True, BLACK
        )

        screen.blit(txt, (10, 10))

def draw_button(screen, button):
    # Cria uma surface do tamanho do botão com canal alpha
    rect_surface = pygame.Surface(button["rect"].size, pygame.SRCALPHA)

    # Cor com alpha (ex: preto transparente)
    rect_color = (0, 0, 0, 0)
    
    # Desenha o retângulo transparente na surface auxiliar
    pygame.draw.rect(rect_surface, rect_color, rect_surface.get_rect())

    # Blita a surface com o fundo transparente na posição do botão
    screen.blit(rect_surface, button["rect"].topleft)

    # Centraliza a imagem do botão dentro do retângulo
    rect = button["image"].get_rect(center=button["rect"].center)
    screen.blit(button["image"], rect)

def reset_game_state():
    return {
        "money": {'amount': STARTING_MONEY},
        "score": {'amount': 100},
        "time_of_day": TIME_START,
        "buildings": {},
        "buses": [],
        "projectiles": [],
        "qt": QuadTree(Rect(0, 0, WIDTH, HEIGHT)),
        "slots": [pygame.Rect(x, y, h, w) for x, y, h, w in BUILDING_SLOTS],
        "spawn_timer": 0
    }

def quit_game():
    pygame.quit()
    sys.exit()

def main():
    # Variáveis da HUD    
    screen_state = STATE_WAIT

    # Estado do jogo
    game_state = {
        "money": {'amount': STARTING_MONEY},
        "score": {'amount': 100},
        "time_of_day": TIME_START,
        "buildings": {},
        "buses": [],
        "projectiles": [],
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
                quit_game()
            
            # Se clicou com o botão esquerdo do mouse
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:

                # Se estiver na tela de ajuda
                if screen_state == STATE_HELP:
                    if buttons_ui["back"]["rect"].collidepoint((mx, my)):
                        if game_state["time_of_day"] > TIME_START:
                            screen_state = STATE_PAUSE
                        else:
                            screen_state = STATE_WAIT

                if screen_state == STATE_WAIT:
                    if buttons_ui["help"]["rect"].collidepoint((mx, my)):
                        screen_state = STATE_HELP

                    if buttons_ui["play"]["rect"].collidepoint((mx, my)):
                        screen_state = STATE_GAME

                    elif buttons_ui["quit"]["rect"].collidepoint((mx, my)):
                        quit_game()

                if screen_state == STATE_PAUSE:
                    if buttons_ui["help"]["rect"].collidepoint((mx, my)):
                        screen_state = STATE_HELP

                    elif buttons_ui["resume"]["rect"].collidepoint((mx, my)):
                        screen_state = STATE_GAME

                    elif buttons_ui["restart"]["rect"].collidepoint((mx, my)):
                        game_state = reset_game_state()
                        screen_state = STATE_WAIT

                    elif buttons_ui["quit"]["rect"].collidepoint((mx, my)):
                        quit_game()

                # Se estiver no jogo
                elif screen_state == STATE_GAME:
                    if buttons_ui["help"]["rect"].collidepoint((mx, my)):
                        screen_state = STATE_HELP

                    elif buttons_ui["pause"]["rect"].collidepoint((mx, my)):
                        screen_state = STATE_PAUSE

                    elif buttons_ui["quit"]["rect"].collidepoint((mx, my)):
                        quit_game()

                    hovered_slot = None

                    for i, slot in enumerate(game_state["slots"]):
                        if slot.collidepoint(mx, my):
                            hovered_slot = i
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            break
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

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

        if screen_state == STATE_HELP:
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

            draw_button(screen, buttons_ui["back"])  # Desenha o botão de voltar

        elif screen_state == STATE_WAIT:
            draw_game(screen, game_state)  # Sempre desenha o estado do jogo

            draw_button(screen, buttons_ui["help"])  # Desenha o botão de ajuda
            draw_button(screen, buttons_ui["play"])  # Desenha o botão de jogar
            draw_button(screen, buttons_ui["quit"])  # Desenha o botão de sair

        elif screen_state == STATE_PAUSE:
            draw_game(screen, game_state)  # Sempre desenha o estado do jogo

            draw_button(screen, buttons_ui["help"])  # Desenha o botão de ajuda
            draw_button(screen, buttons_ui["resume"])  # Desenha o botão de jogar
            draw_button(screen, buttons_ui["restart"]) # Desenha o botão de reiniciar
            draw_button(screen, buttons_ui["quit"])  # Desenha o botão de sair

        elif screen_state == STATE_GAME:
            update_game(dt, game_state)  # Atualiza o estado do jogo
            draw_game(screen, game_state)  # Sempre desenha o estado do jogo

            draw_button(screen, buttons_ui["help"])  # Desenha o botão de ajuda
            draw_button(screen, buttons_ui["pause"])  # Desenha o botão de jogar

            if game_state["time_of_day"] >= TIME_END:
                print("Fim do dia!")
                running = False # TODO: Implementar reinício do jogo

            if game_state["score"]['amount'] <= 0:
                print("Game Over! Você perdeu todos os pontos!")
                running = False # TODO: Implementar reinício do jogo

        pygame.display.flip()

    input("Pressione Enter para sair...")

    # Finaliza o Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
