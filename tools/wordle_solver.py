import sys
import os
import urllib.request
import collections

# --- CONFIGURATION ---
WORD_LIST_URL = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"
HARDCODED_FALLBACK = ["slate", "sauce", "slice", "shale", "saute", "share", "sooty", "shine", "suite", "crane"]

class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    GRAY = "\033[90m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

class WordleSolver:
    def __init__(self):
        self.words = []
        self.possible_words = []

    def load_words(self):
        """Fetches the official Wordle list."""
        print(f"{Colors.GRAY}Downloading word list...{Colors.RESET}")
        try:
            with urllib.request.urlopen(WORD_LIST_URL, timeout=5) as response:
                data = response.read().decode('utf-8')
                self.words = [w.strip().lower() for w in data.splitlines() if len(w.strip()) == 5]
            print(f"{Colors.GREEN}✔ Loaded {len(self.words)} words.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}✘ Could not download list. Using fallback.{Colors.RESET}")
            self.words = HARDCODED_FALLBACK
        
        self.possible_words = self.words[:]

    def calculate_scores(self):
        """Scores words based on frequency of unique letters."""
        if not self.possible_words: return {}
        letter_counts = collections.Counter()
        for word in self.possible_words:
            letter_counts.update(set(word))
        scores = {}
        for word in self.possible_words:
            scores[word] = sum(letter_counts[c] for c in set(word))
        return scores

    def filter_words(self, guess, pattern):
        """Filters words based on pattern: G=Green, Y=Yellow, X=Gray"""
        new_candidates = []
        for word in self.possible_words:
            match = True
            word_counts = collections.Counter(word)
            
            # Pass 1: Handle GREENS
            for i, (g_char, p_char) in enumerate(zip(guess, pattern)):
                if p_char == 'G':
                    if word[i] != g_char:
                        match = False; break
                    word_counts[g_char] -= 1
            if not match: continue

            # Pass 2: Handle YELLOWS and GRAYS
            for i, (g_char, p_char) in enumerate(zip(guess, pattern)):
                if p_char == 'G': continue
                elif p_char == 'Y':
                    if word[i] == g_char or word_counts[g_char] == 0:
                        match = False; break
                    word_counts[g_char] -= 1
                elif p_char == 'X':
                    if word_counts[g_char] > 0:
                        match = False; break
            
            if match: new_candidates.append(word)
        self.possible_words = new_candidates

    def recommend(self):
        scores = self.calculate_scores()
        ranked = sorted(self.possible_words, key=lambda w: scores.get(w, 0), reverse=True)
        return ranked[:10]

    def main_loop(self):
        Colors.cls()
        print(f"{Colors.BOLD}{Colors.GREEN}=== Wordle Solver CLI ==={Colors.RESET}")
        self.load_words()
        
        print("\nINSTRUCTIONS:")
        print("1. Enter the word you guessed in Wordle.")
        print("2. Enter the 5-letter color pattern:")
        print(f"   - {Colors.GREEN}G{Colors.RESET} for Green")
        print(f"   - {Colors.YELLOW}Y{Colors.RESET} for Yellow")
        print(f"   - {Colors.GRAY}X{Colors.RESET} for Gray")
        print(f"   Example: If 'A' is Green and 'B' is Gray, type pattern like: {Colors.BOLD}GXYXX{Colors.RESET}")
        print("-" * 50)

        print(f"\n{Colors.BOLD}Starter Suggestion:{Colors.RESET} {Colors.YELLOW}slate{Colors.RESET}")

        while True:
            print(f"\n{Colors.GRAY}Words left: {len(self.possible_words)}{Colors.RESET}")
            
            guess = input(f"{Colors.BOLD}Input your Guess > {Colors.RESET}").strip().lower()
            if guess == 'exit': break
            if len(guess) != 5:
                print(f"{Colors.RED}Error: Guess must be exactly 5 letters.{Colors.RESET}")
                continue

            pattern = input(f"{Colors.BOLD}Input 5 Colors (G/Y/X) > {Colors.RESET}").strip().upper()
            
            # --- IMPROVED ERROR HANDLING ---
            if len(pattern) != 5:
                print(f"{Colors.RED}Error: You entered {len(pattern)} chars. Pattern must be exactly 5 characters (e.g. GXYXX).{Colors.RESET}")
                continue
            if any(c not in 'GYX' for c in pattern):
                print(f"{Colors.RED}Error: Invalid characters. Use only G, Y, or X.{Colors.RESET}")
                continue

            prev_count = len(self.possible_words)
            self.filter_words(guess, pattern)
            curr_count = len(self.possible_words)
            
            if curr_count == 0:
                print(f"{Colors.RED}No words match! You might have entered a wrong pattern.{Colors.RESET}")
                break
            elif curr_count == 1:
                print(f"\n{Colors.GREEN}🎉 The word is: {self.possible_words[0].upper()}!{Colors.RESET}")
                break
            else:
                top = self.recommend()
                print(f"\n{Colors.BOLD}Best Next Guesses:{Colors.RESET}")
                print(" | ".join([f"{Colors.YELLOW}{w.upper()}{Colors.RESET}" for w in top[:5]]))

if __name__ == "__main__":
    try:
        WordleSolver().main_loop()
    except KeyboardInterrupt:
        print("\nExiting.")