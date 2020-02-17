import re
import collections
from itertools import product

VERBOSE = True
SYSTEM_DICTIONARY = 'courses_data.json'
vowels = set('aeiouy')
alphabet = set('abcdefghijklmnopqrstuvwxyz')


def log(*args):
    if VERBOSE: print(''.join([str(x) for x in args]))


def words(text):
    # find words
    return re.findall('[a-z]+', text.lower())


def train(text, model=None):
    # update word model
    model = collections.defaultdict(lambda: 0) if model is None else model
    for word in words(text):
        model[word] += 1
    return model


def train_from_files(file_list, model=None):
    for f in file_list:
        model = train(open(f).read(), model)
    return model


def number_of_duplicates(string, idx):
    # return number of duplicates
    initial_idx = idx
    last = string[idx]
    while idx + 1 < len(string) and string[idx + 1] == last:
        idx += 1
    return idx - initial_idx


def hamming_distance(word1, word2):
    if word1 == word2:
        return 0
    dist = sum(map(str.__ne__, word1[:len(word2)], word2[:len(word1)]))
    dist = max([word2, word1]) if not dist else dist + abs(len(word2) - len(word1))
    return dist


def frequency(word, word_model):
    return word_model.get(word, 0)


def variants(word):
    # get possible word types
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def double_variants(word):
    # find multiple variants
    return set(s for w in variants(word) for s in variants(w))


def reductions(word):
    # remove duplicate letters
    word = list(word)
    # ['h','i', 'i', 'i'] becomes ['h', ['i', 'ii', 'iii']]
    for idx, l in enumerate(word):
        n = number_of_duplicates(word, idx)
        # if letter appears more than once in a row
        if n:
            # generate a flat list of options ('hhh' becomes ['h','hh','hhh'])
            flat_dupes = [l * (r + 1) for r in range(n + 1)][
                         :3]  # only take up to 3, there are no 4 letter repetitions in english
            # remove duplicate letters in original word
            for _ in range(n):
                word.pop(idx + 1)
            # replace original letter with flat list
            word[idx] = flat_dupes

    # ['h',['i','ii','iii']] becomes 'hi','hii','hiii'
    for p in product(*word):
        yield ''.join(p)


def vowel_swap(word):
    # swap vowels
    word = list(word)
    # ['h','i'] becomes ['h', ['a', 'e', 'i', 'o', 'u', 'y']]
    for idx, l in enumerate(word):
        if type(l) == list:
            pass  # dont mess with the reductions
        elif l in vowels:
            word[idx] = list(vowels)  # if l is a vowel, replace with all possible vowels

    # ['h',['i','ii','iii']] becomes 'hi','hii','hiii'
    for p in product(*word):
        yield ''.join(p)


def both(word):
    # find all permutations
    for reduction in reductions(word):
        for variant in vowel_swap(reduction):
            yield variant


def suggestions(word, actual_words, short_circuit=True):
    # find ideal spelling suggestion, return on first word or collect everything
    word = word.lower()
    if short_circuit:  # setting short_circuit makes the spellchecker much faster, but less accurate in some cases
        return ({word} & actual_words or  # caps     "USA" => "usa"
                set(reductions(word)) & actual_words or  # repeats  "hhii" => "hi"
                set(vowel_swap(word)) & actual_words or  # vowels   "weke" => "woke"
                set(variants(word)) & actual_words or  # other    "cal" => "cat"
                set(both(word)) & actual_words or  # both     "CUNsperrICY" => "conspiracy"
                set(double_variants(word)) & actual_words or  # other    "nmnster" => "manster"
                {"NO SUGGESTION"})
    else:
        return ({word} & actual_words or
                (set(reductions(word)) | set(vowel_swap(word)) | set(variants(word)) | set(both(word)) | set(
                    double_variants(word))) & actual_words or
                {"NO SUGGESTION"})


def best(inputted_word, suggestions, word_model=None):
    # choose best based off hamming distance or frequency
    suggestions = list(suggestions)

    def compare_hamming(one, two):
        score1 = hamming_distance(inputted_word, one)
        score2 = hamming_distance(inputted_word, two)
        return ((score2 > score1) - (score2 < score1))  # lower is better

    def compare_frequency(one, two):
        score1 = frequency(one, word_model)
        score2 = frequency(two, word_model)
        return ((score2 > score1) - (score2 < score1))  # higher is better

    freq_sorted = sorted(suggestions)[10:]  # take the top 10
    hamming_sorted = sorted(suggestions)[10:]  # take the top 10
    print('FREQ', freq_sorted)
    print('HAM', hamming_sorted)
    return ''


if __name__ == '__main__':
    # list of all possible words to start
    word_model = train(open(SYSTEM_DICTIONARY).read())
    real_words = set(word_model)

    # additional text to train
    texts = [
        'courses_corpus.html'
    ]
    # enhance the model with real bodies of english so we know which words are more common than others
    word_model = train_from_files(texts, word_model)

    log('Total set of words: ', len(word_model))
    log('Model Precision: %s' % (float(sum(word_model.values())) / len(word_model)))
    try:
        while True:
            word = str(input('>'))

            possibilities = suggestions(word, real_words, short_circuit=False)
            short_circuit_result = suggestions(word, real_words, short_circuit=True)
            if VERBOSE:
                print([(x, word_model[x]) for x in possibilities])
                print(best(word, possibilities, word_model))
                print('---')
            print([(x, word_model[x]) for x in short_circuit_result])
            if VERBOSE:
                print(best(word, short_circuit_result, word_model))

    except (EOFError, KeyboardInterrupt):
        exit(0)
