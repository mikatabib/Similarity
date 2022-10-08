from pathlib import Path
wordlist = Path(__file__).parent / 'stopwords.list'

stopwords = []


def reload():
    with wordlist.open() as w:
        words = w.read().strip()
        return set(words.split())


def update():
    global stopwords
    stopwords = reload()


def contains(word: str) -> bool:
    return word in stopwords


def filter(seq: list, reload=True) -> list:
    if reload:
        update()

    return [x for x in seq if x not in stopwords]


def filter_from_pairs(seq: list[tuple], reload=True):
    if reload:
        update()

    li = []
    for lemma, tag in seq:
        if lemma not in stopwords:
            li.append((lemma, tag))
    return li


def save(words: list):
    words = sorted(words)
    with wordlist.open('w') as w:
        for word in words:
            w.write(word + '\n')


update()
