# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from . import app

if __name__ == '__main__':
    parser = ArgumentParser(prog='auth')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_serve = subparsers.add_parser('serve', help='serve')
    parser_serve.add_argument('--host', dest='host', default='0.0.0.0')
    parser_serve.add_argument('--port', dest='port', type=int, default=8080)
    parser_serve.add_argument('--workers', dest='workers', type=int, default=2)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()

    if args.command == 'serve':
        app.run(
            host=args.host,
            port=args.port,
            workers=args.workers,
        )
