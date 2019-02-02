# -*- coding: utf-8 -*-
'''
HTTP API.
'''
from sanic import Sanic
from sanic.log import logger
from sanic.exceptions import abort
from sanic.response import json
from functools import wraps
from jsonschema import validate as jsonvalidate
from . import app
from .auth import AuthenticateUser, AuthenticationToken
from .registry import Registry


register_and_login_validation_schema = {
    'type': 'object',
    'properties': {
        'email': {  # basic, sure it's not RFC
            'type': 'string',
            'pattern': '^[^@]+@[^@]+\\.[^@]+$'
        },
        'password': {
            'type': 'string',
            'minLength': 6,
            'maxLength': 64
        },
    },
    'required': ['email', 'password'],
}

validate_validation_schema = {
    'type': 'object',
    'properties': {
        'accessToken': {
            'type': 'string',
            'minLength': 48,
            'maxLength': 1024
        },
    },
    'required': ['accessToken'],
}


@app.route('/', methods=['GET'])
async def index_handle(request):
    return json({'title': 'Auth Service'})


@app.route('/api/auth/register', methods=['POST'])
async def register_handle(request):
    body = request.json
    jsonvalidate(body, register_and_login_validation_schema)

    auth_user = AuthenticateUser(body['email'].lower(), body['password'])

    svc = Registry.authentication_service()
    auth_token = await svc.register(auth_user)

    return json({
        'statusCode': 200,
        'accessToken': auth_token.token,
    })


@app.route('/api/auth/login', methods=['POST'])
async def login_handle(request):
    body = request.json
    jsonvalidate(body, register_and_login_validation_schema)

    auth_user = AuthenticateUser(body['email'].lower(), body['password'])

    svc = Registry.authentication_service()
    auth_token = await svc.authenticate(auth_user)

    return json({
        'statusCode': 200,
        'accessToken': auth_token.token,
    })


@app.route('/api/auth/validate', methods=['POST'])
async def validate_handle(request):
    body = request.json
    jsonvalidate(body, validate_validation_schema)

    svc = Registry.authentication_service()
    decoded_token = await svc.validate_token(
        AuthenticationToken(body['accessToken']))
    if not decoded_token:
        abort(401)

    return json({
        'statusCode': 200,
        'decodedToken': decoded_token,
    })
