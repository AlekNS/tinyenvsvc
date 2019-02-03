# -*- coding: utf-8 -*-
'''
HTTP API.
'''
from sanic import Sanic
from sanic.log import logger
from sanic.exceptions import abort
from sanic.response import json
from csv import reader as csvreader
from io import TextIOWrapper, BytesIO
from ..db import DataBase
from .module import module
from .loader import MeasurementsCsvLoader


BATCH_SIZE = 1000


@module.route('/measurements/csv', methods=['POST'])
async def measurements_upload_csv_handle(request):
    if not 'csv_file' in request.files:
        return json({
            'statusCode': 400,
            'message': 'Invalid POST data, no csv_file was passed'
        })

    csv_fo = TextIOWrapper(BytesIO(request.files['csv_file'][0].body))
    reader = csvreader(csv_fo)

    loader = MeasurementsCsvLoader(await DataBase.pool())

    processed_rows = await loader.run(
        reader,
        BATCH_SIZE)

    return json({
        'statusCode': 201,
        'processedRows': processed_rows,
    })
