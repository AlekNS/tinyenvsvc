from datetime import datetime
from collections import defaultdict
from ..consts import MEASUREMENTS_TABLE, STATIONS_TABLE, VARIABLES_TABLE


supported_methods = frozenset(('sum', 'avg', 'max', 'min', 'count'))


def get_method(method, support_all=True):
    if method in supported_methods:
        return [method]
    if support_all and method == 'all':
        return list(supported_methods)
    raise Exception('Unknown method')


def sql_method(method, support_all=True):
    return ', '.join(map(lambda m: '{}(real_value)'.format(m), get_method(method)))


def transform_named_to_dict(rows, exclude=()):
    return map(lambda r: {k: v for k, v in r.items() if not k in exclude}, rows)


class ValueRange:
    def __init__(self, start, end):
        self._start = float(start)
        self._end = float(end)

        if self._start > self._end:
            raise Exception('invalid value range')

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end


class Paging:
    def __init__(self, offset=0, limit=1000):
        self._offset = int(offset)
        self._limit = int(limit)

        if self._offset < 0:
            raise Exception('from is negative')

        if self._limit < 1:
            raise Exception('limit is too small')

        if self._limit > 10000:
            raise Exception('limit is too large')

    @property
    def offset(self):
        return self._offset

    @property
    def limit(self):
        return self._limit


class TimeRange:
    fmt = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, from_at, until):
        self._from_at = datetime.strptime(from_at, self.fmt)
        self._until = datetime.strptime(until, self.fmt)

        if self._from_at >= self._until:
            raise Exception('invalid time range boundaries')

    @property
    def from_at(self):
        return self._from_at

    @property
    def until(self):
        return self._until


class SummaryVariable:
    def __init__(self, db):
        self._db = db

    def set_parameters(self, varname: str, method: str = 'all'):
        self._varname = varname
        self._method = method

    async def query(self, time_range: TimeRange, paging: Paging):
        async with (await self._db.pool()).acquire() as connection:
            async with connection.transaction():
                rows = await connection.fetch('''
                SELECT
                    s.name,
                    q.*
                FROM (
                    SELECT
                        station_id,
                        {method}
                    FROM
                        "{measurements}" m
                    WHERE
                        measured_at between $1 AND $2 AND
                        parameter_id = (
                            SELECT id FROM "{parameters}" WHERE name = $3
                        )
                    GROUP BY
                        station_id,
                        parameter_id
                ) q
                INNER JOIN "{stations}" s ON
                    q.station_id = s.id
                LIMIT $4 OFFSET $5'''.format_map({
                    'method': sql_method(self._method),
                    'measurements': MEASUREMENTS_TABLE,
                    'parameters': VARIABLES_TABLE,
                    'stations': STATIONS_TABLE,
                }), time_range.from_at, time_range.until, self._varname, paging.limit, paging.offset)

            return list(transform_named_to_dict(rows, ['station_id']))


class ThresholdOvercomeVariable:
    def __init__(self, db):
        self._db = db

    def set_parameters(self, varname: str):
        self._varname = varname

    async def query(self, value_range: ValueRange, time_range: TimeRange, paging: Paging):
        async with (await self._db.pool()).acquire() as connection:
            async with connection.transaction():
                rows = await connection.fetch('''
                SELECT
                    s.name,
                    q.*
                FROM (
                    SELECT
                        station_id,
                        count(station_id),
                        date_trunc_epoch(measured_at, '1 days') as date
                    FROM
                        "{measurements}"
                    WHERE
                        measured_at between $1 AND $2 AND
                        parameter_id = (
                            SELECT id FROM "{parameters}" WHERE name = $3
                        ) AND
                        NOT real_value between $4 AND $5
                    GROUP BY
                        date, station_id
                ) q
                INNER JOIN "{stations}" s ON
                    q.station_id = s.id
                LIMIT $6 OFFSET $7'''.format_map({
                    'measurements': MEASUREMENTS_TABLE,
                    'parameters': VARIABLES_TABLE,
                    'stations': STATIONS_TABLE,
                }),
                    time_range.from_at,
                    time_range.until,
                    self._varname,
                    value_range.start,
                    value_range.end,
                    paging.limit,
                    paging.offset)

            stations = defaultdict(lambda: list())
            for row in rows:
                stations[row['name']].append({
                    'count': row['count'],
                    'date': row['date'].isoformat(),
                })

            return [{k: v} for k, v in stations.items()]


class StationTimeSeries:
    max_interval = 24 * 60 * 31

    def __init__(self, db):
        self._db = db

    def set_parameters(self, station: str, varname: str, method: str = 'avg', minutes_interval: str = '5'):
        self._station = station
        self._varname = varname
        self._method = method
        self._minutes = int(minutes_interval)
        if self._minutes < 1:
            raise Exception('aggregation interval is too small')
        if self._minutes > self.max_interval:
            raise Exception('aggregation interval is too large')

    async def query(self, time_range: TimeRange, paging: Paging):
        async with (await self._db.pool()).acquire() as connection:
            async with connection.transaction():
                rows = await connection.fetch('''
                SELECT
                    q.dt as measured_at,
                    q.*
                FROM (
                    SELECT
                        date_trunc_epoch(measured_at, '{interval} minutes'::interval) as dt,
                        {method}
                    FROM
                        "{measurements}"
                    WHERE
                        measured_at between $1 AND $2 AND
                        parameter_id = (
                            SELECT id FROM "{parameters}" WHERE name = $3
                        ) AND
                        station_id = (
                            SELECT id FROM "{stations}" WHERE name = $4
                        )
                    GROUP BY
                        dt
                ) q
                ORDER BY
                    q.dt
                LIMIT $5 OFFSET $6'''.format_map({
                    'interval': self._minutes,
                    'method': sql_method(self._method),
                    'measurements': MEASUREMENTS_TABLE,
                    'parameters': VARIABLES_TABLE,
                    'stations': STATIONS_TABLE,
                }),
                    time_range.from_at,
                    time_range.until,
                    self._varname,
                    self._station,
                    paging.limit,
                    paging.offset)

                rows = list(map(lambda l: dict(l), rows))
                for row in rows:
                    row['measured_at'] = row['measured_at'].isoformat()

                return transform_named_to_dict(rows, ('dt',))
