from functools import reduce


def group(n, iterable):
    return list(zip(*[iter(iterable)] * n))


def words_for_nerds(text):
    legal = lambda c: c >= ord('a') and c <= ord('z')

    words = text.strip().lower().split(' ')
    codes = [[ord(c) for c in word if legal(ord(c))] for word in words]

    return [list(filter(legal, word)) for word in codes]


def make_dict():
    half1 = list(zip(range(ord('a'), ord('m') + 1), [0] * 13))
    half2 = list(zip(range(ord('n'), ord('z') + 1), [1] * 13))

    return dict(half1 + half2)


def twos(bits):
    bits = list(bits)
    return reduce(lambda a, b: 2 * a + b, bits, 0)


def nerdy_words_to_twos(words):
    d = make_dict()

    bits = [[d[c] for c in word] for word in words]
    par = map(lambda x: sum(x) % 2, bits)

    groups = group(5, par)

    return map(twos, groups)


def decrypt(text):
    nerds = words_for_nerds(text)
    twos = nerdy_words_to_twos(nerds)

    chars = [chr(ord('a') + x) for x in twos]
    return ''.join(chars)
