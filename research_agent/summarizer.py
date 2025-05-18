import os
from pathlib import Path
from typing import Iterable

import openai
from PyPDF2 import PdfReader


def _extract_text(path: Path) -> str:
    reader = PdfReader(str(path))
    parts: Iterable[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text)
    return "\n".join(parts)


def summarize_pdf(pdf_path: Path) -> str:
    """Summarize a paper using the ChatGPT API."""
    text = _extract_text(pdf_path)
    prompt = (
        "Read the following research paper and provide a concise summary "
        "highlighting the main points, interesting work, and important results:\n\n"
        f"{text}"
    )
    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3,
    )
    return response["choices"][0]["message"]["content"].strip()
