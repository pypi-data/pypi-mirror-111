from random import choice

def get_random():
    words = open("words.txt"). read().splitlines()
    word = choice(words)
    return word
