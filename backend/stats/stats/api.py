# -*- coding: utf-8 -*-
'''
HTTP API.
'''
from sanic.log import logger
from sanic.response import json
from . import app
from .uploads import api as uploadsapi
from .gathering import api as gatheringapi
from .dicts import api as dictsapi


@app.route('/', methods=['GET'])
async def index_handle(request):
    return json({'title': 'Stats Service'})


app.blueprint(uploadsapi.module, url_prefix='/api/uploads')
app.blueprint(gatheringapi.module, url_prefix='/api/statistics')
app.blueprint(dictsapi.module, url_prefix='/api/dicts')
