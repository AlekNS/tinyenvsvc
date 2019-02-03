# -*- coding: utf-8 -*-
from aiohttp import ClientSession
from expiringdict import ExpiringDict


class AuthenticationService:
    '''
    Authentication Service
    '''
    _token_cache = ExpiringDict(2048, 60 * 5)

    def __init__(self, auth_url: str):
        self._auth_url = auth_url
        self._timeout = 5

    async def validate_token(self, token: str) -> dict:
        if token is None or len(token) < 16 or len(token) > 512:
            return None

        cached_token = self._token_cache.get(token)
        if not cached_token is None:
            return cached_token

        async with ClientSession() as session:
            async with session.post(self._auth_url,
                json={'accessToken': token},
                timeout=self._timeout) as response:
                response = await response.json()
                if 'decodedToken' in response:
                    self._token_cache[token] = response['decodedToken']
                    return response['decodedToken']

        return None
