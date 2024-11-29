import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock-Paper-Scissors (DEBUG)")

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

# Font
font = pygame.font.Font("fonts/Snowy Days.ttf", 32)
large_font = pygame.font.Font("fonts/Snowy Days.ttf", 40)

# Constants for layout
CARD_SIZE = (70, 80)
ENERGY_ICON_SIZE = (18, 24)
CARD_SPACING = 120
SIDE_MARGIN = 30
TOP_MARGIN = 120
ENERGY_OFFSET = 10
BUFF_AREA_TOP = 280
BATTLE_AREA_TOP = 320
SUBMIT_BUTTON_WIDTH = 120  # Increased from 100
SUBMIT_BUTTON_HEIGHT = 50  # Increased from 40
SUBMIT_BUTTON_Y = 440  # Adjusted from 420 to account for new height

# Load and scale images
def load_image(name):
    path = os.path.join('imgs', name)
    return pygame.image.load(path)

# Card images
card_images = {
    'rock': load_image('rock.png'),
    'paper': load_image('paper.png'),
    'scissors': load_image('scissors.png')
}

# Energy icon
energy_icon = pygame.transform.smoothscale(load_image('energy.png'), ENERGY_ICON_SIZE)

# Result images
result_images = {
    'win': load_image('win.png'),
    'lose': load_image('lose.png'),
    'draw': load_image('draw.png'),
    'victory': load_image('victory.png'),
    'defeat': load_image('defeat.png')
}

# Scale images
for card in card_images:
    card_images[card] = pygame.transform.smoothscale(card_images[card], CARD_SIZE)

# Game state
player_score = 0
opponent_score = 0
round_number = 1
max_rounds = 5

# Game state for buff system
card_types = ['rock', 'paper', 'scissors']
player_energy = {card_type: 1 for card_type in card_types}
opponent_energy = {card_type: 1 for card_type in card_types}
selected_buff = None
player_selection = None
opponent_selection = None
show_result = None
submit_button = pygame.Rect(
    WIDTH // 2 - SUBMIT_BUTTON_WIDTH // 2,
    SUBMIT_BUTTON_Y,
    SUBMIT_BUTTON_WIDTH,
    SUBMIT_BUTTON_HEIGHT
)
game_phase = 'select_buff'

# 在游戏状态常量区域添加倒计时相关常量
COUNTDOWN_DURATION = 1000  # 每个数字显示1秒
COUNTDOWN_SIZE = (40, 40)  # 倒计时数字的大小

# 在游戏状态区域添加倒计时状态
countdown_number = None
countdown_start_time = None

def draw_energy_icons(x, y, energy_count, align_right=False):
    if align_right:
        # Calculate starting x position for right alignment
        total_width = energy_count * (ENERGY_ICON_SIZE[0] + 5) - 5  # Subtract last spacing
        x = x - total_width
    for i in range(energy_count):
        screen.blit(energy_icon, (x + i * (ENERGY_ICON_SIZE[0] + 5), y))

def draw_submit_button():
    button_color = BLUE if selected_buff else (150, 150, 150)
    
    # Add hover effect
    if selected_buff and submit_button.collidepoint(pygame.mouse.get_pos()):
        button_color = HOVER_COLOR
    
    # Draw button with rounded corners
    pygame.draw.rect(screen, button_color, submit_button, border_radius=8)
    
    # Add a subtle border
    if selected_buff:
        border_rect = submit_button.inflate(4, 4)  # Slightly larger rect for border
    
    # Draw text with padding
    text = font.render("Okay!", True, WHITE)
    text_rect = text.get_rect(center=submit_button.center)
    screen.blit(text, text_rect)

def draw_ui():
    screen.fill(LIGHT_BLUE)
    
    # Draw player and opponent labels
    player_label = large_font.render("PLAYER", True, BLACK)
    opponent_label = large_font.render("COMPUTER", True, BLACK)
    screen.blit(player_label, (SIDE_MARGIN, 20))
    screen.blit(opponent_label, (WIDTH - SIDE_MARGIN - opponent_label.get_width(), 20))
    
    # Draw scores
    score_text = font.render(f"Score: {player_score}", True, BLACK)
    opponent_score_text = font.render(f"Score: {opponent_score}", True, BLACK)
    screen.blit(score_text, (SIDE_MARGIN, 80))
    screen.blit(opponent_score_text, (WIDTH - SIDE_MARGIN - opponent_score_text.get_width(), 80))
    
    # Draw player cards with energy icons
    for i, card_type in enumerate(card_types):
        card_pos = (SIDE_MARGIN, TOP_MARGIN + i * CARD_SPACING)
        card_rect = pygame.Rect(card_pos, CARD_SIZE)
        
        screen.blit(card_images[card_type], card_pos)
        
        if game_phase == 'select_card':
            # Draw hover effect
            if card_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, HOVER_COLOR, card_rect, 3)
            
            # Draw selection border
            if card_type == player_selection:
                pygame.draw.rect(screen, SELECT_COLOR, card_rect, 3)
                
        draw_energy_icons(SIDE_MARGIN, card_pos[1] + CARD_SIZE[1] + ENERGY_OFFSET, 
                         player_energy[card_type])
    
    # Draw phase text
    phase_text = {
        'select_buff': "Select Buff",
        'opponent_buff': "Opponent selecting buff...",
        'select_card': "Select Your Card",
        'countdown': "Get Ready!",  # 改为显示准备文本
        'show_battle': "Battle Result"
    }.get(game_phase, "")
    select_text = large_font.render(phase_text, True, BLACK)
    screen.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, 160))
    
    # Draw central area based on game phase
    if game_phase == 'select_buff':
        # Draw border for buff selection area
        buff_area_rect = pygame.Rect(WIDTH // 2 - 180, BUFF_AREA_TOP - 20, 360, 150)
        pygame.draw.rect(screen, BORDER_COLOR, buff_area_rect, 3)
        
        for i, card_type in enumerate(card_types):
            card_pos = (WIDTH // 2 - 150 + i * 100, BUFF_AREA_TOP)
            screen.blit(card_images[card_type], card_pos)
            
            # Draw hover effect
            card_rect = pygame.Rect(card_pos, CARD_SIZE)
            if card_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, HOVER_COLOR, card_rect, 3)
            
            # Draw selection border
            if card_type == selected_buff:
                pygame.draw.rect(screen, SELECT_COLOR, card_rect, 3)
                
            screen.blit(energy_icon, (card_pos[0] + CARD_SIZE[0]//2 - ENERGY_ICON_SIZE[0]//2, 
                                    card_pos[1] + CARD_SIZE[1] + 5))
        draw_submit_button()
        
    elif game_phase == 'show_battle' and player_selection and opponent_selection:
        # Draw border for battle area
        battle_area_rect = pygame.Rect(WIDTH // 2 - 200, BATTLE_AREA_TOP - 20, 400, 150)
        pygame.draw.rect(screen, BORDER_COLOR, battle_area_rect, 3)
        
        # Draw battle result in center
        player_card_pos = (WIDTH // 2 - 100 - CARD_SIZE[0], BATTLE_AREA_TOP)
        opponent_card_pos = (WIDTH // 2 + 100, BATTLE_AREA_TOP)
        
        # Draw selected cards
        screen.blit(card_images[player_selection], player_card_pos)
        screen.blit(card_images[opponent_selection], opponent_card_pos)
        
        # Draw energy icons below cards
        draw_energy_icons(player_card_pos[0], player_card_pos[1] + CARD_SIZE[1] + ENERGY_OFFSET, 
                         player_energy[player_selection])
        draw_energy_icons(opponent_card_pos[0] + CARD_SIZE[0], opponent_card_pos[1] + CARD_SIZE[1] + ENERGY_OFFSET,
                         opponent_energy[opponent_selection], align_right=True)
        
        # Draw VS text
        vs_text = large_font.render("VS", True, BLACK)
        screen.blit(vs_text, (WIDTH // 2 - vs_text.get_width() // 2, BATTLE_AREA_TOP + 30))
    
    # Draw opponent cards with energy icons
    for i, card_type in enumerate(card_types):
        card_pos = (WIDTH - SIDE_MARGIN - CARD_SIZE[0], TOP_MARGIN + i * CARD_SPACING)
        screen.blit(card_images[card_type], card_pos)
        draw_energy_icons(card_pos[0] + CARD_SIZE[0], card_pos[1] + CARD_SIZE[1] + ENERGY_OFFSET,
                         opponent_energy[card_type], align_right=True)
    
    # Draw round number
    round_text = large_font.render(f"Round: {round_number}/{max_rounds}", True, BLACK)
    screen.blit(round_text, (WIDTH // 2 - round_text.get_width() // 2, 10))
    
    # Draw result if available
    if show_result:
        result_img = result_images[show_result]
        result_pos = (WIDTH // 2 - result_img.get_width() // 2,
                     HEIGHT // 2 - result_img.get_height() // 2)
        screen.blit(result_img, result_pos)
    
    # 在倒计时阶段显示大数字
    if game_phase == 'countdown' and countdown_number:
        countdown_text = large_font.render(str(countdown_number), True, BLACK)
        countdown_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(countdown_text, countdown_rect)

def update_score_and_health(winner):
    global player_score, opponent_score, show_result
    
    if winner == 'player':
        score = 10 + player_energy[player_selection] * 10
        player_score += score
        show_result = 'win'
    elif winner == 'opponent':
        score = 10 + opponent_energy[opponent_selection] * 10
        opponent_score += score
        show_result = 'lose'
    else:
        show_result = 'draw'
    
    # Reduce energy
    if winner != 'tie':
        player_energy[player_selection] = max(0, player_energy[player_selection] - 1)
        opponent_energy[opponent_selection] = max(0, opponent_energy[opponent_selection] - 1)
def get_card_rect(index):
    return pygame.Rect(WIDTH // 2 - 150 + index * 100, BUFF_AREA_TOP, *CARD_SIZE)

def get_player_card_rect(index):
    return pygame.Rect(SIDE_MARGIN, TOP_MARGIN + index * CARD_SPACING, *CARD_SIZE)

def handle_buff_selection(pos):
    global selected_buff
    for i, card_type in enumerate(card_types):
        if get_card_rect(i).collidepoint(pos):
            selected_buff = card_type
            return True
    return False

def handle_card_selection(pos):
    global player_selection, game_phase, countdown_number, countdown_start_time
    if game_phase == 'select_card':
        for i, card_type in enumerate(card_types):
            if get_player_card_rect(i).collidepoint(pos):
                player_selection = card_type
                game_phase = 'countdown'  # 改为倒计时阶段
                countdown_number = 3
                countdown_start_time = pygame.time.get_ticks()
                return True
    return False

def apply_buff():
    global player_energy, opponent_energy, game_phase, selected_buff
    if selected_buff:
        # Apply player's buff
        player_energy[selected_buff] += 1
        game_phase = 'opponent_buff'
        
def apply_opponent_buff():
    global opponent_energy, game_phase
    # Computer randomly chooses a buff
    opponent_buff = random.choice(card_types)
    opponent_energy[opponent_buff] += 1
    game_phase = 'select_card'

def opponent_choose():
    # Computer chooses card with highest energy
    max_energy = max(opponent_energy.values())
    possible_choices = [card for card, energy in opponent_energy.items() if energy == max_energy]
    return random.choice(possible_choices)

def determine_winner(player, opponent):
    if player == opponent:
        return 'tie'
    elif (player == 'rock' and opponent == 'scissors') or \
         (player == 'paper' and opponent == 'rock') or \
         (player == 'scissors' and opponent == 'paper'):
        return 'player'
    else:
        return 'opponent'


def main():
    global player_selection, opponent_selection, round_number, show_result, game_phase, selected_buff, countdown_number, countdown_start_time
    clock = pygame.time.Clock()
    result_display_time = 0
    opponent_buff_timer = 0
    battle_start_time = 0
    
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not show_result:
                if game_phase == 'select_buff':
                    handle_buff_selection(event.pos)
                    if submit_button.collidepoint(event.pos) and selected_buff:
                        apply_buff()
                        opponent_buff_timer = current_time
                elif game_phase == 'select_card':
                    handle_card_selection(event.pos)
        
        # 处理倒计时逻辑
        if game_phase == 'countdown':
            time_elapsed = current_time - countdown_start_time
            if time_elapsed >= COUNTDOWN_DURATION:
                countdown_start_time = current_time
                countdown_number -= 1
                if countdown_number <= 0:
                    game_phase = 'show_battle'
                    opponent_selection = opponent_choose()
                    battle_start_time = current_time
                    countdown_number = None
        
        # Handle opponent buff selection after a delay
        if game_phase == 'opponent_buff' and pygame.time.get_ticks() - opponent_buff_timer > 1000:
            apply_opponent_buff()
            selected_buff = None
        
        # Handle battle result after a delay
        if game_phase == 'show_battle' and pygame.time.get_ticks() - battle_start_time > 1500:
            winner = determine_winner(player_selection, opponent_selection)
            update_score_and_health(winner)
            result_display_time = pygame.time.get_ticks()
            game_phase = 'show_result'
        
        # Clear result after delay
        if show_result and pygame.time.get_ticks() - result_display_time > 2000:
            show_result = None
            round_number += 1
            
            # 检查是否达到最大回合数
            if round_number > max_rounds:
                # 显示最终结果
                show_result = 'victory' if player_score > opponent_score else 'defeat'
                # 等待3秒后退出
                pygame.time.delay(3000)
                pygame.quit()
                sys.exit()
            else:
                # 继续下一回合
                game_phase = 'select_buff'
                player_selection = None
                opponent_selection = None
        
        draw_ui()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main() 