"""
Text File Analyzer - Analyze text files for readability, word frequency, and statistics.
Works with .txt, .md, .py, .js, .html, and other text-based files.
"""

import os
import re
import math
from collections import Counter
import sys


class TextAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.content = ""
        self.stats = {}
    

    # Load and read the text file
    def load_file(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except FileNotFoundError:
            print(f"❌ Error: File '{self.filepath}' not found.")
            return False
        except UnicodeDecodeError:
            print(f"❌ Error: Cannot read '{self.filepath}'. Not a text file.")
            return False
    

    # Count total words in the text
    def count_words(self):
        words = re.findall(r'\b\w+\b', self.content.lower())
        return len(words)
    

    # Count characters (excluding spaces)
    def count_characters(self):
        return len(self.content.replace(' ', ''))
    

    # Count sentences by looking for sentence endings
    def count_sentences(self):
        sentences = re.split(r'[.!?]+', self.content)
        return len([s for s in sentences if s.strip()])
    

    # Calculate estimated reading time (200 words per minute)
    def calculate_reading_time(self, word_count):
        minutes = word_count / 200
        if minutes < 1:
            return "< 1 minute"
        elif minutes < 60:
            return f"{int(minutes)} minutes"
        else:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            return f"{hours}h {mins}m"
    

    # Calculate Flesch-Kincaid readability score
    def calculate_readability(self):
        if not self.content.strip():
            return 0
        
        sentences = re.split(r'[.!?]+', self.content)
        sentences = [s for s in sentences if s.strip()]
        
        if len(sentences) == 0:
            return 0
        
        words = re.findall(r'\b\w+\b', self.content)
        syllables = sum(self.count_syllables(word) for word in words)
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words) if words else 0
        
        # Flesch-Kincaid formula
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        return max(0, min(100, score))
    

    # Simple syllable counting algorithm
    def count_syllables(self, word):
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        prev_char_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_char_was_vowel:
                syllable_count += 1
            prev_char_was_vowel = is_vowel
        
        # Handle silent 'e' at the end
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    

    # Convert readability score to reading level
    def get_reading_level(self, score):
        if score >= 90:
            return "5th grade"
        elif score >= 80:
            return "6th grade"
        elif score >= 70:
            return "7th grade"
        elif score >= 60:
            return "8th grade"
        elif score >= 50:
            return "9th grade"
        elif score >= 40:
            return "10th grade"
        elif score >= 30:
            return "11th grade"
        else:
            return "College level"
    

    # Get most common words (excluding common stop words)
    def get_word_frequency(self, top_n=10):
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        words = re.findall(r'\b\w+\b', self.content.lower())
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return Counter(filtered_words).most_common(top_n)
    

    def get_file_size(self):
        size = os.path.getsize(self.filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    

    """Perform complete text analysis"""
    def analyze(self):
        if not self.load_file():
            return False
        
        word_count = self.count_words()
        char_count = self.count_characters()
        sentence_count = self.count_sentences()
        readability_score = self.calculate_readability()
        reading_level = self.get_reading_level(readability_score)
        reading_time = self.calculate_reading_time(word_count)
        word_frequency = self.get_word_frequency()
        file_size = self.get_file_size()
        
        self.stats = {
            'file_path': self.filepath,
            'file_size': file_size,
            'word_count': word_count,
            'char_count': char_count,
            'sentence_count': sentence_count,
            'readability_score': readability_score,
            'reading_level': reading_level,
            'reading_time': reading_time,
            'word_frequency': word_frequency
        }
        
        return True
    

    def display_results(self):
        if not self.stats:
            return
        
        print("\n" + "="*50)
        print("📊 TEXT ANALYSIS RESULTS")
        print("="*50)
        print(f"📄 File: {self.stats['file_path']}")
        print(f"💾 Size: {self.stats['file_size']}")
        print(f"📊 Words: {self.stats['word_count']:,}")
        print(f"📝 Characters: {self.stats['char_count']:,}")
        print(f"📖 Sentences: {self.stats['sentence_count']}")
        print(f"⏱️ Reading Time: {self.stats['reading_time']}")
        print(f"📚 Readability Score: {self.stats['readability_score']:.1f}/100")
        print(f"🎓 Reading Level: {self.stats['reading_level']}")
        
        if self.stats['word_frequency']:
            print(f"\n--- Top {len(self.stats['word_frequency'])} Words ---")
            for i, (word, count) in enumerate(self.stats['word_frequency'], 1):
                print(f"{i:2d}. {word:<15} ({count} times)")
        
        print("="*50)


def main():
    if len(sys.argv) != 2:
        print("Usage: python text_analyzer.py <file_path>")
        print("Example: python text_analyzer.py document.txt")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"❌ Error: File '{filepath}' does not exist.")
        sys.exit(1)
    
    analyzer = TextAnalyzer(filepath)
    
    if analyzer.analyze():
        analyzer.display_results()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
