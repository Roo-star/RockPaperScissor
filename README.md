# 5913 Final Project
Enhanced Rock-Paper-Scissors

## Rules
1. Player vs Computer, 5 rounds per game
2. Before each round:
   - Both sides choose a Buff (Rock/Paper/Scissors)
   - Selected move's energy +1 (base energy is 1)
3. Scoring rules:
   - Winner's score = 10 + (energy value × 10)
   - Loser loses points = Winner's score
   - Both sides' used Buff energy -1
   - When energy is 0, winning only gets 10 points
4. At the end of each round:
   - Both sides' health reduction = sum of both sides' card energy

## Implementation

### Tech Stack
- Python 3.x
- Pygame library for graphical interface

### Core Modules

1. Game Initialization
   - Window setup (800x600)
   - Resource loading (images, fonts)
   - Game constants definition

2. State Management
   - Game phases: select_buff -> opponent_buff -> select_card -> countdown -> show_battle -> show_result
   - Score system
   - Energy system
   - Round counting

3. Interface Rendering
   - Player/Computer area display
   - Energy icon drawing
   - Card display
   - Battle result display
   - Countdown animation

4. Game Logic
   - Buff selection mechanism
   - Computer AI decision
   - Win/Loss determination
   - Score calculation
   - Energy update

5. Event Handling
   - Mouse click response
   - Game flow control
   - State transitions

### File Structure

5913Final/
├── src/
│   ├── __init__.py
│   ├── main.py           # Main entry file
│   ├── config.py         # Configuration and constants
│   ├── game_state.py     # Game state management
│   ├── renderer.py       # Interface rendering
│   ├── game_logic.py     # Game core logic
│   └── resource_loader.py # Resource loading
├── imgs/
├── fonts/
└── README.md

### How to Run
1. Ensure dependencies are installed:   ```bash
   pip install pygame   ```
2. Execute in project root directory:   ```bash
   python run.py   ```

