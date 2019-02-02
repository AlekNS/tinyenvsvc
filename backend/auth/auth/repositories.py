# -*- coding: utf-8 -*-
from .models import User


class UserRepository:
    '''
    User repository.
    '''

    async def get_by_email(self, email: str) -> User:
        '''
        Get user by email.
        '''
        return await User.query.where(User.email == email).gino.first()

    async def save(self, user: User) -> User:
        '''
        Save user.
        '''
        if user.id is None:
            return await User.create(email=user.email, password=user.password)
        return await User.update(email=user.email, password=user.password)
