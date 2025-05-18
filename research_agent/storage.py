import json
from pathlib import Path
from typing import List, Dict
from urllib.request import urlopen

PAPERS_DIR = Path('papers')

DATA_DIR = Path('data')


def save_papers(topic: str, papers: List[Dict[str, str]]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out_file = DATA_DIR / f'{topic.replace(" ", "_")}.json'
    if out_file.exists():
        with out_file.open('r', encoding='utf-8') as f:
            existing = json.load(f)
    else:
        existing = []
    existing.extend(papers)
    with out_file.open('w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2)


def download_pdf(url: str, dest_dir: Path = PAPERS_DIR) -> Path:
    """Download a PDF from a URL into *dest_dir* and return the file path."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = url.rsplit('/', 1)[-1]
    out_path = dest_dir / filename
    with urlopen(url) as response:
        data = response.read()
    with out_path.open('wb') as f:
        f.write(data)
    return out_path
