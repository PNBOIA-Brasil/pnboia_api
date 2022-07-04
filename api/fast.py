from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from datamodelapi.bd import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/buoys")
def data():
    df = Getdata().get(table='buoys')

    return df.to_json()

@app.get("/data_buoys")
def data(data, table='raw_articles'):

    res = Getdata().post(table=table, data=data)
    return res


@app.delete("/data/{table}/")
def delete(table):

    res = Getdata().delete(table=table)
    print(res)
    return res
