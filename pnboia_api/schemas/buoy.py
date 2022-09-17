from pydantic import BaseModel, HttpUrl
import datetime
from typing import Optional, Any, List

class BuoyBase(BaseModel):
    id: Optional[int]
    name_buoy: Optional[str]
    model: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    depth: Optional[int]
    deploy_date: Optional[datetime.datetime]
    status: Optional[str]
    wmo_number: Optional[str]
    duration_wave: Optional[int]
    h_sensor_pres: Optional[float]
    d_sensor_wtmp: Optional[float]
    wtmp_prec: Optional[float]
    wind_avg: Optional[float]
    h_sensor_wind: Optional[float]
    h_sensor_atmp: Optional[float]
    gust_avg: Optional[int]
    atmp_avg: Optional[int]
    d_curr: Optional[float]
    h_sensor_wind_2: Optional[float]

    class Config:
        orm_mode = True
