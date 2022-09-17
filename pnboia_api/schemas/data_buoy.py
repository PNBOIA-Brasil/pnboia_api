from pydantic import BaseModel, HttpUrl
import datetime
from typing import Optional, Any, List

class DataBuoyBase(BaseModel):
    id: int
    name_buoy: str
    model: str
    lat: float
    lon: float
    depth: int
    deploy_date: datetime.datetime
    status: str
    wmo_number: str
    duration_wave: int
    h_sensor_pres: float
    d_sensor_wtmp: float
    wtmp_prec: float
    wind_avg: float
    h_sensor_wind: float
    h_sensor_atmp: float
    gust_avg: int
    atmp_avg: int
    d_curr: float
    h_sensor_wind_2: float

    class Config:
        orm_mode = True
