# -*- coding: utf-8 -*-
from sanic.exceptions import abort
from .registry import Registry


def auth_middleware(url_prefix = '/'):
    async def middleware(request):
        if len(request.path) > 0 and request.path.find(url_prefix) != 0:
            return None

        svc = Registry.authentication_service()
        result = await svc.validate_token(request.token)

        if result is None:
            abort(401)

        request['auth'] = result

    return middleware