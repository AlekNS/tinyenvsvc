# -*- coding: utf-8 -*-
'''
Registry like service locator
'''
from sanic import Sanic
from . import app
from .db import DataBase
from .auth import AuthenticationService


class Registry:
    '''
    Like a service locator.
    '''
    @classmethod
    def database(cls):
        return DataBase()

    @classmethod
    def authentication_service(cls) -> AuthenticationService:
        return AuthenticationService(
            app.config.get('AUTH_VALIDATE_URL', 'http://auth:8080/api/auth/validate'))
