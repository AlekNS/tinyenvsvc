# -*- coding: utf-8 -*-
from ..consts import STATIONS_TABLE, VARIABLES_TABLE


class DictionaryTable:
    def __init__(self, db, table_name, columns):
        self._db = db
        self._table = table_name
        self._columns = columns

    async def query(self) -> list:
        async with (await self._db.pool()).acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch('''
                SELECT
                    {columns}
                FROM
                    "{table}"
                ORDER BY
                    name'''.format_map({
                        'columns': ','.join(self._columns),
                        'table': self._table,
                    }))

                return list(result)


class VariablesDict(DictionaryTable):
    def __init__(self, db):
        super().__init__(db, VARIABLES_TABLE, ['name', 'description'])


class StationsDict(DictionaryTable):
    def __init__(self, db):
        super().__init__(db, STATIONS_TABLE, ['name'])
