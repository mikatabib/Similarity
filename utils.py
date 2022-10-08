import re


def text_normalizer(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9 -]', ' ', text, flags=re.IGNORECASE | re.MULTILINE)
    return text
