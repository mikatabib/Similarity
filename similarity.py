import wn
import stemmer
import stopword
from pathlib import Path
from wn.similarity import wup
from utils import text_normalizer
from tagger import tagger


_tagger = tagger.Tagger()
wn.config.data_directory = Path().cwd() / "wn_data"
_wordnet = wn.Wordnet("omw-id:1.4")


def calculate(sentenceA: str, sentenceB: str) -> float:
    # step 0: normalize
    normalizedA: str = text_normalizer(sentenceA)
    normalizedB: str = text_normalizer(sentenceB)

    # step 1 & 2 : POS Tag & tokenize
    taggedA: list[tuple[str, str]] = _tagger.tag(normalizedA)
    taggedB: list[tuple[str, str]] = _tagger.tag(normalizedB)

    # step 3: stopword
    filteredA = stopword.filter_from_pairs(taggedA)
    filteredB = stopword.filter_from_pairs(taggedB)

    # step 4: stemming
    stemmedA = stemmer.stem_pairs(filteredA)
    stemmedB = stemmer.stem_pairs(filteredB)

    # step 5: build vector
    # allow duplicates IF ONLY there are differences in POS Tag
    vector = set(stemmedA + stemmedB)

    # step 6: weights
    weightsA = weighting(stemmedA, vector)
    weightsB = weighting(stemmedB, vector)

    # step 7: cosine
    return cosine(weightsA, weightsB)


def calculate_verbose(sentenceA: str, sentenceB: str) -> dict:
    normalizedA: str = text_normalizer(sentenceA)
    normalizedB: str = text_normalizer(sentenceB)

    taggedA: list[tuple[str, str]] = _tagger.tag(normalizedA)
    taggedB: list[tuple[str, str]] = _tagger.tag(normalizedB)

    filteredA = stopword.filter_from_pairs(taggedA)
    filteredB = stopword.filter_from_pairs(taggedB)

    stemmedA = stemmer.stem_pairs(filteredA)
    stemmedB = stemmer.stem_pairs(filteredB)

    # allow duplicates IF ONLY there are differences in POS Tag
    vector = set(stemmedA + stemmedB)

    vweightsA = verbose_weighting(stemmedA, vector)
    vweightsB = verbose_weighting(stemmedB, vector)

    weightsA = list(map(lambda l: max(l), vweightsA))
    weightsB = list(map(lambda l: max(l), vweightsB))

    sim = cosine(weightsA, weightsB)

    result = {
        "tagged": {
            "A": taggedA,
            "B": taggedB,
        },
        "filtered": {
            "A": filteredA,
            "B": filteredB,
        },
        "stemmed": {
            "A": stemmedA,
            "B": stemmedB,
        },
        "verbose_weight": {
            "A": vweightsA,
            "B": vweightsB,
        },
        "weight": {
            "A": weightsA,
            "B": weightsB,
        },
        "vector": vector,
        "sim": sim,
    }

    return result


def verbose_weighting(
    words: list[tuple[str, str]], vector: set[tuple[str, str]]
) -> list[float]:
    weights = []
    for v, vtag in vector:
        current = []
        for w, wtag in words:
            if is_comparable(vtag, wtag):
                weight = 1 if v == w else wordnet(v, w)
            else:
                weight = 0
            current.append(weight)
        weights.append(current)
    return weights


def weighting(
    words: list[tuple[str, str]], vector: set[tuple[str, str]]
) -> list[float]:
    weights = []
    for v, vtag in vector:
        max_weight = 0
        for w, wtag in words:
            if is_comparable(vtag, wtag):
                weight = 1 if v == w else wordnet(v, w)
                if weight > max_weight:
                    max_weight = weight

            if abs(1 - max_weight) <= 0.0001:
                break
        weights.append(max_weight)

    return weights


def wordnet(word1: str, word2: str) -> float:
    synsets1 = _wordnet.synsets(word1)
    synsets2 = _wordnet.synsets(word2)

    if len(synsets1) == 0 or len(synsets2) == 0:
        return 0

    for w1 in synsets1:
        for w2 in synsets2:
            try:
                return wup(w1, w2, True)
            except wn.Error as e:
                pass
    return 0


def cosine(vecA: list, vecB: list) -> float:
    diff = len(vecA) - len(vecB)
    if diff < 0:
        vecA = vecA.copy() + [0] * -diff

    elif diff > 0:
        vecB = vecB.copy() + [0] * diff

    num = 0
    sva = 0
    svb = 0

    for a, b in zip(vecA, vecB):
        num += a * b
        sva += a**2
        svb += b**2

    denum = sva**0.5 * svb**0.5
    if denum == 0:
        return 0

    return num / denum


def is_comparable(pos1: str, pos2: str) -> bool:
    if pos1 == pos2:
        return True

    num = {"CD", "OD"}
    if pos1 in num and pos2 in num:
        return True

    noun = {"NN", "NNP", "NND"}
    if pos1 in noun and pos2 in noun:
        return True

    # allow comparison between verb, adverb, and adjective
    # tags = {'VB', 'RB', 'JJ',}
    # if pos1 in tags and pos2 in tags:
    #    return True

    return pos1[0] == pos2[0]
