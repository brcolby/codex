import argparse
from .topics import TopicManager
from .agent import run_once


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
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
