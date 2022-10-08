import pickle
from pathlib import Path

_LOCAL_PATH = (Path(__file__).parent / "nltk_data").absolute()
import nltk.data

nltk.data.path.insert(0, _LOCAL_PATH)
from nltk.tokenize import word_tokenize


class Tagger:
    def __init__(self):
        path = Path(__file__).resolve().parent
        path = path / "indonesian_classifier_pos_tag.pickle"
        with open(path.absolute(), "rb") as file:
            self._tagger = pickle.load(file)

    def tag(self, sentence: str) -> list[tuple]:
        tokens = word_tokenize(sentence)
        return self._tagger.tag(tokens)
