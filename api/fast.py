from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from pnboia_api.bd import GetData
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/v2")
def index():
    return {"greeting": "Hello world"}


@app.get("/v2/buoys")
async def data(status:str=None):

    if status == None:
        arguments = None
    else:
        arguments = {'status': status.capitalize()}

    df = GetData().get(table='buoys', arguments=arguments)

    df.deploy_date = df.deploy_date.dt.strftime("%Y-%m-%d %H:%M%S")

    df = df.fillna("-9999")

    result = df.to_dict('records')
    return JSONResponse(content=result)

@app.get("/v2/data_buoys")
async def data(start_date=None,
         end_date=None,
         buoy=None):

    arguments = {}

    if buoy == None:
        return {'Erro': 'Necessário adicionar um id de boia'}

    arguments['buoy_id']=buoy

    if start_date == None:
        start_date = (datetime.utcnow() - timedelta(days=3))
    else:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        except:
            return {'Erro': 'Formato errado de start_date (YYYY-MM-DD)'}
    if end_date == None:
        end_date = (datetime.utcnow() + timedelta(days=1))
    else:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        except:
            return {'Erro': 'Formato errado de end_date (YYYY-MM-DD)'}
    
    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))
    
    arguments['date_time>'] = start_date.strftime('%Y-%m-%d')
    arguments['date_time<'] = end_date.strftime('%Y-%m-%d')

    print(arguments)
    df = GetData().get(table='data_buoys', arguments=arguments)

    print(df)
    df.date_time = df.date_time.dt.strftime("%Y-%m-%d %H:%M:%S")

    df = df.fillna("-9999")

    result = df.to_dict('records')
    
    return JSONResponse(content=result)

@app.post("/v2/buoys")
async def data(info : Request):
    req_info = info
    return GetData().post(table='buoys', data=req_info)
