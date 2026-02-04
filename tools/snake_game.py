#!/usr/bin/env python3
"""
Advanced Snake Game - CLI Edition
A feature-rich terminal-based snake game with interactive UI
"""

import sys
import os
import time
import random
import threading
from collections import deque
from enum import Enum
import select

# Try to import required modules, provide helpful error if missing
try:
    import curses
except ImportError:
    print("Error: curses module not found. Install windows-curses on Windows:")
    print("  pip install windows-curses")
    sys.exit(1)


class Direction(Enum):
    """Snake movement directions"""
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class PowerUpType(Enum):
    """Types of power-ups available in the game"""
    SPEED_BOOST = "⚡"
    SLOW_DOWN = "🐌"
    DOUBLE_POINTS = "💎"
    INVINCIBLE = "🛡️"
    SHRINK = "📉"


class GameDifficulty(Enum):
    """Game difficulty levels"""
    EASY = ("Easy", 150, 1)
    MEDIUM = ("Medium", 100, 2)
    HARD = ("Hard", 70, 3)
    EXTREME = ("Extreme", 40, 5)


class PowerUp:
    """Represents a power-up in the game"""
    def __init__(self, position, power_type, duration=5):
        self.position = position
        self.type = power_type
        self.duration = duration
        self.spawn_time = time.time()
        self.lifetime = 10  # Power-up disappears after 10 seconds
    
    def is_expired(self):
        return time.time() - self.spawn_time > self.lifetime


class Snake:
    """Represents the snake with all its properties"""
    def __init__(self, start_pos, start_length=3):
        self.body = deque([start_pos])
        self.direction = Direction.RIGHT
        self.grow_pending = start_length - 1
        self.score = 0
        self.high_score = 0
        self.active_effects = {}
        
    def move(self, new_head):
        """Move snake to new position"""
        self.body.appendleft(new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    
    def grow(self, amount=1):
        """Schedule snake growth"""
        self.grow_pending += amount
    
    def check_collision(self, height, width):
        """Check if snake collided with walls or itself"""
        head = self.body[0]
        
        # Check wall collision
        if head[0] <= 0 or head[0] >= height - 1 or head[1] <= 0 or head[1] >= width - 1:
            return True
        
        # Check self collision
        if head in list(self.body)[1:]:
            return True
        
        return False
    
    def activate_effect(self, power_type, duration):
        """Activate a power-up effect"""
        self.active_effects[power_type] = time.time() + duration
    
    def update_effects(self):
        """Remove expired effects"""
        current_time = time.time()
        self.active_effects = {k: v for k, v in self.active_effects.items() if v > current_time}
    
    def has_effect(self, power_type):
        """Check if an effect is currently active"""
        return power_type in self.active_effects


class SnakeGame:
    """Main game controller"""
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.game_area_height = self.height - 8
        self.game_area_width = self.width - 2
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Snake
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)      # Food
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Power-ups
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)     # UI
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Special
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_RED)      # Game Over
        
        # Game state
        self.running = False
        self.paused = False
        self.game_over = False
        self.difficulty = GameDifficulty.MEDIUM
        self.snake = None
        self.food = None
        self.power_ups = []
        self.frame_count = 0
        
        # High score persistence
        self.high_score_file = os.path.expanduser("~/.snake_game_highscore")
        self.load_high_score()
        
        # Input handling
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        curses.curs_set(0)
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists(self.high_score_file):
                with open(self.high_score_file, 'r') as f:
                    return int(f.read().strip())
        except:
            pass
        return 0
    
    def save_high_score(self, score):
        """Save high score to file"""
        try:
            with open(self.high_score_file, 'w') as f:
                f.write(str(score))
        except:
            pass
    
    def show_menu(self):
        """Display main menu and get user choice"""
        self.stdscr.clear()
        menu_items = [
            "╔═══════════════════════════════════════╗",
            "║     🐍  ADVANCED SNAKE GAME  🐍      ║",
            "╚═══════════════════════════════════════╝",
            "",
            "Select Difficulty:",
            "",
            "  [1] Easy    - Slow speed, 1x points",
            "  [2] Medium  - Normal speed, 2x points",
            "  [3] Hard    - Fast speed, 3x points",
            "  [4] Extreme - Ultra fast, 5x points",
            "",
            "  [H] View High Scores",
            "  [I] Instructions",
            "  [Q] Quit",
            "",
            "Choose your challenge..."
        ]
        
        start_row = max(0, (self.height - len(menu_items)) // 2)
        
        for i, line in enumerate(menu_items):
            col = max(0, (self.width - len(line)) // 2)
            try:
                if i < 3:
                    self.stdscr.addstr(start_row + i, col, line, curses.color_pair(4) | curses.A_BOLD)
                else:
                    self.stdscr.addstr(start_row + i, col, line)
            except:
                pass
        
        self.stdscr.refresh()
        
        while True:
            key = self.stdscr.getch()
            if key == ord('1'):
                self.difficulty = GameDifficulty.EASY
                return True
            elif key == ord('2'):
                self.difficulty = GameDifficulty.MEDIUM
                return True
            elif key == ord('3'):
                self.difficulty = GameDifficulty.HARD
                return True
            elif key == ord('4'):
                self.difficulty = GameDifficulty.EXTREME
                return True
            elif key == ord('h') or key == ord('H'):
                self.show_high_scores()
                self.stdscr.clear()
                return self.show_menu()
            elif key == ord('i') or key == ord('I'):
                self.show_instructions()
                self.stdscr.clear()
                return self.show_menu()
            elif key == ord('q') or key == ord('Q'):
                return False
            time.sleep(0.05)
    
    def show_instructions(self):
        """Display game instructions"""
        self.stdscr.clear()
        instructions = [
            "╔═══════════════════════════════════════╗",
            "║          INSTRUCTIONS                ║",
            "╚═══════════════════════════════════════╝",
            "",
            "Controls:",
            "  W/↑ - Move Up",
            "  S/↓ - Move Down",
            "  A/← - Move Left",
            "  D/→ - Move Right",
            "  P   - Pause/Resume",
            "  Q   - Quit to Menu",
            "",
            "Gameplay:",
            "  • Eat food (●) to grow and score points",
            "  • Avoid walls and your own body",
            "  • Collect power-ups for special abilities",
            "",
            "Power-ups:",
            "  ⚡ Speed Boost  - Move faster temporarily",
            "  🐌 Slow Down   - Slow down for precision",
            "  💎 2x Points   - Double points for 5 seconds",
            "  🛡️ Invincible - Immunity from collisions",
            "  📉 Shrink     - Remove tail segments",
            "",
            "Press any key to return..."
        ]
        
        start_row = max(0, (self.height - len(instructions)) // 2)
        for i, line in enumerate(instructions):
            col = max(0, (self.width - len(line)) // 2)
            try:
                if i < 3:
                    self.stdscr.addstr(start_row + i, col, line, curses.color_pair(4) | curses.A_BOLD)
                else:
                    self.stdscr.addstr(start_row + i, col, line)
            except:
                pass
        
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        self.stdscr.getch()
        self.stdscr.nodelay(True)
    
    def show_high_scores(self):
        """Display high scores"""
        self.stdscr.clear()
        high_score = self.load_high_score()
        
        scores = [
            "╔═══════════════════════════════════════╗",
            "║          HIGH SCORES                 ║",
            "╚═══════════════════════════════════════╝",
            "",
            f"  Current Record: {high_score} points",
            "",
            "",
            "Press any key to return..."
        ]
        
        start_row = max(0, (self.height - len(scores)) // 2)
        for i, line in enumerate(scores):
            col = max(0, (self.width - len(line)) // 2)
            try:
                if i < 3:
                    self.stdscr.addstr(start_row + i, col, line, curses.color_pair(4) | curses.A_BOLD)
                else:
                    self.stdscr.addstr(start_row + i, col, line)
            except:
                pass
        
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        self.stdscr.getch()
        self.stdscr.nodelay(True)
    
    def initialize_game(self):
        """Initialize game state"""
        start_row = self.game_area_height // 2
        start_col = self.game_area_width // 2
        self.snake = Snake((start_row, start_col))
        self.food = self.spawn_food()
        self.power_ups = []
        self.running = True
        self.paused = False
        self.game_over = False
        self.frame_count = 0
    
    def spawn_food(self):
        """Spawn food at random empty location"""
        while True:
            row = random.randint(2, self.game_area_height - 2)
            col = random.randint(2, self.game_area_width - 2)
            pos = (row, col)
            
            if pos not in self.snake.body and not any(p.position == pos for p in self.power_ups):
                return pos
    
    def spawn_power_up(self):
        """Spawn a random power-up"""
        if len(self.power_ups) >= 3:  # Maximum 3 power-ups at once
            return
        
        power_type = random.choice(list(PowerUpType))
        
        while True:
            row = random.randint(2, self.game_area_height - 2)
            col = random.randint(2, self.game_area_width - 2)
            pos = (row, col)
            
            if pos not in self.snake.body and pos != self.food and not any(p.position == pos for p in self.power_ups):
                self.power_ups.append(PowerUp(pos, power_type))
                break
    
    def handle_input(self):
        """Handle user input"""
        key = self.stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            self.running = False
            return
        
        if key == ord('p') or key == ord('P'):
            self.paused = not self.paused
            return
        
        # Direction controls
        new_direction = None
        if key == ord('w') or key == ord('W') or key == curses.KEY_UP:
            new_direction = Direction.UP
        elif key == ord('s') or key == ord('S') or key == curses.KEY_DOWN:
            new_direction = Direction.DOWN
        elif key == ord('a') or key == ord('A') or key == curses.KEY_LEFT:
            new_direction = Direction.LEFT
        elif key == ord('d') or key == ord('D') or key == curses.KEY_RIGHT:
            new_direction = Direction.RIGHT
        
        # Prevent 180-degree turns
        if new_direction:
            opposite = {
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP,
                Direction.LEFT: Direction.RIGHT,
                Direction.RIGHT: Direction.LEFT
            }
            if new_direction != opposite.get(self.snake.direction):
                self.snake.direction = new_direction
    
    def update_game(self):
        """Update game state"""
        if self.paused or self.game_over:
            return
        
        # Update effects
        self.snake.update_effects()
        
        # Calculate new head position
        head = self.snake.body[0]
        dr, dc = self.snake.direction.value
        new_head = (head[0] + dr, head[1] + dc)
        
        # Check collision (unless invincible)
        if not self.snake.has_effect(PowerUpType.INVINCIBLE):
            if self.snake.check_collision(self.game_area_height, self.game_area_width):
                self.game_over = True
                return
        else:
            # Wrap around if invincible and hit wall
            new_head = (
                new_head[0] % self.game_area_height,
                new_head[1] % self.game_area_width
            )
            if new_head[0] == 0:
                new_head = (1, new_head[1])
            if new_head[1] == 0:
                new_head = (new_head[0], 1)
        
        # Move snake
        self.snake.move(new_head)
        
        # Check food collision
        if new_head == self.food:
            points = 10 * self.difficulty.value[2]
            if self.snake.has_effect(PowerUpType.DOUBLE_POINTS):
                points *= 2
            self.snake.score += points
            self.snake.grow(2)
            self.food = self.spawn_food()
        
        # Check power-up collision
        for power_up in self.power_ups[:]:
            if new_head == power_up.position:
                self.apply_power_up(power_up)
                self.power_ups.remove(power_up)
        
        # Remove expired power-ups
        self.power_ups = [p for p in self.power_ups if not p.is_expired()]
        
        # Spawn power-ups randomly
        if self.frame_count % 50 == 0 and random.random() < 0.3:
            self.spawn_power_up()
        
        self.frame_count += 1
    
    def apply_power_up(self, power_up):
        """Apply power-up effect"""
        if power_up.type == PowerUpType.SPEED_BOOST:
            self.snake.activate_effect(PowerUpType.SPEED_BOOST, 5)
        elif power_up.type == PowerUpType.SLOW_DOWN:
            self.snake.activate_effect(PowerUpType.SLOW_DOWN, 5)
        elif power_up.type == PowerUpType.DOUBLE_POINTS:
            self.snake.activate_effect(PowerUpType.DOUBLE_POINTS, 5)
        elif power_up.type == PowerUpType.INVINCIBLE:
            self.snake.activate_effect(PowerUpType.INVINCIBLE, 5)
        elif power_up.type == PowerUpType.SHRINK:
            # Remove up to 5 tail segments
            shrink_amount = min(5, len(self.snake.body) - 3)
            for _ in range(shrink_amount):
                if len(self.snake.body) > 3:
                    self.snake.body.pop()
            self.snake.score += 20
    
    def draw_border(self):
        """Draw game border"""
        # Top and bottom borders
        for col in range(self.game_area_width):
            try:
                self.stdscr.addstr(0, col, "═", curses.color_pair(4))
                self.stdscr.addstr(self.game_area_height - 1, col, "═", curses.color_pair(4))
            except:
                pass
        
        # Left and right borders
        for row in range(self.game_area_height):
            try:
                self.stdscr.addstr(row, 0, "║", curses.color_pair(4))
                self.stdscr.addstr(row, self.game_area_width - 1, "║", curses.color_pair(4))
            except:
                pass
        
        # Corners
        try:
            self.stdscr.addstr(0, 0, "╔", curses.color_pair(4))
            self.stdscr.addstr(0, self.game_area_width - 1, "╗", curses.color_pair(4))
            self.stdscr.addstr(self.game_area_height - 1, 0, "╚", curses.color_pair(4))
            self.stdscr.addstr(self.game_area_height - 1, self.game_area_width - 1, "╝", curses.color_pair(4))
        except:
            pass
    
    def draw_ui(self):
        """Draw game UI"""
        ui_row = self.game_area_height + 1
        
        # Score and difficulty
        score_text = f"Score: {self.snake.score}"
        diff_text = f"Difficulty: {self.difficulty.value[0]}"
        high_score = max(self.snake.score, self.load_high_score())
        high_score_text = f"High Score: {high_score}"
        
        try:
            self.stdscr.addstr(ui_row, 2, score_text, curses.color_pair(4) | curses.A_BOLD)
            self.stdscr.addstr(ui_row, 20, diff_text, curses.color_pair(4))
            self.stdscr.addstr(ui_row, 45, high_score_text, curses.color_pair(5) | curses.A_BOLD)
        except:
            pass
        
        # Active effects
        effects_row = ui_row + 1
        effects_text = "Active: "
        for effect in self.snake.active_effects:
            effects_text += f"{effect.value} "
        
        try:
            if self.snake.active_effects:
                self.stdscr.addstr(effects_row, 2, effects_text, curses.color_pair(3) | curses.A_BOLD)
        except:
            pass
        
        # Controls reminder
        controls_row = ui_row + 2
        controls = "Controls: WASD/Arrows=Move | P=Pause | Q=Quit"
        try:
            self.stdscr.addstr(controls_row, 2, controls, curses.color_pair(4))
        except:
            pass
        
        # Pause indicator
        if self.paused:
            pause_text = "⏸ PAUSED ⏸"
            try:
                col = (self.width - len(pause_text)) // 2
                self.stdscr.addstr(self.game_area_height // 2, col, pause_text, 
                                 curses.color_pair(5) | curses.A_BOLD | curses.A_BLINK)
            except:
                pass
    
    def draw_game(self):
        """Draw game state"""
        self.stdscr.clear()
        
        # Draw border
        self.draw_border()
        
        # Draw snake
        for i, segment in enumerate(self.snake.body):
            try:
                if i == 0:
                    # Snake head
                    char = "◉"
                    if self.snake.has_effect(PowerUpType.INVINCIBLE):
                        self.stdscr.addstr(segment[0], segment[1], char, 
                                         curses.color_pair(5) | curses.A_BOLD)
                    else:
                        self.stdscr.addstr(segment[0], segment[1], char, 
                                         curses.color_pair(1) | curses.A_BOLD)
                else:
                    # Snake body
                    char = "●" if i % 2 == 0 else "○"
                    self.stdscr.addstr(segment[0], segment[1], char, curses.color_pair(1))
            except:
                pass
        
        # Draw food
        try:
            self.stdscr.addstr(self.food[0], self.food[1], "●", 
                             curses.color_pair(2) | curses.A_BOLD)
        except:
            pass
        
        # Draw power-ups
        for power_up in self.power_ups:
            try:
                # Blinking effect for power-ups
                attr = curses.color_pair(3) | curses.A_BOLD
                if self.frame_count % 2 == 0:
                    attr |= curses.A_REVERSE
                self.stdscr.addstr(power_up.position[0], power_up.position[1], 
                                 power_up.type.value, attr)
            except:
                pass
        
        # Draw UI
        self.draw_ui()
        
        self.stdscr.refresh()
    
    def show_game_over(self):
        """Display game over screen"""
        high_score = self.load_high_score()
        
        if self.snake.score > high_score:
            self.save_high_score(self.snake.score)
            new_record = True
        else:
            new_record = False
        
        game_over_text = [
            "╔═══════════════════════════════════════╗",
            "║           GAME OVER!                 ║",
            "╚═══════════════════════════════════════╝",
            "",
            f"  Final Score: {self.snake.score}",
            f"  High Score: {max(self.snake.score, high_score)}",
            "",
        ]
        
        if new_record:
            game_over_text.append("  🎉 NEW HIGH SCORE! 🎉")
            game_over_text.append("")
        
        game_over_text.extend([
            "  [R] Play Again",
            "  [M] Main Menu",
            "  [Q] Quit",
        ])
        
        start_row = max(0, (self.height - len(game_over_text)) // 2)
        
        for i, line in enumerate(game_over_text):
            col = max(0, (self.width - len(line)) // 2)
            try:
                if i < 3:
                    self.stdscr.addstr(start_row + i, col, line, 
                                     curses.color_pair(6) | curses.A_BOLD)
                elif new_record and "NEW HIGH SCORE" in line:
                    self.stdscr.addstr(start_row + i, col, line, 
                                     curses.color_pair(5) | curses.A_BOLD | curses.A_BLINK)
                else:
                    self.stdscr.addstr(start_row + i, col, line)
            except:
                pass
        
        self.stdscr.refresh()
        
        while True:
            key = self.stdscr.getch()
            if key == ord('r') or key == ord('R'):
                return 'restart'
            elif key == ord('m') or key == ord('M'):
                return 'menu'
            elif key == ord('q') or key == ord('Q'):
                return 'quit'
            time.sleep(0.05)
    
    def run(self):
        """Main game loop"""
        while True:
            # Show menu
            if not self.show_menu():
                break
            
            # Initialize game
            self.initialize_game()
            
            # Calculate game speed based on difficulty and effects
            base_delay = self.difficulty.value[1] / 1000.0
            
            # Game loop
            while self.running:
                self.handle_input()
                self.update_game()
                self.draw_game()
                
                if self.game_over:
                    choice = self.show_game_over()
                    if choice == 'restart':
                        self.initialize_game()
                        continue
                    elif choice == 'menu':
                        break
                    else:
                        return
                
                # Adjust speed based on active effects
                delay = base_delay
                if self.snake.has_effect(PowerUpType.SPEED_BOOST):
                    delay *= 0.5
                elif self.snake.has_effect(PowerUpType.SLOW_DOWN):
                    delay *= 1.5
                
                time.sleep(delay)


def main(stdscr):
    """Main entry point"""
    # Check terminal size
    height, width = stdscr.getmaxyx()
    if height < 25 or width < 60:
        stdscr.clear()
        msg = "Terminal too small! Need at least 60x25"
        stdscr.addstr(height // 2, (width - len(msg)) // 2, msg)
        stdscr.refresh()
        stdscr.getch()
        return
    
    game = SnakeGame(stdscr)
    game.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nThanks for playing! 🐍")
    except Exception as e:
        print(f"\nError: {e}")
        print("If you see 'addwstr' errors, your terminal may not support Unicode.")
        print("Try using a different terminal emulator.")