import json
from pathlib import Path
from typing import List, Dict

TOPICS_FILE = Path('data/topics.json')

class TopicManager:
    def __init__(self, path: Path = TOPICS_FILE):
        self.path = path
        self.topics = self._load()

    def _load(self) -> List[Dict[str, str]]:
        if self.path.exists():
            with self.path.open('r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(self.topics, f, indent=2)

    def list_topics(self) -> List[Dict[str, str]]:
        return self.topics

    def add_topic(self, name: str, query: str) -> None:
        self.topics.append({'name': name, 'query': query})
        self._save()

    def remove_topic(self, name: str) -> None:
        self.topics = [t for t in self.topics if t['name'] != name]
        self._save()
