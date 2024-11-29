import pygame
from .config import *

class GameRenderer:
    def __init__(self, screen, resources):
        self.screen = screen
        self.card_images, self.energy_icon, self.result_images = resources
        self.submit_button = pygame.Rect(
            WIDTH // 2 - SUBMIT_BUTTON_WIDTH // 2,
            SUBMIT_BUTTON_Y,
            SUBMIT_BUTTON_WIDTH,
            SUBMIT_BUTTON_HEIGHT
        )
        
    def draw_energy_icons(self, x, y, energy_count, align_right=False):
        if align_right:
            total_width = energy_count * (ENERGY_ICON_SIZE[0] + 5) - 5
            x = x - total_width
        for i in range(energy_count):
            self.screen.blit(self.energy_icon, 
                           (x + i * (ENERGY_ICON_SIZE[0] + 5), y))
    
    def draw_ui(self, game_state):
        self.screen.fill(LIGHT_BLUE)
        self._draw_scores(game_state)
        self._draw_cards(game_state)
        self._draw_phase_text(game_state)
        self._draw_game_area(game_state)
        self._draw_round_number(game_state)
        self._draw_result(game_state)
    
    def _draw_scores(self, game_state):
        # Draw player and opponent labels
        player_label = large_font.render("PLAYER", True, BLACK)
        opponent_label = large_font.render("COMPUTER", True, BLACK)
        self.screen.blit(player_label, (SIDE_MARGIN, 20))
        self.screen.blit(opponent_label, (WIDTH - SIDE_MARGIN - opponent_label.get_width(), 20))
        
        # Draw scores
        score_text = font.render(f"Score: {game_state.player_score}", True, BLACK)
        opponent_score_text = font.render(f"Score: {game_state.opponent_score}", True, BLACK)
        self.screen.blit(score_text, (SIDE_MARGIN, 80))
        self.screen.blit(opponent_score_text, (WIDTH - SIDE_MARGIN - opponent_score_text.get_width(), 80))
    
    def _draw_cards(self, game_state):
        # Draw player cards with energy icons
        for i, card_type in enumerate(game_state.card_types):
            # Player cards
            card_pos = (SIDE_MARGIN, TOP_MARGIN + i * CARD_SPACING)
            card_rect = pygame.Rect(card_pos, CARD_SIZE)
            self.screen.blit(self.card_images[card_type], card_pos)
            
            if game_state.game_phase == 'select_card':
                # Draw hover effect
                if card_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, HOVER_COLOR, card_rect, 3)
                # Draw selection border
                if card_type == game_state.player_selection:
                    pygame.draw.rect(self.screen, SELECT_COLOR, card_rect, 3)
            
            self.draw_energy_icons(SIDE_MARGIN, card_pos[1] + CARD_SIZE[1] + ENERGY_OFFSET, 
                                 game_state.player_energy[card_type])
            
            # Opponent cards
            opponent_card_pos = (WIDTH - SIDE_MARGIN - CARD_SIZE[0], TOP_MARGIN + i * CARD_SPACING)
            self.screen.blit(self.card_images[card_type], opponent_card_pos)
            self.draw_energy_icons(opponent_card_pos[0] + CARD_SIZE[0], 
                                 opponent_card_pos[1] + CARD_SIZE[1] + ENERGY_OFFSET,
                                 game_state.opponent_energy[card_type], align_right=True)
    
    def _draw_phase_text(self, game_state):
        phase_text = {
            'select_buff': "Select Buff",
            'opponent_buff': "Opponent selecting buff...",
            'select_card': "Select Your Card",
            'countdown': "Get Ready!",
            'show_battle': "Battle Result"
        }.get(game_state.game_phase, "")
        select_text = large_font.render(phase_text, True, BLACK)
        self.screen.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, 160))
    
    def _draw_game_area(self, game_state):
        if game_state.game_phase == 'select_buff':
            self._draw_buff_selection(game_state)
        elif game_state.game_phase == 'show_battle':
            self._draw_battle_area(game_state)
        elif game_state.game_phase == 'countdown' and game_state.countdown_number:
            self._draw_countdown(game_state)
    
    def _draw_buff_selection(self, game_state):
        # Draw border for buff selection area
        buff_area_rect = pygame.Rect(WIDTH // 2 - 180, BUFF_AREA_TOP - 20, 360, 150)
        pygame.draw.rect(self.screen, BORDER_COLOR, buff_area_rect, 3)
        
        for i, card_type in enumerate(game_state.card_types):
            card_pos = (WIDTH // 2 - 150 + i * 100, BUFF_AREA_TOP)
            self.screen.blit(self.card_images[card_type], card_pos)
            
            # Draw hover effect
            card_rect = pygame.Rect(card_pos, CARD_SIZE)
            if card_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, HOVER_COLOR, card_rect, 3)
            
            # Draw selection border
            if card_type == game_state.selected_buff:
                pygame.draw.rect(self.screen, SELECT_COLOR, card_rect, 3)
            
            self.screen.blit(self.energy_icon, 
                           (card_pos[0] + CARD_SIZE[0]//2 - ENERGY_ICON_SIZE[0]//2,
                            card_pos[1] + CARD_SIZE[1] + 5))
        self._draw_submit_button(game_state)
    
    def _draw_battle_area(self, game_state):
        if not game_state.player_selection or not game_state.opponent_selection:
            return
            
        # Draw border for battle area
        battle_area_rect = pygame.Rect(WIDTH // 2 - 200, BATTLE_AREA_TOP - 20, 400, 150)
        pygame.draw.rect(self.screen, BORDER_COLOR, battle_area_rect, 3)
        
        # Draw battle result in center
        player_card_pos = (WIDTH // 2 - 100 - CARD_SIZE[0], BATTLE_AREA_TOP)
        opponent_card_pos = (WIDTH // 2 + 100, BATTLE_AREA_TOP)
        
        # Draw selected cards
        self.screen.blit(self.card_images[game_state.player_selection], player_card_pos)
        self.screen.blit(self.card_images[game_state.opponent_selection], opponent_card_pos)
        
        # Draw energy icons below cards
        self.draw_energy_icons(player_card_pos[0], 
                             player_card_pos[1] + CARD_SIZE[1] + ENERGY_OFFSET,
                             game_state.player_energy[game_state.player_selection])
        self.draw_energy_icons(opponent_card_pos[0] + CARD_SIZE[0],
                             opponent_card_pos[1] + CARD_SIZE[1] + ENERGY_OFFSET,
                             game_state.opponent_energy[game_state.opponent_selection],
                             align_right=True)
        
        # Draw VS text
        vs_text = large_font.render("VS", True, BLACK)
        self.screen.blit(vs_text, (WIDTH // 2 - vs_text.get_width() // 2, BATTLE_AREA_TOP + 30))
    
    def _draw_countdown(self, game_state):
        countdown_text = large_font.render(str(game_state.countdown_number), True, BLACK)
        countdown_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(countdown_text, countdown_rect)
    
    def _draw_round_number(self, game_state):
        round_text = large_font.render(f"Round: {game_state.round_number}/{MAX_ROUNDS}", True, BLACK)
        self.screen.blit(round_text, (WIDTH // 2 - round_text.get_width() // 2, 10))
    
    def _draw_result(self, game_state):
        if game_state.show_result:
            result_img = self.result_images[game_state.show_result]
            result_pos = (WIDTH // 2 - result_img.get_width() // 2,
                         HEIGHT // 2 - result_img.get_height() // 2)
            self.screen.blit(result_img, result_pos)
    
    def _draw_submit_button(self, game_state):
        button_color = BLUE if game_state.selected_buff else GRAY
        
        # Add hover effect
        if game_state.selected_buff and self.submit_button.collidepoint(pygame.mouse.get_pos()):
            button_color = HOVER_COLOR
        
        # Draw button with rounded corners
        pygame.draw.rect(self.screen, button_color, self.submit_button, border_radius=8)
        
        # Add a subtle border
        if game_state.selected_buff:
            border_rect = self.submit_button.inflate(4, 4)
            pygame.draw.rect(self.screen, BORDER_COLOR, border_rect, 2, border_radius=10)
        
        # Draw text
        text = font.render("Okay!", True, WHITE)
        text_rect = text.get_rect(center=self.submit_button.center)
        self.screen.blit(text, text_rect)