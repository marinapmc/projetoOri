# config.py

WIDTH = 975
HEIGHT = 650
FPS = 60
TITLE = "Campus Defense"

# Cores (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (102, 106, 17)
RED = (255, 0, 0)

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
        'base_cost': 100,
        'upgrade_cost': 100,
        'range': 100,
        'range_increase': 50,  # aumento do alcance por nível
        'damage': 1,
        'fire_rate': 0.8,  # taxa de disparo em segundos
        'fire_rate_increase': 0.1,  # aumento da taxa de disparo por nível
    },
    'AT5': {
        'name': 'AT5',
        'max_level': 2,
        'base_cost': 100,
        'upgrade_cost': 100,
        'range': 100,
        'range_increase': 50,  # aumento do alcance por nível
        'damage': 1,
        'fire_rate': 0.8,  
        'fire_rate_increase': 0.1, 
    },
    'AT7': {
        'name': 'AT7',
        'max_level': 2,
        'base_cost': 100,
        'upgrade_cost': 100,
        'range': 100,
        'range_increase': 50,  # aumento do alcance por nível
        'damage': 1,
        'fire_rate': 0.8, 
        'fire_rate_increase': 0.1,
    },
    'AT10': {
        'name': 'AT10',
        'max_level': 2,
        'base_cost': 100,
        'upgrade_cost': 100,
        'range': 100,
        'range_increase': 50,  # aumento do alcance por nível
        'damage': 1,
        'fire_rate': 0.8,  
        'fire_rate_increase': 0.1,
    },
    'DEMA': {
        'name': 'DEMA',
        'max_level': 3,
        'base_cost': 200,
        'upgrade_cost': 250,
        'range': 120,
        'range_increase': 50,  # aumento do alcance por nível
        'damage': 1,
        'fire_rate': 0.6,
        'fire_rate_increase': 0.2,  # aumento da taxa de disparo por nível
    },
    'DF': {
        'name': 'DF',
        'max_level': 3,
        'base_cost': 200,
        'upgrade_cost': 250,
        'range': 120,
        'damage': 1,
        'fire_rate': 0.6,  
    },
    'BCO': {
        'name': 'BCO',
        'max_level': 4,
        'base_cost': 300,
        'upgrade_cost': 300,
        'range': 140,
        'damage': 1,
        'fire_rate': 0.4,
    },
}

# Clock settings (em horas de jogo)
TIME_START = 6.0            # início do dia (horas)
TIME_END = 19.0             # fim do dia (horas)
TOTAL_DAY_SECONDS = 0.5 * 60  # tempo real para um dia completo: 6 minutos (360s)
TIME_SPEED = (TIME_END - TIME_START) / TOTAL_DAY_SECONDS  # horas de jogo por segundo real

# Cronograma de spawn de ônibus: (hora início, hora fim, intervalo em segundos, min_passageiros, max_passageiros)
BUS_SPAWN_SCHEDULE = [
    (6, 8, 8, 10, 20),   
    (8, 10, 10, 15, 30),    
    (10, 12, 9, 30, 40), 
    (12, 14, 11, 40, 60), 
    (14, 16, 9, 30, 50), 
    (16, 19, 8, 50, 70), 
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
STARTING_MONEY = 10000

# Alcance máximo de qualquer torre (para consulta na quadtree)
MAX_BUILDING_RANGE = max(bt['range'] for bt in BUILDING_TYPES.values())