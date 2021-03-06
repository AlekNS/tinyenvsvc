# -*- coding: utf-8 -*-
import jwt


class JwtToken:
    '''
    Simple JWT token provider.
    '''

    def __init__(self, secret, alg='HS256'):
        self.secret = secret
        self.alg = alg

    async def sign(self, values: dict) -> str:
        '''
        Sign dictionary.

        :return: JWT as string
        '''
        return jwt.encode(values, self.secret, algorithm=self.alg)

    async def decode(self, token: str) -> dict:
        '''
        Decode token.

        :return: Decoded values or None for invalid token
        '''
        try:
            values = jwt.decode(token, self.secret, algorithms=self.alg)
            return values
        except:
            return None
