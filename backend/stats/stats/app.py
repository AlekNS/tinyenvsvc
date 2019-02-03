# -*- coding: utf-8 -*-
from sanic import Sanic
from dotenv import load_dotenv
from sanic_cors import CORS
from .errors import CustomErrorHandler


load_dotenv()

app = Sanic('auth', load_env='STATS_')
cors = CORS(app, resources=r'/api/*', automatic_options=True)
app.error_handler = CustomErrorHandler()
