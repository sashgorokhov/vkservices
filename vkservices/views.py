import logging

logger = logging.getLogger(__name__)


async def process(request):
    return await request.app['events_manager'].handle(request)
