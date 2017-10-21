import logging

import aiohttp
import bs4

logger = logging.getLogger(__name__)


def _bs_from_response(html):
    """
    Returns BeautifulSoup from given str with html inside.
    :param str html:
    :rtype: bs4.BeautifulSoup
    """
    return bs4.BeautifulSoup(html, "html.parser")


def build_login_url(client_id, scope):
    return "http://oauth.vk.com/oauth/authorize?" + \
           "redirect_uri=http://oauth.vk.com/blank.html&response_type=token&" + \
           "client_id=%s&scope=%s&display=wap" % (client_id, ",".join(scope))


class Authcheck(Exception):
    pass


async def auth(email, password, client_id, scope):
    login_url = build_login_url(client_id, scope)

    async with aiohttp.ClientSession() as session:

        # Get user login page
        async with session.get(login_url) as response:
            body = await response.text()

        if response.url.path == '/blank.html':
            return response.url.query
        else:
            bs = _bs_from_response(body)
            form_url = bs.find('form').get('action')
            data = {i.attrs['name']: i.attrs.get('value') for i in bs.find_all('input') if 'name' in i.attrs}
            data['email'] = email
            data['pass'] = password

            # Login user, get access granting page
            async with session.post(form_url, data=data) as response:
                body = await response.text()

        if response.url.path == '/blank.html':
            return response.url.query
        elif response.url.query.get('act', '') == 'authcheck':
            raise Authcheck()
        else:
            bs = _bs_from_response(body)
            form_url = bs.find('form').get('action')

            # Grant access to app
            async with session.post(form_url) as response:
                return response.url.query
