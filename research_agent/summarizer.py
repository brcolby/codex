import os
from pathlib import Path
from typing import Iterable

from PyPDF2 import PdfReader

from .mistral_api import chat_completion


def _extract_text(path: Path) -> str:
    reader = PdfReader(str(path))
    parts: Iterable[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text)
    return "\n".join(parts)


def summarize_pdf(pdf_path: Path) -> str:
    """Summarize a paper using the Mistral API."""
    text = _extract_text(pdf_path)
    prompt = (
        "Read the following research paper and provide a concise summary "
        "highlighting the main points, interesting work, and important results:\n\n"
        f"{text}"
    )
    return chat_completion([
        {"role": "user", "content": prompt}
    ], max_tokens=300, temperature=0.3)
