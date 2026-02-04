import time
import random
import os
import json
import difflib
import sys
from datetime import datetime

# --- CONFIGURATION ---
HISTORY_FILE = "typing_stats.json"

# --- SAMPLE TEXTS ---
SENTENCES = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is an interpreted, high-level and general-purpose programming language.",
    "To be or not to be, that is the question.",
    "A journey of a thousand miles begins with a single step.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "In the middle of difficulty lies opportunity.",
    "Clean code always looks like it was written by someone who cares.",
    "Debugging is twice as hard as writing the code in the first place.",
    "Complexity is the enemy of execution.",
    "Premature optimization is the root of all evil in programming."
]

# --- COLORS ---
class Colors:
    HEADER = "\033[95m"  # Added this missing attribute
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

class TypingTest:
    def __init__(self):
        self.load_history()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r') as f:
                    self.history = json.load(f)
            except:
                self.history = []
        else:
            self.history = []

    def save_history(self, wpm, accuracy):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "wpm": round(wpm, 1),
            "accuracy": round(accuracy, 1)
        }
        self.history.append(entry)
        # Keep only last 50 records
        if len(self.history) > 50:
            self.history.pop(0)
            
        with open(HISTORY_FILE, 'w') as f:
            json.dump(self.history, f, indent=4)

    def get_diff_string(self, target, actual):
        """Highlights errors in red and correct chars in green."""
        output = ""
        matcher = difflib.SequenceMatcher(None, target, actual)
        
        for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
            if opcode == 'equal':
                output += f"{Colors.GREEN}{target[a0:a1]}{Colors.RESET}"
            elif opcode == 'replace':
                output += f"{Colors.RED}{actual[b0:b1]}{Colors.RESET}"
            elif opcode == 'insert':
                output += f"{Colors.RED}{actual[b0:b1]}{Colors.RESET}"
            elif opcode == 'delete':
                output += f"{Colors.YELLOW}_{Colors.RESET}" * (a1 - a0)
        return output

    def countdown(self):
        print("\nStarting in...")
        for i in range(3, 0, -1):
            sys.stdout.write(f"\r{Colors.BOLD}{i}...{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write(f"\r{Colors.BOLD}{Colors.GREEN}GO!{Colors.RESET}   \n")

    def run_test(self):
        Colors.cls()
        print(f"{Colors.BLUE}=== ⚡ TYPING SPEED TEST ⚡ ==={Colors.RESET}")
        
        target_text = random.choice(SENTENCES)
        print(f"\n{Colors.YELLOW}Type the following text exactly:{Colors.RESET}")
        print(f"{Colors.BOLD}┌{'─'*len(target_text)}┐")
        print(f"│{target_text}│")
        print(f"└{'─'*len(target_text)}┘{Colors.RESET}")
        
        self.countdown()
        
        start_time = time.time()
        try:
            user_input = input(f"{Colors.BLUE}>> {Colors.RESET}")
        except KeyboardInterrupt:
            return

        end_time = time.time()
        time_taken = end_time - start_time
        
        # --- CALCULATIONS ---
        # WPM = (Characters / 5) / (Minutes)
        word_count = len(user_input) / 5
        minutes = time_taken / 60
        wpm = word_count / minutes if minutes > 0 else 0
        
        # Accuracy using SequenceMatcher
        matcher = difflib.SequenceMatcher(None, target_text, user_input)
        accuracy = matcher.ratio() * 100

        # --- RESULTS ---
        print("\n" + "="*40)
        print(f"⏱️  Time:     {time_taken:.2f} seconds")
        print(f"🚀 Speed:    {Colors.GREEN}{wpm:.1f} WPM{Colors.RESET}")
        print(f"🎯 Accuracy: {Colors.BLUE}{accuracy:.1f}%{Colors.RESET}")
        print("="*40)
        
        # Visual Diff
        if accuracy < 100:
            print(f"\n{Colors.BOLD}Corrections:{Colors.RESET}")
            print(f"Expected: {target_text}")
            print(f"You Typed: {self.get_diff_string(target_text, user_input)}")
            print(f"({Colors.GREEN}Green=Correct{Colors.RESET}, {Colors.RED}Red=Wrong{Colors.RESET}, {Colors.YELLOW}_=Missing{Colors.RESET})")

        self.save_history(wpm, accuracy)
        input("\nPress Enter to continue...")

    def show_stats(self):
        Colors.cls()
        print(f"{Colors.BLUE}=== 📊 HISTORICAL PROGRESS ==={Colors.RESET}")
        if not self.history:
            print("No tests taken yet.")
        else:
            print(f"{'DATE':<20} {'WPM':<10} {'ACCURACY'}")
            print("-" * 40)
            # Show last 10
            for entry in reversed(self.history[-10:]):
                wpm_col = f"{Colors.GREEN}{entry['wpm']}{Colors.RESET}"
                acc_col = f"{Colors.BLUE}{entry['accuracy']}%{Colors.RESET}"
                print(f"{entry['date']:<20} {wpm_col:<19} {acc_col}")
            
            # Averages
            avg_wpm = sum(e['wpm'] for e in self.history) / len(self.history)
            avg_acc = sum(e['accuracy'] for e in self.history) / len(self.history)
            print("-" * 40)
            print(f"{Colors.BOLD}Average Speed:{Colors.RESET}    {avg_wpm:.1f} WPM")
            print(f"{Colors.BOLD}Average Accuracy:{Colors.RESET} {avg_acc:.1f}%")
        
        input("\nPress Enter to return...")

    def main_menu(self):
        while True:
            Colors.cls()
            print(f"{Colors.BOLD}{Colors.BLUE}")
            # Used triple quotes to safely handle backslashes in ASCII art
            print(r"""
  _______          _              _______        _   
 |__   __|        (_)            |__   __|      | |  
    | |_   _ _ __  _ _ __   __ _    | | ___  ___| |_ 
    | | | | | '_ \| | '_ \ / _` |   | |/ _ \/ __| __|
    | | |_| | |_) | | | | | (_| |   | |  __/\__ \ |_ 
    |_|\__, | .__/|_|_| |_|\__, |   |_|\___||___/\__|
        __/ | |             __/ |                    
       |___/|_|            |___/                     
            """)
            print(f"{Colors.RESET}{Colors.HEADER}   >>> CLI Typing Speed Trainer <<<{Colors.RESET}\n")
            print("1. 🚀 Start New Test")
            print("2. 📊 View Statistics")
            print("3. ❌ Exit")
            
            choice = input(f"\n{Colors.BLUE}>> {Colors.RESET}").strip()
            
            if choice == '1':
                self.run_test()
            elif choice == '2':
                self.show_stats()
            elif choice == '3':
                print("Keep practicing! Goodbye.")
                break

if __name__ == "__main__":
    app = TypingTest()
    app.main_menu()