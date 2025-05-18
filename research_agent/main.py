import argparse
from pathlib import Path
import shutil

from .topics import TopicManager
from .agent import run_once
from .search import query_arxiv
from .summarizer import summarize_pdf
from .storage import download_pdf


def browse_cli(max_results: int = 5) -> None:
    query = input("Enter arXiv search query: ")
    papers = query_arxiv(query, max_results=max_results)
    if not papers:
        print("No papers found.")
        return
    while True:
        print("\nSelect a paper to view:\n")
        for i, p in enumerate(papers, 1):
            print(f"{i}. {p['title']}")
        choice = input("Enter number or 'q' to quit: ")
        if choice.lower() == 'q':
            break
        try:
            idx = int(choice) - 1
            paper = papers[idx]
        except (ValueError, IndexError):
            print("Invalid selection")
            continue

        tmp_path = download_pdf(paper['pdf_url'], Path('tmp'))
        summary = summarize_pdf(tmp_path)
        print(f"\nSummary for {paper['title']}\n{'-'*40}\n{summary}\n")
        download = input("Download this paper? [y/N]: ").lower().startswith('y')
        if download:
            final = Path('papers') / tmp_path.name
            final.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(tmp_path, final)
            print(f"Saved to {final}")
        else:
            tmp_path.unlink()


def main():
    parser = argparse.ArgumentParser(description='Research tracking agent')
    sub = parser.add_subparsers(dest='cmd')

    add_p = sub.add_parser('add', help='add a topic')
    add_p.add_argument('name')
    add_p.add_argument('query')

    remove_p = sub.add_parser('remove', help='remove a topic')
    remove_p.add_argument('name')

    sub.add_parser('list', help='list topics')
    sub.add_parser('run', help='run once')
    sub.add_parser('browse', help='interactive browser')

    args = parser.parse_args()
    tm = TopicManager()

    if args.cmd == 'add':
        tm.add_topic(args.name, args.query)
    elif args.cmd == 'remove':
        tm.remove_topic(args.name)
    elif args.cmd == 'list':
        for t in tm.list_topics():
            print(f"{t['name']}: {t['query']}")
    elif args.cmd == 'run':
        run_once()
    elif args.cmd == 'browse':
        browse_cli()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
