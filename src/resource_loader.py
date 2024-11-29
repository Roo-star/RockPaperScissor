import os
import pygame
from .config import CARD_SIZE, ENERGY_ICON_SIZE

def load_image(name):
    path = os.path.join('imgs', name)
    return pygame.image.load(path)

def load_resources():
    # Load card images
    card_images = {
        'rock': load_image('rock.png'),
        'paper': load_image('paper.png'),
        'scissors': load_image('scissors.png')
    }
    
    # Scale card images
    for card in card_images:
        card_images[card] = pygame.transform.smoothscale(card_images[card], CARD_SIZE)
    
    # Load and scale energy icon
    energy_icon = pygame.transform.smoothscale(load_image('energy.png'), ENERGY_ICON_SIZE)
    
    # Load result images
    result_images = {
        'win': load_image('win.png'),
        'lose': load_image('lose.png'),
        'draw': load_image('draw.png'),
        'victory': load_image('victory.png'),
        'defeat': load_image('defeat.png')
    }
    
    return card_images, energy_icon, result_images 