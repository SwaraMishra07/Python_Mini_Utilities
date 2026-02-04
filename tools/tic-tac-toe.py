import os
import time
import random
import math
import sys

# --- CONFIGURATION & VISUALS ---
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"   # For 'O'
    RED = "\033[91m"    # For 'X'
    GREEN = "\033[92m"  # For Wins
    YELLOW = "\033[93m" # For UI elements
    GRAY = "\033[90m"   # Fixed: Added missing color
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

class GameState:
    def __init__(self):
        self.player_wins = 0
        self.ai_wins = 0
        self.draws = 0

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)] # 3x3 Grid
        self.current_winner = None

    def print_board(self):
        print(f"\n{Colors.BOLD}   Current Board:{Colors.RESET}")
        # Cleaner ASCII Art Grid
        for i in range(3):
            row = self.board[i*3:(i+1)*3]
            formatted_row = []
            for cell in row:
                if cell == 'X':
                    formatted_row.append(f"{Colors.RED} X {Colors.RESET}")
                elif cell == 'O':
                    formatted_row.append(f"{Colors.BLUE} O {Colors.RESET}")
                else:
                    formatted_row.append("   ")
            
            print("   " + "│".join(formatted_row))
            if i < 2:
                print("   " + "───┼───┼───") # Professional grid lines
        print("\n")

    def print_board_nums(self):
        print(f"{Colors.GRAY}   Reference Map:{Colors.RESET}")
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for i, row in enumerate(number_board):
            print("   " + " │ ".join(row))
            if i < 2:
                print("   " + "───┼───┼───")
        print("")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        # Check Row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind+1)*3]
        if all([spot == letter for spot in row]): return True
        
        # Check Column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]): return True

        # Check Diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]): return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]): return True
        return False

# --- PLAYERS ---
class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter
        self.is_bot = False

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            try:
                prompt = f"{Colors.BOLD}Player {self.letter} turn (0-8): {Colors.RESET}"
                square = input(prompt)
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print(f"{Colors.RED}Invalid square. Try again.{Colors.RESET}")
        return val

class SmartAI:
    def __init__(self, letter):
        self.letter = letter
        self.opponent = 'O' if letter == 'X' else 'X'
        self.is_bot = True

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            return 4 # Optimization: Take center
        
        print(f"{Colors.GRAY}AI is thinking...{Colors.RESET}")
        square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = self.opponent

        # Base cases: Check if previous move won
        if state.current_winner == other_player:
            # Score depends on empty squares (win faster = better)
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # 1. SIMULATE MOVE
            state.board[possible_move] = player
            
            # CRITICAL FIX: Check if this move wins!
            if state.check_winner(possible_move, player):
                state.current_winner = player
            
            # 2. RECURSE
            sim_score = self.minimax(state, other_player if player == max_player else max_player)
            
            # 3. UNDO MOVE
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            # 4. UPDATE BEST SCORE
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

class RandomAI:
    def __init__(self, letter):
        self.letter = letter
        self.is_bot = True
    def get_move(self, game):
        return random.choice(game.available_moves())

# --- GAME LOOP ---
def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                Colors.cls() # Clear screen for clean UI
                game.print_board_nums()
                
                # Dynamic Print Message
                if letter == 'O':
                    name = "AI" if o_player.is_bot else "Player 2"
                    color = Colors.YELLOW if o_player.is_bot else Colors.BLUE
                else:
                    name = "Player 1"
                    color = Colors.RED
                
                print(f"{color}{name} ({letter}) chose square {square}{Colors.RESET}")
                game.print_board()
            
            if game.current_winner:
                if print_game:
                    if letter == 'X':
                        print(f"{Colors.GREEN}{Colors.BOLD}🎉 PLAYER 1 (X) WINS! 🎉{Colors.RESET}")
                    elif letter == 'O' and o_player.is_bot:
                        print(f"{Colors.RED}{Colors.BOLD}🤖 AI (O) WINS! (Resistance is futile){Colors.RESET}")
                    else:
                        print(f"{Colors.BLUE}{Colors.BOLD}🎉 PLAYER 2 (O) WINS! 🎉{Colors.RESET}")
                return letter
            
            letter = 'O' if letter == 'X' else 'X'
        
        # Delay only if it's a bot's turn to act
        if print_game and ((letter == 'O' and o_player.is_bot) or (letter == 'X' and x_player.is_bot)):
            time.sleep(0.6)

    if print_game:
        print(f"{Colors.GRAY}It's a tie!{Colors.RESET}")
    return 'Draw'

# --- MAIN MENU ---
def main_menu():
    stats = GameState()
    
    while True:
        Colors.cls()
        print(f"{Colors.BOLD}{Colors.BLUE}")
        print(r"""
  _______ _        _______           _______         
 |__   __(_)      |__   __|         |__   __|        
    | |   _  ___     | | __ _  ___     | | ___   ___ 
    | |  | |/ __|    | |/ _` |/ __|    | |/ _ \ / _ \
    | |  | | (__     | | (_| | (__     | | (_) |  __/
    |_|  |_|\___|    |_|\__,_|\___|    |_|\___/ \___|
        """)
        print(f"{Colors.RESET}{Colors.HEADER}    >>> PROFESSIONAL EDITION <<<{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}SCOREBOARD:{Colors.RESET} P1 Wins: {stats.player_wins} | P2/AI Wins: {stats.ai_wins} | Draws: {stats.draws}")
        print("-" * 60)
        print("1. ⚔️  Vs Unbeatable AI (Hard Mode)")
        print("2. 🎲 Vs Random Bot (Easy Mode)")
        print("3. 👥 Two Player Mode (Local)")
        print("4. ❌ Exit")

        choice = input(f"\n{Colors.BLUE}>> {Colors.RESET}").strip()

        if choice == '4':
            print("Goodbye!")
            break
            
        t = TicTacToe()
        
        if choice == '1':
            x_player = HumanPlayer('X')
            o_player = SmartAI('O')
            result = play(t, x_player, o_player, print_game=True)
            if result == 'X': stats.player_wins += 1
            elif result == 'O': stats.ai_wins += 1
            else: stats.draws += 1
            
        elif choice == '2':
            x_player = HumanPlayer('X')
            o_player = RandomAI('O')
            result = play(t, x_player, o_player, print_game=True)
            if result == 'X': stats.player_wins += 1
            elif result == 'O': stats.ai_wins += 1
            else: stats.draws += 1
            
        elif choice == '3':
            x_player = HumanPlayer('X')
            o_player = HumanPlayer('O')
            result = play(t, x_player, o_player, print_game=True)
            if result == 'X': stats.player_wins += 1
            elif result == 'O': stats.ai_wins += 1
            else: stats.draws += 1
            
        input(f"\n{Colors.GRAY}Press Enter to play again...{Colors.RESET}")

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting.")