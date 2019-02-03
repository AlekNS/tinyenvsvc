# -*- coding: utf-8 -*-
import asyncio
from sanic.log import logger
from csv import reader as csvreader
from .db import DataBase
from .uploads.loader import MeasurementsCsvLoader


class AsyncCommand:
    async def _invoke(self):
        pass

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._invoke())


class MeasurementsFileLoaderCommand(AsyncCommand):
    CSV_TYPE = 'csv'

    def __init__(self, file_path, file_type):
        super().__init__()
        self._file_path = file_path
        self._file_type = file_type
        if file_type != 'csv':
            raise Exception('File type isnt supported yet')
        self._batch_size = 1000

    async def _invoke(self):
        logger.info('Upload measurements from CSV file')
        try:

            with open(self._file_path, newline='') as csvfile:
                reader = csvreader(csvfile)

                loader = MeasurementsCsvLoader(await DataBase.pool())

                await loader.run(
                    reader,
                    self._batch_size,
                    lambda rows, _: logger.info('Rows processed: {}'.format(rows)))

            logger.info('Complete!')

        except Exception as e:
            logger.error(e)
