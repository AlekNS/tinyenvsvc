# -*- coding: utf-8 -*-
from . import app
from gino.ext.sanic import Gino


db = Gino()
db.init_app(app)
