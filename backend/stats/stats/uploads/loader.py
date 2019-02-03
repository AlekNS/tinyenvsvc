# -*- coding: utf-8 -*-
from datetime import datetime
from ..helpers import chunks
from ..consts import MEASUREMENTS_TABLE, STATIONS_TABLE, VARIABLES_TABLE


class MeasurementsLoader:
    '''
    Measurements loader.
    '''

    MEASURED_COLUMN_NAME = 'timeinstant'
    STATION_COLUMN_NAME = 'id_entity'
    not_variables_columns = frozenset((
        'id', MEASURED_COLUMN_NAME, STATION_COLUMN_NAME, 'created_at', 'updated_at'))
    stations_batch_size = 20

    def __init__(self, pool):
        self._pool = pool
        self._datetime_format = '%Y-%m-%d %H:%M:%S.%f'
        self._variables_cache = {}
        self._stations_cache = {}

    def _fix_measured_at_milliseconds(self, measured_at_str):
        if measured_at_str.find('.') < 0:
            measured_at_str += '.000'
        return measured_at_str

    async def prepare_variables(self, columns: list):
        # keys of "columns" should be in lowercase.
        cols = list(filter(
            lambda i: not i in self.not_variables_columns, columns.keys()))

        if len(cols) == 0:
            raise Exception('no measurements')

        async with self._pool.acquire() as connection:
            async with connection.transaction():
                await self._prefill_dictionaries(connection, VARIABLES_TABLE, self._variables_cache, cols)

    async def _prefill_dictionaries(self, connection, tbl_name, cache, values):
        values = list(filter(lambda i: not i in cache, values))
        if len(values) == 0:
            return

        await connection.execute('''
        INSERT INTO "{}" (name) VALUES {} ON CONFLICT (name) DO NOTHING
        '''.format(tbl_name, ','.join(map(lambda x: '(${})'.format(x), range(1, len(values) + 1)))), *values)

        result = await connection.fetch(
            'SELECT id, name FROM "{}" WHERE name = any($1::text[])'.format(tbl_name), values)

        for param in result:
            cache[param['name']] = param['id']

    async def load_batch(self, columns: list, rows: list):
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                station_inx = columns[self.STATION_COLUMN_NAME]
                stations_dict = {r[station_inx]: True for r in rows}

                for stations in chunks(stations_dict.keys(), self.stations_batch_size):
                    await self._prefill_dictionaries(connection, STATIONS_TABLE, self._stations_cache, list(stations))

                records = []

                for row in rows:
                    measured_at_str = self._fix_measured_at_milliseconds(
                        row[columns[self.MEASURED_COLUMN_NAME]])

                    measured_at = datetime.strptime(
                        measured_at_str, self._datetime_format)

                    for param_name, param_id in self._variables_cache.items():
                        records += ((
                            self._stations_cache[row[columns[self.STATION_COLUMN_NAME]]],
                            param_id,
                            measured_at,
                            float(row[columns[param_name]])),)

                await connection.copy_records_to_table(
                    MEASUREMENTS_TABLE,
                    columns=['station_id', 'parameter_id',
                             'measured_at', 'real_value'],
                    records=records)

    async def done(self):
        async with self._pool.acquire() as connection:
            await connection.execute('ANALYZE "{}"'.format(MEASUREMENTS_TABLE))

def noop(r, c):
    pass

class MeasurementsCsvLoader:
    def __init__(self, pool):
        self._loader = MeasurementsLoader(pool)

    async def run(self, csvreader, batch_size, chunk_process_callback: callable = noop):
        header_row = next(csvreader)
        columns = {
            header_row[inx].lower(): inx for inx in range(len(header_row))
        }

        await self._loader.prepare_variables(columns)

        rows = 0
        for chunk in chunks(csvreader, batch_size):
            chunk_items = list(chunk)
            await self._loader.load_batch(columns, chunk_items)
            rows += len(chunk_items)

            chunk_process_callback(rows, chunk)

        await self._loader.done()

        return rows
