
from sqlalchemy import create_engine
import sqlalchemy
import pandas as pd
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import urllib
from urllib.parse import quote  

class GetData():

  load_dotenv()

  def __init__(self):
    self.engine = GetData.engine_create()

  def get(self, table, arguments=None):

    query = f"SELECT * FROM {table}"
    if arguments:
      query = self.create_query(query, arguments)

    df = pd.read_sql(query, self.engine)

    return df


  def post(self,table, data):

    df = pd.DataFrame(data)
    print(data)
    if table == 'buoy':
      buoy = self.get(table=table, arguments={'id': df['buoy_id']})
      if buoy.empty:
        df.to_sql(con=self.engine, name=table, if_exists='append', index=False)
        return {
            "status" : "SUCCESS",
            "data" : df.to_json()
        }
      else:
        return {
            "status" : "ERRO",
            "code" : "Boia já está no banco de dados"
        }

  def delete(self, table, **kwargs):

    query = f"DELETE FROM {table} WHERE true"
    if kwargs:
      query = self.create_query(query, kwargs)

    self.engine.execute(query)

  def feed_bd(self, table, df, data_type=None):
    self.post(table=table, df=df, data_type=data_type)


  def engine_create(qc=True):

    if qc:
      password = os.getenv('REMOBS_QC_DB_PASSWORD')
      local = os.getenv('REMOBS_QC_DB_URL')
      engine = create_engine(f"postgresql+psycopg2://{os.getenv('REMOBS_QC_DB_USR')}:{quote(password)}@{local}/{os.getenv('REMOBS_QC_DB')}")

    return engine

  def create_query(self, wargs):
    for key, value in kwargs.items():
      if type(value[1]) == list:
        if len(value[1]) == 1:
          query += f" AND {key} {value[0]} ('{value[1][0]}')"
        else:
          query += f" AND {key} {value[0]} {tuple(value[1])}"
      else:
        query += f" AND {key} {value[0]} '{value[1]}'"

    return query

