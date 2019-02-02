# -*- coding: utf-8 -*-
from bcrypt import hashpw, checkpw, gensalt


class PasswordHasher:
    '''
    Hash password.
    '''

    async def encrypt(self, password: str) -> str:
        '''
        Hash password
        '''
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    async def compare(self, password: str, hashedPassword: str) -> bool:
        '''
        Check password
        '''
        return checkpw(password.encode('utf-8'), hashedPassword.encode('utf-8'))
