import wn
import nltk
import nltk.data
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
LOCAL_WN_DIRECTORY = CURRENT_DIR / "wn_data"
LOCAL_NLTK_DIRECTORY = CURRENT_DIR / "tagger" / "nltk_data"

if not LOCAL_WN_DIRECTORY.exists():
    LOCAL_WN_DIRECTORY.mkdir()

wn.config.data_directory = str(LOCAL_WN_DIRECTORY.absolute())
wn.download("oewn:2021")
wn.download("omw-id:1.4")

if not LOCAL_NLTK_DIRECTORY.exists():
    LOCAL_NLTK_DIRECTORY.mkdir()

nltk.download("punkt", str(LOCAL_NLTK_DIRECTORY.absolute()))
