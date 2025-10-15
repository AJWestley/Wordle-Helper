import os
import msvcrt
from random import choice
from utils.dictionary import word_choices
from utils.wordle import generate_feedback, filter_word_list

class KeyInput:
    NULL = 0
    UP = 1
    DOWN = 2
    ENTER = 3

class MenuOption:
    ADD_GUESS = 1
    SHOW_WORDS = 2
    GET_RECOMMENDATION = 3
    EXIT = 4


def get_number_of_words(word_list: set[str], containing: str = ''):
    return len([word for word in word_list if all(letter in word for letter in containing)])

def show_words(words: set[str], containing: str = ''):
    filtered_words = [word for word in words if all(letter in word for letter in containing)]
    for word in filtered_words:
        print(word)
    print(f"\nTotal words: {get_number_of_words(words, containing)}")

def get_word_recommendation(word_list: set[str], containing: str = ''):
    filtered_words = [word for word in word_list if all(letter in word for letter in containing)]
    return choice(filtered_words) if filtered_words else None

def display_menu(selected_option: int, guess_count: int, word_choices: set[str]):
    options = [
        'Add new guess and feedback',
        'Show possible words',
        'Get a word recommendation',
        'Exit'
    ]
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\nGuess {guess_count}: {get_number_of_words(word_choices)} possible words")
    for i, option in enumerate(options, 1):
        prefix = "-> " if i == selected_option else "   "
        print(f"{prefix}{i}. {option}")

def get_feedback() -> str:
    feedback = ''
    prompt = "Enter feedback (g=green, y=yellow, b=black) for the guess: "
    while len(feedback) != 5 or any(c not in 'gyb' for c in feedback):
        feedback = input(prompt).strip().lower()
        prompt = "Invalid input. Please enter exactly 5 characters using g, y, b: "
    return feedback

def get_guess() -> str:
    guess = ''
    prompt = "Enter your 5-letter guess: "
    while len(guess) != 5 or not guess.isalpha():
        guess = input(prompt).strip().upper()
        prompt = "Invalid input. Please enter exactly 5 alphabetic characters: "
    return guess

def get_key_input():
    while True:
        key = msvcrt.getch()
        if key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H':
                return KeyInput.UP
            elif key == b'P':
                return KeyInput.DOWN
        elif key == b'\r':
            return KeyInput.ENTER

def user_input(guess: int, word_choices: set[str]):
    selected_option = 0
    key_input = KeyInput.NULL
    while key_input != KeyInput.ENTER:
        display_menu(selected_option + 1, guess, word_choices)
        key_input = get_key_input()
        if key_input == KeyInput.UP:
            selected_option = (selected_option - 1) % 4
        elif key_input == KeyInput.DOWN:
            selected_option = (selected_option + 1) % 4
    return selected_option + 1

def main():
    words = word_choices.copy()
    guess_count = 1
    while True:
        user_input_value = user_input(guess_count, words)
        if user_input_value == MenuOption.ADD_GUESS:
            guess = get_guess()
            print()
            feedback = get_feedback()
            print()
            words = set(filter_word_list(words, guess, feedback))
            guess_count += 1
        elif user_input_value == MenuOption.SHOW_WORDS:
            containing = input("\nEnter letters that must be included (leave blank for none): ").strip().upper()
            print()
            show_words(words, containing)
            input("\nPress Enter to continue...")
        elif user_input_value == MenuOption.GET_RECOMMENDATION:
            containing = input("\nEnter letters that must be included (leave blank for none): ").strip().upper()
            print()
            recommendation = get_word_recommendation(words, containing)
            if recommendation:
                print(f"Recommended word: {recommendation}")
            else:
                print("No words found with the specified letters.")
            input("\nPress Enter to continue...")
        elif user_input_value == MenuOption.EXIT:
            print("\nExiting the program...\n")
            break

if __name__ == '__main__':
    main()