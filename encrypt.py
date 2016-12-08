import string
from . import words


__D = { c: 0 if ord(c) < ord('n') else 1 for c in string.ascii_lowercase }


def word_to_bit(word, D=__D):
    return sum(map(lambda c: D[c], word)) % 2


def sat_bit(bit):
    return lambda word: word_to_bit(word) == bit


def char_to_bits(c):
    c = ord(c) - ord('a')
    return [(c >> (4 - i)) & 1 for i in range(5)]


def words_to_bits(text):
    return sum([char_to_bits(c) for c in text], [])


def words_to_words(text):
    bits = words_to_bits(text)
    sats = [sat_bit(bit) for bit in bits]

    sentences = []

    while sats:
        sentences.append(words.sentence(sats=sats))

    return ' '.join(sentences)


def encrypt(text):
    text = ''.join(filter(lambda c: c in string.ascii_lowercase, text))
    return words_to_words(text)
