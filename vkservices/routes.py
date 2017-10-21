from aiohttp import web
from vkservices import views


def setup_routes(app: web.Application, endpoint='/'):
    app.router.add_post(endpoint, views.process)
