# main.py
import sys
import pygame
import random

from config import (
    BUILDING_SLOT_TYPES, GREEN, WIDTH, HEIGHT, FPS, TITLE, STARTING_MONEY, TIME_START, TIME_END, TIME_SPEED,
    BUS_SPAWN_SCHEDULE, MAX_BUILDING_RANGE, BUILDING_TYPES, GRAY, BLACK, WHITE
)
from quadtree import QuadTree, Rect
from entities import Building, Bus, StudentProjectile

# Estados do jogo
STATE_WAIT = "wait"
STATE_GAME = "game"
STATE_HELP = "help"
STATE_PAUSE = "pause"
STATE_WIN = "win"
STATE_LOSE = "lose"

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("assets/BACKGROUND.png").convert()

title = pygame.image.load("assets/NOME_JOGO.png").convert_alpha()

icon_life = pygame.image.load("assets/ICON_LIFE.png").convert_alpha()
icon_money = pygame.image.load("assets/ICON_MONEY.png").convert_alpha()
icon_clock = pygame.image.load("assets/ICON_CLOCK.png").convert_alpha()

bar_outline = pygame.image.load("assets/BAR_OUTLINE.png").convert_alpha()
bar_fill = pygame.image.load("assets/BAR_FILL.png").convert_alpha()

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
    "back":    {"image": button_images["back"],    "rect": pygame.Rect(460, 550, 93, 34), "action": "back"},
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

# Slots para construir prédios (x, y, largura, altura)
BUILDING_SLOTS = [
    (155, 345, 77, 50), # AT10
    (308, 175, 77, 50), # AT4
    (695, 235, 77, 50), # AT5
    (837, 215, 77, 50), # AT7
    (200, 535, 143, 50), # Departamento Física
    (495, 190, 149, 50), # Departamento Materiais
    (265, 390, 140, 50), # BCO
]

pygame.display.set_caption(TITLE)

pygame.font.init()

clock = pygame.time.Clock()

# Fontes
FONT_HUD  = pygame.font.Font("assets/PressStart2P-Regular.ttf", 16)
FONT_SLOT = pygame.font.Font("assets/PressStart2P-Regular.ttf", 10)
FONT_BUS  = pygame.font.Font("assets/PressStart2P-Regular.ttf", 12)

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
                state["score"]['amount'] = max(0, state["score"]['amount'] - int(bus.student_count))  # Perde pontos
            else:
                state["money"]['amount'] += 50  # Ganha dinheiro

    
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

            # Se o slot não tiver um prédio construído
            if i not in state["buildings"]:
                # Desenha o slot com uma borda verde
                pygame.draw.rect(screen, GREEN, slot, 2)

                btype = BUILDING_SLOT_TYPES[i]
                cost = BUILDING_TYPES[btype]['base_cost']

                # Desenha o texto de custo do prédio
                txt = FONT_SLOT.render(f"${cost}", True, GREEN)

                tx = slot.x + slot.w // 2 - txt.get_width() // 2
                ty = slot.y + slot.h // 2 - txt.get_height() // 2 + 10

                screen.blit(txt, (tx, ty))

                # Desenha o texto do nome do prédio
                txt = FONT_SLOT.render(BUILDING_SLOT_TYPES[i], True, GREEN)

                tx = slot.x + slot.w // 2 - txt.get_width() // 2
                ty = slot.y + slot.h // 2 - txt.get_height() // 2 - 10

                screen.blit(txt, (tx, ty))
            
        for bus in state["buses"]:
            bus.draw(screen, FONT_BUS)

        for b in state["buildings"].values():
            b.draw(screen)

        for p in state["projectiles"]:
            p.draw(screen)

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

# Função para desenhar a barra de vida
def draw_health_bar(screen, state):
    x, y = 690, 590
    health = state["score"]['amount']

    fill_ratio = max(0, min(1, health / 100))  # Garante entre 0 e 1
    fill_width = int(200 * fill_ratio)

    if fill_width > 0:
        # Recorta a parte visível da imagem de preenchimento
        bar_fill_cropped = bar_fill.subsurface((0, 0, fill_width, 32)).copy()

        # Desenha um retângulo arredondado no formato desejado (máscara de borda esquerda)
        mask = pygame.Surface((fill_width, 32), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, fill_width, 32))

        # Aplica a máscara à imagem da barra (mantém só a parte arredondada)
        bar_fill_cropped.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Desenha o preenchimento
        screen.blit(bar_fill_cropped, (x + 45, y))

    # Desenha o contorno da barra por cima
    screen.blit(bar_outline, (x + 45, y))

    # Ícone de vida
    icon_rect = icon_life.get_rect(topleft=(x, y))
    screen.blit(icon_life, icon_rect)

# Função para desenhar o relógio na HUD
def draw_clock(screen, state):
    x, y = 70, 35

    # Texto do horário
    h = int(state["time_of_day"])
    m = int((state["time_of_day"] - h) * 60)
    time_str = f"{h}:{m:02d}"
    time_text = FONT_HUD.render(f"{time_str}", True, WHITE)
    time_rect = time_text.get_rect(topleft=(x + 50, y + 10))
    screen.blit(time_text, time_rect)

    # Ícone de relógio
    clock_icon_rect = icon_clock.get_rect(topleft=(x, y))
    screen.blit(icon_clock, clock_icon_rect)

# Função para desenhar o dinheiro na HUD
def draw_money(screen, state):
    x, y = 690, 540

    # Texto do dinheiro
    money_text = FONT_HUD.render(f"{int(state['money']['amount'])}", True, WHITE)
    money_rect = money_text.get_rect(topleft=(x + 50, y + 10))
    screen.blit(money_text, money_rect)

    # Ícone de dinheiro
    money_icon_rect = icon_money.get_rect(topleft=(x, y))
    screen.blit(icon_money, money_icon_rect)

def draw_overlay(screen, text):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # Fundo preto com transparência

    # Desenha o texto centralizado
    txt = FONT_HUD.render(text, True, WHITE)
    txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    screen.blit(overlay, (0, 0))  # Desenha o overlay
    screen.blit(txt, txt_rect)     # Desenha o texto
    pygame.display.flip()          # Atualiza a tela

def draw_title(screen):
    # Desenha o título do jogo no topo da tela
    title_rect = title.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title, title_rect)

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

# Função principal do jogo
def main():
    # Variáveis da HUD    
    screen_state = STATE_WAIT
    last_screen_draw = None

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

        # Detecta hover em slots
        mx, my = pygame.mouse.get_pos()

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

                    for hovered_slot, slot in enumerate(game_state["slots"]):
                        if slot.collidepoint((mx, my)):
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

                elif screen_state == STATE_WIN:
                    if buttons_ui["restart"]["rect"].collidepoint((mx, my)):
                        game_state = reset_game_state()
                        screen_state = STATE_WAIT

                    elif buttons_ui["quit"]["rect"].collidepoint((mx, my)):
                        quit_game()

                elif screen_state == STATE_LOSE:
                    if buttons_ui["restart"]["rect"].collidepoint((mx, my)):
                        game_state = reset_game_state()
                        screen_state = STATE_WAIT

                    elif buttons_ui["quit"]["rect"].collidepoint((mx, my)):
                        quit_game()

        if screen_state == STATE_HELP:
            if last_screen_draw != screen_state:
                screen.fill((0, 0, 0))

                draw_title(screen)  # Desenha o título do jogo

                help_lines = [
                    "- Impeça que os ônibus cheguem ao destino",
                    " com passageiros",
                    "- Construa torres clicando nos slots e atualize-as para",
                    " aumentar alcance e velocidade de ataque",
                    "- Cada torre consome dinheiro; planeje seu orçamento",
                    " entre construções e upgrades",
                    "- Observe o relógio do jogo e adapte sua estratégia",
                    " aos picos de tráfego",
                    "- Ganhe dinheiro ao esvaziar totalmente um ônibus e ",
                    " perca pontos quando alguém escapar"
                ]
                for i, line in enumerate(help_lines):
                    text = FONT_HUD.render(line, True, (255, 255, 255))
                    screen.blit(text, (50, 120 + i*40))

                draw_button(screen, buttons_ui["back"])  # Desenha o botão de voltar

                last_screen_draw = screen_state  # Armazena o último estado desenhado

            if buttons_ui["back"]["rect"].collidepoint((mx, my)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif screen_state == STATE_WAIT:
            if last_screen_draw != screen_state:
                screen.fill((0, 0, 0))

                draw_game(screen, game_state)  # Sempre desenha o estado do jogo

                draw_title(screen)  # Desenha o título do jogo

                draw_button(screen, buttons_ui["help"])  # Desenha o botão de ajuda
                draw_button(screen, buttons_ui["play"])  # Desenha o botão de jogar
                draw_button(screen, buttons_ui["quit"])  # Desenha o botão de sair

                last_screen_draw = screen_state  # Armazena o último estado desenhado

            if buttons_ui["help"]["rect"].collidepoint((mx, my)) or \
               buttons_ui["quit"]["rect"].collidepoint((mx, my)) or \
               buttons_ui["play"]["rect"].collidepoint((mx, my)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
        elif screen_state == STATE_PAUSE:
            if last_screen_draw != screen_state:
                screen.fill((0, 0, 0))  # fundo preto por padrão

                draw_game(screen, game_state)  # Sempre desenha o estado do jogo

                draw_title(screen)  # Desenha o título do jogo

                # Desenha o restante da HUD
                draw_health_bar(screen, game_state)
                draw_money(screen, game_state)
                draw_clock(screen, game_state)

                draw_overlay(screen, "Jogo pausado.")
                
                draw_button(screen, buttons_ui["help"])  # Desenha o botão de ajuda
                draw_button(screen, buttons_ui["resume"])  # Desenha o botão de jogar
                draw_button(screen, buttons_ui["restart"]) # Desenha o botão de reiniciar
                draw_button(screen, buttons_ui["quit"])  # Desenha o botão de sair

                last_screen_draw = screen_state  # Armazena o último estado desenhado

            if buttons_ui["help"]["rect"].collidepoint((mx, my)) or \
               buttons_ui["resume"]["rect"].collidepoint((mx, my)) or \
               buttons_ui["restart"]["rect"].collidepoint((mx, my)) or \
               buttons_ui["quit"]["rect"].collidepoint((mx, my)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif screen_state == STATE_WIN:
            if last_screen_draw != screen_state:
                screen.fill((0, 0, 0))

                draw_game(screen, game_state)  # Sempre desenha o estado do jogo

                # Desenha o restante da HUD
                draw_health_bar(screen, game_state)
                draw_money(screen, game_state)
                draw_clock(screen, game_state)

                draw_overlay(screen, "Você chegou ao fim do dia! Parabéns!")

                draw_button(screen, buttons_ui["restart"]) # Desenha o botão de reiniciar
                draw_button(screen, buttons_ui["quit"])  # Desenha o botão de sair

                last_screen_draw = screen_state  # Armazena o último estado desenhado

            if buttons_ui["restart"]["rect"].collidepoint((mx, my)) or \
                buttons_ui["quit"]["rect"].collidepoint((mx, my)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif screen_state == STATE_LOSE:
            if last_screen_draw != screen_state:
                screen.fill((0, 0, 0))

                draw_game(screen, game_state)  # Sempre desenha o estado do jogo

                # Desenha o restante da HUD
                draw_health_bar(screen, game_state)
                draw_money(screen, game_state)
                draw_clock(screen, game_state)

                draw_overlay(screen, "Você perdeu! Tente novamente!")

                draw_button(screen, buttons_ui["restart"]) # Desenha o botão de reiniciar
                draw_button(screen, buttons_ui["quit"])  # Desenha o botão de sair

                last_screen_draw = screen_state  # Armazena o último estado desenhado

            if buttons_ui["restart"]["rect"].collidepoint((mx, my)) or \
               buttons_ui["quit"]["rect"].collidepoint((mx, my)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif screen_state == STATE_GAME:
            screen.fill((0, 0, 0))

            update_game(dt, game_state)  # Atualiza o estado do jogo
            draw_game(screen, game_state)  # Sempre desenha o estado do jogo

            draw_title(screen)  # Desenha o título do jogo

            draw_button(screen, buttons_ui["help"])  # Desenha o botão de ajuda
            draw_button(screen, buttons_ui["pause"])  # Desenha o botão de jogar
        
            # Desenha o restante da HUD
            draw_health_bar(screen, game_state)
            draw_money(screen, game_state)
            draw_clock(screen, game_state)

            for hovered_slot, slot in enumerate(game_state["slots"]):
                if slot.collidepoint((mx, my)):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            last_screen_draw = screen_state  # Armazena o último estado desenhado

            if game_state["time_of_day"] >= TIME_END:
                screen_state = STATE_WIN

            if game_state["score"]['amount'] <= 0:
                screen_state = STATE_LOSE  

        pygame.display.flip()

    input("Pressione Enter para sair...")

    # Finaliza o Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
