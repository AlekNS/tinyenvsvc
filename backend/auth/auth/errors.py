# -*- coding: utf-8 -*-
from sanic.exceptions import SanicException
from sanic.response import json
from sanic.log import logger
from sanic.handlers import ErrorHandler


class UserExistsError(SanicException):
    status_code = 400


class UserPasswordError(SanicException):
    status_code = 404


# @TODO: Should be more accurate implementation
class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception):
        if issubclass(type(exception), SanicException):
            status = getattr(exception, 'status_code', 500)
            message = '{}'.format(exception)

            if issubclass(type(exception), UserPasswordError):
                message = 'Not found'

            return json({
                'statusCode': status,
                'message': message
            },
                status=status,
                headers=getattr(exception, 'headers', dict()),
            )

        return super().default(request, exception)
