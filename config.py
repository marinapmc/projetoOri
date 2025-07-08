# config.py

WIDTH = 975
HEIGHT = 650
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
    (155, 342, 77, 54), # AT10
    (308, 172, 77, 54), # AT4
    (692, 232, 77, 54), # AT5
    (837, 213, 77, 54), # AT7
    (195, 530, 143, 60), # Departamento Física
    (495, 190, 149, 60), # Departamento Materiais
    (265, 378, 140, 70), # BCO
]

# Tipo de prédio correspondente a cada slot
BUILDING_SLOT_TYPES = [
    'AT10', 'AT4', 'AT5', 'AT7',
    'DF', 'DEMA',
    'BCO'
]

# Definição dos tipos de prédios e parâmetros por nível
BUILDING_TYPES = {
    'AT4': {
        'name': 'AT4',
        'max_level': 2,
        'base_cost': 50,
        'upgrade_cost': 40,
        'range': 100,
        'damage': 1,
        'fire_rate': 0.6,  # taxa de disparo em segundos
    },
    'AT5': {
        'name': 'AT5',
        'max_level': 2,
        'base_cost': 50,
        'upgrade_cost': 40,
        'range': 100,
        'damage': 1,
        'fire_rate': 0.6,  
    },
    'AT7': {
        'name': 'AT7',
        'max_level': 2,
        'base_cost': 50,
        'upgrade_cost': 40,
        'range': 100,
        'damage': 1,
        'fire_rate': 0.6, 
    },
    'AT10': {
        'name': 'AT10',
        'max_level': 2,
        'base_cost': 50,
        'upgrade_cost': 40,
        'range': 100,
        'damage': 1,
        'fire_rate': 0.6,  
    },
    'DEMA': {
        'name': 'DEMA',
        'max_level': 3,
        'base_cost': 100,
        'upgrade_cost': 75,
        'range': 120,
        'damage': 1,
        'fire_rate': 0.8,
    },
    'DF': {
        'name': 'DF',
        'max_level': 3,
        'base_cost': 100,
        'upgrade_cost': 75,
        'range': 120,
        'damage': 1,
        'fire_rate': 0.8,  
    },
    'BCO': {
        'name': 'BCO',
        'max_level': 4,
        'base_cost': 150,
        'upgrade_cost': 100,
        'range': 140,
        'damage': 1,
        'fire_rate': 0.6,
    },
}

# Clock settings (em horas de jogo)
TIME_START = 6.0            # início do dia (horas)
TIME_END = 19.0             # fim do dia (horas)
TOTAL_DAY_SECONDS = 5 * 60  # tempo real para um dia completo: 6 minutos (360s)
TIME_SPEED = (TIME_END - TIME_START) / TOTAL_DAY_SECONDS  # horas de jogo por segundo real

# Cronograma de spawn de ônibus: (hora início, hora fim, intervalo em segundos, min_passageiros, max_passageiros)
BUS_SPAWN_SCHEDULE = [
    (6, 7, 10, 10, 30),   
    (7, 8, 8, 30, 60),   
    (8, 9, 10, 10, 30),   
    (9, 10, 6.0, 25, 55),  
    (10, 11, 10, 10, 30), 
    (11, 12, 6.0, 25, 55), 
    (12, 13, 6.0, 25, 55), 
    (13, 14, 6, 50, 75), 
    (14, 15, 10, 10, 30), 
    (15, 16, 4.0, 50, 75), 
    (16, 17, 10, 10, 30), 
    (17, 18, 6, 50, 75), 
    (18, 19, 3.0, 70, 95), 
]

# Caminho dos ônibus: lista de waypoints (x, y)
BUS_PATH = [
    (-150, 485),
    (87, 485),
    (87, 455),
    (117, 455),
    (117, 300),
    (87, 300), 
    (87, 240),
    (147, 240), 
    (147, 270), 
    (272, 270),
    (272, 145), 
    (427, 145),
    (427, 115), 
    (487, 115), 
    (487, 145),
    (767, 145), 
    (767, 115), 
    (830, 115), 
    (830, 175), 
    (798, 175), 
    (798, 330), 
    (830, 330), 
    (830, 393), 
    (770, 393), 
    (770, 360),
    (612, 360),
    (612, 393),
    (550, 393),
    (550, 360), 
    (458, 360),
    (458, 487),
    (147, 487),
    (147, 517),
    (117, 517),
    (117, 700),
]

# Recursos iniciais
STARTING_MONEY = 200

# Alcance máximo de qualquer torre (para consulta na quadtree)
MAX_BUILDING_RANGE = max(bt['range'] for bt in BUILDING_TYPES.values())