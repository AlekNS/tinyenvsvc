# -*- coding: utf-8 -*-
from . import app
from asyncpg import create_pool


class DataBase:
    __pool = None

    @staticmethod
    def _get_config():
        return {
            'database': app.config.get('DB_DATABASE', 'postgres'),
            'user': app.config.get('DB_USER', 'postgres'),
            'password': app.config.get('DB_PASSWORD', 'postgres'),
            'host': app.config.get('DB_HOST', 'localhost'),
            'port': app.config.get('DB_PORT', '5432')
        }

    @staticmethod
    async def pool():
        if DataBase.__pool is None:
            DataBase.__pool = await create_pool(**DataBase._get_config())

        return DataBase.__pool
