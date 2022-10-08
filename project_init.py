import wn
import nltk
import nltk.data
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
LOCAL_WN_DIRECTORY = str((CURRENT_DIR / "wn_data").absolute())
LOCAL_NLTK_DIRECTORY = str((CURRENT_DIR / "tagger" / "nltk_data").absolute())

wn.config.data_directory = LOCAL_WN_DIRECTORY

nltk.download("punkt", LOCAL_NLTK_DIRECTORY)

# wn.download("oewn:2021")
# wn.download("omw-id:1.4")
