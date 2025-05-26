from exceptions import *
import random

# Complete with your own, just for fun :)
LIST_OF_WORDS = ['python', 'hangman', 'programming', 'computer', 'keyboard']


def _get_random_word(list_of_words):
    if not list_of_words or not isinstance(list_of_words, list):
        raise InvalidListOfWordsException()
    return random.choice(list_of_words)


def _mask_word(word):
    if not word or not isinstance(word, str):
        raise InvalidWordException()
    return '*' * len(word)


def _uncover_word(answer_word, masked_word, character):
    if not answer_word or not isinstance(answer_word, str):
        raise InvalidWordException()
    if not masked_word or not isinstance(masked_word, str):
        raise InvalidWordException()
    if len(answer_word) != len(masked_word):
        raise InvalidWordException()
    if not character or len(character) != 1 or not character.isalpha():
        raise InvalidGuessedLetterException()
    
    character = character.lower()
    answer_word = answer_word.lower()
    
    if character not in answer_word:
        return masked_word
    
    new_masked = list(masked_word)
    for idx, char in enumerate(answer_word):
        if char == character:
            new_masked[idx] = character
    
    return ''.join(new_masked)


def guess_letter(game, letter):
    letter = letter.lower()
    
    # Check if game is already over
    if game['remaining_misses'] <= 0 or game['answer_word'] == game['masked_word']:
        raise GameFinishedException()
    
    # Validate the letter
    if not letter or len(letter) != 1 or not letter.isalpha():
        raise InvalidGuessedLetterException()
    
    # Check if letter was already guessed
    if letter in game['previous_guesses']:
        raise InvalidGuessedLetterException()
    
    # Add to previous guesses
    game['previous_guesses'].append(letter)
    
    # Try to uncover the word
    old_masked = game['masked_word']
    new_masked = _uncover_word(
        game['answer_word'],
        old_masked,
        letter
    )
    
    # Update the game state
    game['masked_word'] = new_masked
    
    # Check if it was a miss
    if old_masked == new_masked:
        game['remaining_misses'] -= 1
    
    # Check win/lose conditions
    if game['answer_word'].lower() == new_masked.lower():
        raise GameWonException()
    
    if game['remaining_misses'] <= 0:
        raise GameLostException()


def start_new_game(list_of_words=None, number_of_guesses=5):
    if list_of_words is None:
        list_of_words = LIST_OF_WORDS

    word_to_guess = _get_random_word(list_of_words)
    masked_word = _mask_word(word_to_guess)
    game = {
        'answer_word': word_to_guess,
        'masked_word': masked_word,
        'previous_guesses': [],
        'remaining_misses': number_of_guesses,
    }

    return game
