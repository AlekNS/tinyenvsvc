# -*- coding: utf-8 -*-
'''
Registry like service locator
'''
from sanic import Sanic
from . import app
from .auth import AuthenticationService
from .password import PasswordHasher
from .repositories import UserRepository
from .token import JwtToken


class Registry:
    '''
    Like a service locator.
    '''

    @classmethod
    def jwt_token(cls) -> JwtToken:
        return JwtToken(app.config.get('JWT_SECRET', ''))

    @classmethod
    def authentication_service(cls) -> AuthenticationService:
        return AuthenticationService(cls.user_repository(),
                                    cls.jwt_token(),
                                    cls.password_hasher(),
                                    app.config.get('TOKEN_EXPIRATION_HOURS', 8))

    @classmethod
    def password_hasher(cls) -> PasswordHasher:
        return PasswordHasher()

    @classmethod
    def user_repository(cls) -> UserRepository:
        return UserRepository()
