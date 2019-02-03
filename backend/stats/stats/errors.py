# -*- coding: utf-8 -*-
from sanic.response import json
from sanic.log import logger
from sanic.handlers import ErrorHandler
from traceback import format_exc


# @TODO: Should be more accurate implementation
class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception):
        self.log(format_exc())
        try:
            url = repr(request.url)
        except AttributeError:
            url = "unknown"

        response_message = "Exception occurred while handling uri: %s"
        status = getattr(exception, 'status_code', 500)
        message = '{}'.format(exception)

        if status > 406:
            logger.exception(response_message, url)

        return json({
            'statusCode': status,
            'message': message
        },
            status=status,
            headers=getattr(exception, 'headers', dict()),
        )
