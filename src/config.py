import pygame

# Window settings
WIDTH, HEIGHT = 800, 600
CARD_SIZE = (70, 80)
ENERGY_ICON_SIZE = (18, 24)
CARD_SPACING = 120
SIDE_MARGIN = 30
TOP_MARGIN = 120
ENERGY_OFFSET = 10
BUFF_AREA_TOP = 280
BATTLE_AREA_TOP = 320
SUBMIT_BUTTON_WIDTH = 120
SUBMIT_BUTTON_HEIGHT = 50
SUBMIT_BUTTON_Y = 440

# Colors
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
BLUE = (65, 105, 225)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (150, 150, 255)
SELECT_COLOR = GREEN
BORDER_COLOR = (100, 100, 100)

# Game settings
COUNTDOWN_DURATION = 1000
COUNTDOWN_SIZE = (40, 40)
MAX_ROUNDS = 5

# Initialize Pygame
pygame.init()
font = pygame.font.Font("fonts/Snowy Days.ttf", 32)
large_font = pygame.font.Font("fonts/Snowy Days.ttf", 40) 