from random import choice

def randomWord():
    words = open("words.txt"). read().splitlines()
    word = choice(words)
    return word


print(randomWord())
