import xml.etree.ElementTree as ET
from typing import List, Dict
from urllib.parse import urlencode
from urllib.request import urlopen

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
        paper = {
            'id': entry.find('a:id', ns).text,
            'title': entry.find('a:title', ns).text.strip(),
            'summary': entry.find('a:summary', ns).text.strip(),
            'updated': entry.find('a:updated', ns).text,
            'published': entry.find('a:published', ns).text,
            'authors': [author.find('a:name', ns).text for author in entry.findall('a:author', ns)],
            'link': next((link_elem.get('href') for link_elem in entry.findall('a:link', ns) if link_elem.get('rel') == 'alternate'), None),
        }
        papers.append(paper)
    return papers
