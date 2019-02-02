# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from . import app

if __name__ == '__main__':
    parser = ArgumentParser(prog='auth')
    parser.add_argument('--host', dest='host', type=str, default='0.0.0.0')
    parser.add_argument('--port', dest='port', type=int, default=8080)
    parser.add_argument('--workers', dest='workers', type=int, default=2)
    args = parser.parse_args()

    app.run(
        host=args.host,
        port=args.port,
        workers=args.workers,
    )
