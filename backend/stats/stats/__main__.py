# -*- coding: utf-8 -*-
from sanic.log import logger
from argparse import ArgumentParser
from . import app
from . commands import MeasurementsFileLoaderCommand

if __name__ == '__main__':
    parser = ArgumentParser(prog='statistics')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_serve = subparsers.add_parser('serve', help='serve')
    parser_serve.add_argument('--host', dest='host', default='0.0.0.0')
    parser_serve.add_argument('--port', dest='port', type=int, default=8080)
    parser_serve.add_argument('--workers', dest='workers', type=int, default=2)

    parser_upload = subparsers.add_parser('upload', help='upload')
    parser_upload.add_argument('--file', type=str, dest='file', required=True)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        if 'upload' in args.command:
            MeasurementsFileLoaderCommand(
                args.file, MeasurementsFileLoaderCommand.CSV_TYPE).run()
        elif 'serve' in args.command:
            app.run(
                host=args.host,
                port=args.port,
                workers=args.workers,
            )
