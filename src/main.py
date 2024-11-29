import pygame
import sys
from .config import WIDTH, HEIGHT, COUNTDOWN_DURATION, MAX_ROUNDS
from .game_state import GameState
from .game_logic import *
from .renderer import GameRenderer
from .resource_loader import load_resources

class Game:
    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rock-Paper-Scissors")
        
        # Initialize game components
        self.resources = load_resources()
        self.game_state = GameState()
        self.renderer = GameRenderer(self.screen, self.resources)
        self.clock = pygame.time.Clock()
        
        # Game timers
        self.opponent_buff_timer = 0
        self.battle_start_time = 0
        self.result_display_time = 0
    
    def handle_buff_selection(self, pos):
        if self.game_state.game_phase != 'select_buff':
            return
            
        # Check card selection
        for i, card_type in enumerate(self.game_state.card_types):
            card_pos = (WIDTH // 2 - 150 + i * 100, 280)  # BUFF_AREA_TOP
            card_rect = pygame.Rect(card_pos, (70, 80))  # CARD_SIZE
            if card_rect.collidepoint(pos):
                self.game_state.selected_buff = card_type
                return
                
        # Check submit button
        if (self.renderer.submit_button.collidepoint(pos) and 
            self.game_state.selected_buff):
            self.game_state.update_energy(self.game_state.selected_buff)
            self.game_state.game_phase = 'opponent_buff'
            self.opponent_buff_timer = pygame.time.get_ticks()
    
    def handle_card_selection(self, pos):
        if self.game_state.game_phase != 'select_card':
            return
            
        for i, card_type in enumerate(self.game_state.card_types):
            card_pos = (30, 120 + i * 120)  # SIDE_MARGIN, TOP_MARGIN + i * CARD_SPACING
            card_rect = pygame.Rect(card_pos, (70, 80))  # CARD_SIZE
            if card_rect.collidepoint(pos):
                self.game_state.player_selection = card_type
                self.game_state.game_phase = 'countdown'
                self.game_state.countdown_number = 3
                self.game_state.countdown_start_time = pygame.time.get_ticks()
    
    def update_countdown(self, current_time):
        if self.game_state.game_phase != 'countdown':
            return
            
        time_elapsed = current_time - self.game_state.countdown_start_time
        if time_elapsed >= COUNTDOWN_DURATION:
            self.game_state.countdown_start_time = current_time
            self.game_state.countdown_number -= 1
            if self.game_state.countdown_number <= 0:
                self.game_state.game_phase = 'show_battle'
                self.game_state.opponent_selection = opponent_choose_move(self.game_state)
                self.battle_start_time = current_time
                self.game_state.countdown_number = None
    
    def update_battle(self, current_time):
        if (self.game_state.game_phase == 'show_battle' and 
            current_time - self.battle_start_time > 1500):
            winner = determine_winner(self.game_state.player_selection, 
                                   self.game_state.opponent_selection)
            
            # Update scores
            if winner == 'player':
                score = calculate_score(self.game_state.player_energy[self.game_state.player_selection])
                self.game_state.player_score += score
                self.game_state.show_result = 'win'
            elif winner == 'opponent':
                score = calculate_score(self.game_state.opponent_energy[self.game_state.opponent_selection])
                self.game_state.opponent_score += score
                self.game_state.show_result = 'lose'
            else:
                self.game_state.show_result = 'draw'
            
            # Reduce energy
            if winner != 'tie':
                self.game_state.reduce_energy()
            
            self.result_display_time = current_time
            self.game_state.game_phase = 'show_result'
    
    def update_result(self, current_time):
        if (self.game_state.show_result and 
            current_time - self.result_display_time > 2000):
            self.game_state.show_result = None
            self.game_state.round_number += 1
            
            # Check if game is over
            if self.game_state.round_number > MAX_ROUNDS:
                self.game_state.show_result = ('victory' if self.game_state.player_score > 
                                             self.game_state.opponent_score else 'defeat')
                pygame.time.delay(3000)
                pygame.quit()
                sys.exit()
            else:
                # Reset for next round
                self.game_state.game_phase = 'select_buff'
                self.game_state.player_selection = None
                self.game_state.opponent_selection = None
                self.game_state.selected_buff = None
    
    def update_opponent_buff(self, current_time):
        if (self.game_state.game_phase == 'opponent_buff' and 
            current_time - self.opponent_buff_timer > 1000):
            opponent_buff = opponent_choose_buff(self.game_state)
            self.game_state.update_energy(opponent_buff, is_player=False)
            self.game_state.game_phase = 'select_card'
    
    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_state.show_result:
                        self.handle_buff_selection(event.pos)
                        self.handle_card_selection(event.pos)
            
            # Game state updates
            self.update_countdown(current_time)
            self.update_battle(current_time)
            self.update_result(current_time)
            self.update_opponent_buff(current_time)
            
            # Render
            self.renderer.draw_ui(self.game_state)
            pygame.display.flip()
            self.clock.tick(60)

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main() 