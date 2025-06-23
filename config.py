# config.py
import pygame

# Tela
WIDTH, HEIGHT = 800, 600
FPS = 60

# Cores
GREEN = (50, 168, 82)
WHITE = (255, 255, 255)
BLUE = (60, 60, 255)
RED = (200, 0, 0)
YELLOW = (255, 200, 0)
GRAY = (180, 180, 180)

# Tipos de prédios
BUILDING_TYPES = {
    "AT": {"radius": 70, "damage": 1, "cooldown": 1000, "color": BLUE},
    "Especial": {"radius": 100, "damage": 2, "cooldown": 800, "color": RED},
}

# Posições fixas
BUILDING_SLOTS = [
    (100, 100), (400, 100), (700, 100),
    (100, 300), (700, 300),
    (100, 500), (400, 500), (700, 500),
]

# Caminho do ônibus
BUS_PATH = [
    (100, 100), (700, 100),
    (700, 500), (100, 500),
    (100, 100)
]
