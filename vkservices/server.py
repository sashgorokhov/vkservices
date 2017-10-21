import asyncio
import aiohttp.web
import logging

import os
import yaml

from vkservices import routes, events


def create_app(loop):
    return aiohttp.web.Application(loop=loop)


def setup_logging(app, level='DEBUG'):
    logger = logging.getLogger('vkservices')
    logger.setLevel(getattr(logging, level.upper() or 'DEBUG'))
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s:%(funcName)s] %(message)s'))
    logger.addHandler(handler)


def read_config(path=None):
    path = path or os.environ.get('VKSERVICES_CONFIG', 'config.yaml')

    with open(path, 'r') as f:
        return yaml.load(f)


def run_server(loop=None, config=None, host='0.0.0.0', port=8080, endpoint='/'):
    loop = loop or asyncio.get_event_loop()

    app = create_app(loop)
    setup_logging(app)

    routes.setup_routes(app, endpoint=endpoint)

    app['events_manager'] = events.EventManager()
    app['config'] = read_config(path=config)

    app.logger.info('Loaded config: %s', app['config'])

    return aiohttp.web.run_app(app, host=host, port=port)
