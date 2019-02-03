# -*- coding: utf-8 -*-
'''
HTTP API.
'''
from sanic import Sanic
from sanic.log import logger
from sanic.exceptions import abort
from sanic.response import json
from .module import module
from .registry import Registry
from .services import TimeRange, Paging, ValueRange


@module.route('/variables/<variable>/summary', methods=['GET'])
async def get_variable_summary(request, variable):
    svc = Registry.summary_variable()
    svc.set_parameters(variable, request.args.get('method', 'all'))
    result = await svc.query(
        TimeRange(
            request.args.get('timestamp_from'), request.args.get(
                'timestamp_until')
        ),
        Paging(
            request.args.get('skip', 0), request.args.get('limit', 1000)
        )
    )

    return json({
        'statusCode': 200,
        'data': result,
    })


@module.route('/thresholds/variables/<variable>/overcomes', methods=['GET'])
async def get_threshold_overcome_variables(request, variable):
    svc = Registry.threshold_overcome_variable()
    svc.set_parameters(variable)
    result = await svc.query(
        ValueRange(
            request.args.get('threshold_low'), request.args.get(
                'threshold_high')
        ),
        TimeRange(
            request.args.get('timestamp_from'), request.args.get(
                'timestamp_until')
        ),
        Paging(
            request.args.get('skip', 0), request.args.get('limit', 1000)
        )
    )

    return json({
        'statusCode': 200,
        'data': result,
    })


@module.route('/time-series/stations/<station>/variables/<variable>', methods=['GET'])
async def measurements_upload_csv_handle(request, station, variable):
    svc = Registry.station_timeseries()
    svc.set_parameters(station, variable, request.args.get(
        'method', 'avg'), request.args.get('interval', '5'))
    result = await svc.query(
        TimeRange(
            request.args.get('timestamp_from'), request.args.get(
                'timestamp_until')
        ),
        Paging(
            request.args.get('skip', 0), request.args.get('limit', 1000)
        )
    )

    return json({
        'statusCode': 200,
        'data': result,
    })
