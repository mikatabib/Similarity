from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

_stemmer = StemmerFactory().create_stemmer()


def stem(word: str):
    return _stemmer.stem(word)


def stem_pairs(pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    stemed = []
    for word, tag in pairs:
        stemed_word = _stemmer.stem(word)
        stemed.append((stemed_word, tag))
    return stemed


if __name__ == "__main__":
    print(stem("lelaguan"))
