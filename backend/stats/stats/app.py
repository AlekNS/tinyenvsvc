# -*- coding: utf-8 -*-
from sanic import Sanic
from dotenv import load_dotenv
from .errors import CustomErrorHandler


load_dotenv()

app = Sanic('auth', load_env='STATS_')
app.error_handler = CustomErrorHandler()
