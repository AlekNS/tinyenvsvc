# -*- coding: utf-8 -*-
'''
HTTP API.
'''
from sanic.response import json
from .module import module
from .registry import Registry
from .transformers import transform_dictionary_response


def default_dict_response(data):
    return json({
        'statusCode': 200,
        'data': list(transform_dictionary_response(data)),
    })


@module.route('/variables', methods=['GET'])
async def get_variables(request):
    svc = Registry.variables_dict()
    return default_dict_response(await svc.query())


@module.route('/stations', methods=['GET'])
async def get_threshold_overcome_variables(request):
    svc = Registry.stations_dict()
    return default_dict_response(await svc.query())
