import re


def summarize(text: str, num_sentences: int = 2) -> str:
    """Naive summary by returning the first num_sentences sentences."""
    sentences = re.split(r'(?:\.|\!|\?)\s+', text.strip())
    selected = sentences[:num_sentences]
    return ' '.join(selected).strip()
