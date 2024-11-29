class GameState:
    def __init__(self):
        self.card_types = ['rock', 'paper', 'scissors']
        self.reset_game()
    
    def reset_game(self):
        self.player_score = 0
        self.opponent_score = 0
        self.round_number = 1
        self.player_energy = {card_type: 1 for card_type in self.card_types}
        self.opponent_energy = {card_type: 1 for card_type in self.card_types}
        self.selected_buff = None
        self.player_selection = None
        self.opponent_selection = None
        self.show_result = None
        self.game_phase = 'select_buff'
        self.countdown_number = None
        self.countdown_start_time = None
    
    def update_energy(self, buff_type, is_player=True):
        if is_player:
            self.player_energy[buff_type] += 1
        else:
            self.opponent_energy[buff_type] += 1
    
    def reduce_energy(self):
        if self.player_selection:
            self.player_energy[self.player_selection] = max(0, self.player_energy[self.player_selection] - 1)
        if self.opponent_selection:
            self.opponent_energy[self.opponent_selection] = max(0, self.opponent_energy[self.opponent_selection] - 1) 