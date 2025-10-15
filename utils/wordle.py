from utils.dictionary import word_choices

def generate_feedback(guess: str, target: str) -> str:
    if len(guess) != len(target):
        raise ValueError('Guess and target should have the same length.')
    guess = guess.upper()
    target = target.upper()
    feedback = ['b'] * len(guess)
    for i, letter in enumerate(target):
        if letter == guess[i]:
            feedback[i] = 'g'
        else:
            idx = guess.find(letter)
            if idx != -1 and feedback[idx] == 'b':
                feedback[idx] = 'y'
    return ''.join(feedback)

def filter_word_list(word_list: set[str], guess: str, feedback: str):
    return list(filter(lambda word: (generate_feedback(guess, word) == feedback), word_list))

if __name__ == '__main__':
    print(generate_feedback('llama', 'peels'))
    print(len(word_choices))
    print(len(filter_word_list(word_choices, 'llama', generate_feedback('llama', 'peels'))))