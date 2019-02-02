# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from .errors import UserPasswordError, UserExistsError
from .models import User
from .password import PasswordHasher
from .repositories import UserRepository
from .token import JwtToken


class AuthenticateUser:
    '''
    DTO for user
    '''

    def __init__(self, email, password):
        self.email = email
        self.password = password


class AuthenticationToken:
    '''
    DTO for token
    '''

    def __init__(self, token):
        self.token = token


class AuthenticationService:
    '''
    Authentication Service
    '''

    def __init__(self, user_repository: UserRepository,
                 jwt_token: JwtToken,
                 encryption_service: PasswordHasher,
                 expiration_hours: int):
        self._user_repository = user_repository
        self._jwt_token = jwt_token
        self._encryption_service = encryption_service
        self._exp_hours = expiration_hours  # @TODO: from config

    async def register(self, auth_user: AuthenticateUser) -> AuthenticationToken:
        '''
        Register a new user.
        '''
        user = User()
        user.email = auth_user.email
        user.password = await self._encryption_service.encrypt(auth_user.password)
        try:
            await self._user_repository.save(user)
        except:
            raise UserExistsError('user already registered')

        return await self.authenticate(auth_user)

    async def authenticate(self, auth_user: AuthenticateUser) -> AuthenticationToken:
        '''
        Authenticate a user.
        '''
        user = await self._user_repository.get_by_email(auth_user.email)
        if user is None:
            raise UserPasswordError('user not found')

        if not await self._encryption_service.compare(auth_user.password, user.password):
            raise UserPasswordError('invalid password')

        token = await self._jwt_token.sign({
            'uid': user.id,
            'exp': int((datetime.now() + timedelta(hours=self._exp_hours)).timestamp()),
        })

        return AuthenticationToken(token)

    async def validate_token(self, auth_token: AuthenticationToken) -> dict:
        '''
        Validate signature and check token expiration.

        :return: Decoded token as dict or None for invalid token.
        '''
        values = await self._jwt_token.decode(auth_token.token)

        if values is None:
            return None

        if values['exp'] < datetime.now().timestamp():
            return None

        return values
