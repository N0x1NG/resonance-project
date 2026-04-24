"""
Text entropy calculator for PAK research
Higher entropy = more information density / unpredictability
"""

import math
from collections import Counter


def calculate_entropy(text: str) -> float:
    """
    Calculate Shannon entropy of text.
    
    Returns:
        float: Entropy in bits per character
    """
    if not text:
        return 0.0
    
    freq = Counter(text.lower())
    total = len(text)
    
    entropy = 0.0
    for count in freq.values():
        probability = count / total
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return round(entropy, 4)


def calculate_word_entropy(text: str) -> float:
    """
    Calculate entropy at word level.
    """
    if not text:
        return 0.0
    
    words = text.lower().split()
    if not words:
        return 0.0
    
    freq = Counter(words)
    total = len(words)
    
    entropy = 0.0
    for count in freq.values():
        probability = count / total
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return round(entropy, 4)


if __name__ == "__main__":
    test_texts = [
        "aaaaaaaaaa",
        "the quick brown fox jumps over the lazy dog",
        "x7$kL9#mP2@nQ5&vR8*wT1!yU4^zA3%bC6",
    ]
    
    for text in test_texts:
        char_e = calculate_entropy(text)
        print(f"Text: '{text[:30]}...' → Entropy: {char_e}")
