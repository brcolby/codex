import json
from pathlib import Path
from typing import List, Dict

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
