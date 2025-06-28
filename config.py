# config.py

WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Campus Defense"

# Cores (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Slots fixos para construir prédios (x, y, largura, altura, tipo)
BUILDING_SLOTS = [
    (100, 100, 50, 50),
    (200, 100, 50, 50),
    (300, 100, 50, 50),
    (100, 200, 50, 50),
    (200, 200, 50, 50),
    (300, 200, 50, 50),
    (400, 150, 50, 50)
]

# Tipo de prédio correspondente a cada slot
BUILDING_SLOT_TYPES = [
    'AT', 'AT',
    'Departamento', 'Departamento',
    'BCO', 'BCO',
    'Restaurante'
]

# Definição dos tipos de prédios e parâmetros por nível
BUILDING_TYPES = {
    'AT': {
        'max_level': 2,
        'base_cost': 50,
        'upgrade_cost': 40,
        'range': 100,
        'damage': 1.0,
    },
    'Departamento': {
        'max_level': 3,
        'base_cost': 100,
        'upgrade_cost': 75,
        'range': 120,
        'damage': 1.5,
    },
    'BCO': {
        'max_level': 4,
        'base_cost': 150,
        'upgrade_cost': 100,
        'range': 140,
        'damage': 2.0,
    },
    'Restaurante': {
        'max_level': 4,
        'base_cost': 150,
        'upgrade_cost': 100,
        'range': 140,
        'damage': 2.0,
    },
}

# Clock settings (em horas de jogo)
TIME_START = 6.0            # início do dia (horas)
TIME_END = 19.0             # fim do dia (horas)
TOTAL_DAY_SECONDS = 5 * 60  # tempo real para um dia completo: 6 minutos (360s)
TIME_SPEED = (TIME_END - TIME_START) / TOTAL_DAY_SECONDS  # horas de jogo por segundo real

# Cronograma de spawn de ônibus: (hora início, hora fim, intervalo em segundos, min_passageiros, max_passageiros)
BUS_SPAWN_SCHEDULE = [
    (6, 8, 5, 3, 7), # manhã cedo: 3–7 passageiros
    (8, 12, 2, 8, 12), # manhã: 8–12 passageiros
    (12, 14, 1, 15, 25), # almoço: 15–25 passageiros
    (14, 17, 2, 8, 12), # tarde: 8–12 passageiros
    (17, 19, 4, 3, 7), # fim: 3–7 passageiros
]

# Caminho dos ônibus: lista de waypoints (x, y)
BUS_PATH = [
    (0, 300),
    (200, 300),
    (200, 100),
    (400, 100),
    (600, 300),
    (800, 300),
]

# Recursos iniciais
STARTING_MONEY = 200

# Alcance máximo de qualquer torre (para consulta na quadtree)
MAX_BUILDING_RANGE = max(bt['range'] for bt in BUILDING_TYPES.values())