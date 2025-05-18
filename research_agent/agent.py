from datetime import datetime

from .topics import TopicManager
from .search import query_arxiv
from .summarizer import summarize
from .storage import save_papers


def run_once(max_results: int = 5) -> None:
    tm = TopicManager()
    for topic in tm.list_topics():
        name = topic['name']
        query = topic['query']
        papers = query_arxiv(query, max_results=max_results)
        for p in papers:
            p['summary_short'] = summarize(p['summary'])
            p['retrieved_at'] = datetime.utcnow().isoformat()
            p['topic'] = name
        save_papers(name, papers)

if __name__ == '__main__':
    run_once()
