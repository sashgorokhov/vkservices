import asyncio
import argparse
import os

from vkservices import server


def filetype(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError('%s not found' % path)
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError('%s is not a file' % path)
    return path


def main():
    parser = argparse.ArgumentParser('vkservices')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default='8080')
    parser.add_argument('--config', type=filetype, default=None)
    parser.add_argument('--endpoint',  default='/')

    args = vars(parser.parse_args())

    loop = asyncio.get_event_loop()

    return server.run_server(loop, **args)


if __name__ == '__main__':
    main()
