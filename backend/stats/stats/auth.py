# -*- coding: utf-8 -*-


class AuthenticationService:
    '''
    Authentication Service
    '''

    async def validate_token(self, token: str) -> dict:
        # return AuthenticationToken(token)
        return {}


# def auth(handler, auth_svc):
#     @wraps
#     async def func(request, *args, **kwargs):
#         auth_svc.validate_token(request.token())
#         return await handler(request, *args, **kwargs)
#     return func
