# main.py
import pygame
from config import (
    WIDTH, HEIGHT, FPS, BUILDING_SLOTS, STARTING_MONEY,
    BUS_PATH, TIME_START, TIME_END, TIME_SPEED,
    BUS_SPAWN_SCHEDULE, TOTAL_DAY_SECONDS, MAX_BUILDING_RANGE, BUILDING_TYPES, GRAY, BLACK
)
from quadtree import QuadTree, Rect
from entities import Building, Bus

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

money = {'amount': STARTING_MONEY}

def get_spawn_interval(hour):
    for start, end, interval in BUS_SPAWN_SCHEDULE:
        if start <= hour < end:
            return interval
    return None


def main():
    time_of_day = TIME_START
    boundary = Rect(0, 0, WIDTH, HEIGHT)
    qt = QuadTree(boundary)
    buildings = {}
    slots = [pygame.Rect(*s) for s in BUILDING_SLOTS]
    buses = []
    spawn_timer = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        # atualizar horário do jogo
        time_of_day += dt * TIME_SPEED
        # fim do dia
        if time_of_day >= TIME_END:
            print("Fim do dia! Game Over")
            running = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                for idx, slot in enumerate(slots):
                    if slot.collidepoint(mx, my):
                        if idx not in buildings:
                            cost = BUILDING_TYPES['AT']['base_cost']
                            if money['amount'] >= cost:
                                money['amount'] -= cost
                                b = Building('AT', slot, money)
                                buildings[idx] = b
                                qt.insert(b)
                        else:
                            buildings[idx].upgrade()

        # spawn de ônibus apenas durante o dia com base na intensidade
        if TIME_START <= time_of_day < TIME_END:
            spawn_timer += dt
            interval = get_spawn_interval(time_of_day)
            if interval and spawn_timer >= interval:
                buses.append(Bus(BUS_PATH))
                spawn_timer = 0

        # atualizar ônibus
        for bus in list(buses):
            bus.update(dt)
            if bus.finished:
                buses.remove(bus)
                if bus.passengers > 0:
                    print("Game Over")
                    running = False

        # ataque das torres
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

        # desenho
        screen.fill(GRAY)
        for slot in slots:
            pygame.draw.rect(screen, BLACK, slot, 1)
        for b in buildings.values():
            b.draw(screen)
        for bus in buses:
            bus.draw(screen)

        # HUD
        font = pygame.font.SysFont(None, 24)
        txt = font.render(
            f"Money: {int(money['amount'])} | Time: {time_of_day:.2f}h", True, BLACK
        )
        screen.blit(txt, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
