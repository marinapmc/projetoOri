# config.py

WIDTH = 800
HEIGHT = 600
FPS = 60

# Cores (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Slots fixos para construir prédios (x, y, largura, altura)
BUILDING_SLOTS = [
    (100, 100, 40, 40),
    (200, 100, 40, 40),
    (300, 100, 40, 40),
    (100, 200, 40, 40),
    (200, 200, 40, 40),
    (300, 200, 40, 40),
    (400, 150, 40, 40),
]

# Definição dos tipos de prédios e parâmetros por nível
BUILDING_TYPES = {
    'AT': {
        'name': 'AT',
        'max_level': 2,
        'base_cost': 50,
        'upgrade_cost': 40,
        'range': 100,
        'damage': 1.0,
    },
    'Departamento': {
        'name': 'Departamento',
        'max_level': 3,
        'base_cost': 100,
        'upgrade_cost': 75,
        'range': 120,
        'damage': 1.5,
    },
    'BCO': {
        'name': 'BCO',
        'max_level': 4,
        'base_cost': 150,
        'upgrade_cost': 100,
        'range': 140,
        'damage': 2.0,
    },
    'Restaurante': {
        'name': 'Restaurante',
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
TOTAL_DAY_SECONDS = 6 * 60  # tempo real para um dia completo: 6 minutos (360s)
TIME_SPEED = (TIME_END - TIME_START) / TOTAL_DAY_SECONDS  # horas de jogo por segundo real

# Horários e intensidade de spawn de ônibus: (início, fim, intervalo em segundos)
BUS_SPAWN_SCHEDULE = [
    (6, 8, 5),    # manhã cedo: 1 ônibus a cada 5s
    (8, 12, 2),   # manhã: 1 ônibus a cada 2s
    (12, 14, 1),  # pico do almoço: 1 ônibus por segundo
    (14, 17, 2),  # tarde: 1 ônibus a cada 2s
    (17, 19, 4),  # fim de expediente: 1 ônibus a cada 4s
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