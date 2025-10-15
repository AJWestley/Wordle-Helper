from collections import Counter
from math import log2
from utils.wordle import generate_feedback, filter_word_list
from utils.dictionary import feedbacks


def entropy(guess: str, word_list: list[str]) -> float:
    N = len(word_list)
    if N == 0:
        return 0.0
    
    possible_patterns = Counter()
    for target in word_list:
        pattern = generate_feedback(guess, target)
        possible_patterns[pattern] += 1

    H = 0.0
    for count in possible_patterns.values():
        p = count / N
        H -= p * log2(p)

    return H

def top_n_entropy(word_list: list[str], n: int = 10) -> list[str]:
    scores = {word : entropy(word, word_list) for word in word_list}
    scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    return [item[0] for item in scores[:n]]

def two_step_lookahead(word_list: list[str]):
    top_first_guesses = top_n_entropy(word_list)
    resulting_options = {}
    for guess in top_first_guesses:
        ... # Finish this function