import logging
from aiohttp import web, web_exceptions
import os

logger = logging.getLogger(__name__)


def get_group_config(group_id, config):
    return next(filter(lambda d: d['group_id'] == group_id, config['groups']), None)


class EventManager:
    handlers = dict()

    async def handle(self, request):
        data = await request.json()

        request_type = data.get('type', None)
        group_id = data.get('group_id', None)

        if not request_type:
            raise web_exceptions.HTTPBadRequest(text='Invalid request type %s' % request_type)

        if request_type not in self.handlers:
            raise web_exceptions.HTTPBadRequest(text='Unhandled request type %s' % request_type)

        if group_id not in request.app['config']['groups']:
            raise web_exceptions.HTTPBadRequest(text='Invalid group id %s' % group_id)

        return await self.handlers[request_type](request)

    @classmethod
    def register(cls, request_type, func):
        if request_type in cls.handlers:
            raise ValueError('%s is already registered as %s' % (request_type, func))

        cls.handlers[request_type] = func


def register(request_type=None):
    def decor(func):
        nonlocal request_type

        request_type = request_type or func.__name__
        EventManager.register(request_type, func)
        return func
    return decor


@register()
async def confirmation(request):
    data = await request.json()

    confirmation_token = request.app['config']['groups'][data['group_id']].get('confirmation_token')

    if not confirmation_token:
        logger.error('Confirmation token for group %s is not set' % data['group_id'])
        raise web_exceptions.HTTPInternalServerError(body='Confirmation token is not set')

    logger.info('Got confirmation request for group %s', data['group_id'])

    return web.Response(body=confirmation_token, status=200)


async def filter_comment(comment):
    logger.info('Got comment: %s', comment)


@register()
async def wall_reply_new(request):
    data = await request.json()

    await filter_comment(data['object'])

    return web.Response(text='ok')
