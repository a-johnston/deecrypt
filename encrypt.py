import string


__D = { c: 0 if ord(c) < ord('n') else 1 for c in string.ascii_lowercase }

def word_to_bit(word, D=__D):
    return sum(map(lambda c: D[c], word)) % 2


def char_to_bits(c):
    c = ord(c) - ord('a')
    return [(c >> i) & 1 for i in range(5)]
