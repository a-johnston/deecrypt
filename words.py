import random
import string


corpus = {}

_punc = '.?!'

_punctual_p = { '.': 0, '!': 0, '?': 0 }

__END = object()

__legal_chars = string.ascii_lowercase + _punc + ' '


def _update_p_p(line):
    for c in _punc:
        _punctual_p[c] += line.count(c)


def _pre_normal(x):
    return ''.join(filter(lambda c: c in __legal_chars, x.strip().lower()))


def _multisplit(string, chars):
    if len(chars) == 0:
        return [string]

    l = []
    for x in string.split(chars[0]):
        l += _multisplit(x, chars[1:])

    return l


def _post_normal(line):
    return line.strip()


def _garner_sentence(sentence):
    words = sentence.split(' ') + [__END]

    for i in range(len(words) - 1):
        if words[i] not in corpus:
            corpus[words[i]] = []
        corpus[words[i]].append(words[i+1])


def _punctuation():
    x = ''.join([c * _punctual_p[c] for c in _punc])
    return random.choice(x)


def read(filename):
    with open(filename) as f:
        pre = ''
        for line in f.readlines():
            line = _pre_normal(line)

            if line == '':
                continue

            _update_p_p(line)

            parts = _multisplit(_pre_normal(line), '.!?')
            parts = [_post_normal(part) for part in parts if part]
            pre = pre + ' ' if pre else ''
            parts[0] = pre + parts[0]
            parts, pre = parts[:-1], parts[-1]

            for part in parts:
                _garner_sentence(part)
        _garner_sentence(pre)


def random_word():
    return random.choice(list(corpus.keys()))


def random_words():
    word = random_word()
    sentence = []

    while word is not __END:
        sentence.append(word)
        word = next(word)

    return sentence


def sentence(words=None):
    if not words:
        words = random_words()
    return (' '.join(words) + _punctuation()).capitalize()


def next(word):
    return random.choice(corpus[word])
