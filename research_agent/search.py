import os
import xml.etree.ElementTree as ET
from typing import List, Dict
from urllib.parse import urlencode
from urllib.request import urlopen

from .mistral_api import chat_completion

ARXIV_API = 'https://export.arxiv.org/api/query'


def query_arxiv(search_query: str, max_results: int = 5) -> List[Dict[str, str]]:
    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'lastUpdatedDate',
    }
    url = f"{ARXIV_API}?{urlencode(params)}"
    with urlopen(url) as response:
        data = response.read()
    root = ET.fromstring(data)
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    papers = []
    for entry in root.findall('a:entry', ns):
        paper_id_url = entry.find('a:id', ns).text
        paper_id = paper_id_url.rsplit('/', 1)[-1]
        pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
        paper = {
            'id': paper_id_url,
            'title': entry.find('a:title', ns).text.strip(),
            'summary': entry.find('a:summary', ns).text.strip(),
            'updated': entry.find('a:updated', ns).text,
            'published': entry.find('a:published', ns).text,
            'authors': [author.find('a:name', ns).text for author in entry.findall('a:author', ns)],
            'link': next((link_elem.get('href') for link_elem in entry.findall('a:link', ns) if link_elem.get('rel') == 'alternate'), None),
            'pdf_url': pdf_url,
        }
        papers.append(paper)
    return papers


def _get_related_terms(query: str) -> List[str]:
    """Use the Mistral API to generate search terms related to *query*."""
    prompt = (
        "List up to 5 short search keywords related to the following research "
        f"topic, separated by commas: {query}"
    )
    text = chat_completion([
        {"role": "user", "content": prompt}
    ], max_tokens=50, temperature=0.3)
    terms = [t.strip() for t in text.split(",") if t.strip()]
    return terms


def _is_relevant(text: str, keywords: List[str]) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def search_related(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search arXiv using *query* and related terms and filter by relevance."""
    terms = [query] + _get_related_terms(query)
    keywords = terms
    results: Dict[str, Dict[str, str]] = {}
    for term in terms:
        for paper in query_arxiv(term, max_results=max_results):
            if paper["id"] in results:
                continue
            if _is_relevant(paper["summary"], keywords) or _is_relevant(
                paper["title"], keywords
            ):
                results[paper["id"]] = paper
    return list(results.values())
