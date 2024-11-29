import random

def determine_winner(player_move, opponent_move):
    if player_move == opponent_move:
        return 'tie'
    elif ((player_move == 'rock' and opponent_move == 'scissors') or
          (player_move == 'paper' and opponent_move == 'rock') or
          (player_move == 'scissors' and opponent_move == 'paper')):
        return 'player'
    else:
        return 'opponent'

def calculate_score(energy_value):
    return 10 + (energy_value * 10)

def opponent_choose_buff(game_state):
    return random.choice(game_state.card_types)

def opponent_choose_move(game_state):
    # Choose card with highest energy
    max_energy = max(game_state.opponent_energy.values())
    possible_choices = [card for card, energy in game_state.opponent_energy.items() 
                       if energy == max_energy]
    return random.choice(possible_choices) 