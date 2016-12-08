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


def random_words(sats=None):
    word = None
    sentence = []
    while word is not __END and (sats is None or len(sats) > 0):
        # This conditional will just end the sentence if the sat conditions
        # end. Should realistically reject a sentence of the wrong length and
        # find one that fits better, but ehh

        sat = sats.pop(0) if sats else _always_sat
        word = next_word(word, sat=sat)

        if word is __END:
            sats.insert(0, sat)
        else:
            sentence.append(word)
    return sentence


def _always_sat(word):
    return True


def _compound_sat(sat):
    return lambda x: x is __END or sat(x)


def sentence(words=None, sats=None):
    if not words:
        words = random_words(sats)
    return (' '.join(words) + _punctuation()).capitalize()


def next_word(prev_word=None, sat=_always_sat):
    l = list(filter(_compound_sat(sat), corpus[prev_word] if prev_word else list(corpus.keys())))
    return random.choice(l) if l else __END
