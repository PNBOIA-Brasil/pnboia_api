# coding: utf-8
from pydantic import BaseModel, HttpUrl, validator, Json
import datetime
from typing import Optional, Any, List
from geojson_pydantic import Feature, Polygon, Point

from geoalchemy2.shape import to_shape 
from geoalchemy2.elements import WKBElement

from sqlalchemy import Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, JSON, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.declarative import declarative_base

class BuoyDriftBase(BaseModel):
    buoy_id: Optional[int]
    hull_id: Optional[int]
    model: Optional[str]
    latitude_deploy: Optional[float]
    longitude_deploy: Optional[float]
    deploy_date: Optional[datetime.date]
    last_date_time: Optional[datetime.datetime]
    last_latitude: Optional[float]
    last_longitude: Optional[float]
    geom_deploy: Optional[str]
    geom_last_position: Optional[str]
    project_id: Optional[int]

    @validator('geom_deploy', pre=True,allow_reuse=True,whole=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    @validator('geom_last_position', pre=True,allow_reuse=True,whole=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    class Config:
        orm_mode = True


class SpotterGeneralBase(BaseModel):
    id: Optional[int]
    buoy_id: Optional[int]
    wspd1: Optional[str]
    wdir1: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    date_time: Optional[str]
    swvht1: Optional[str]
    tp1: Optional[str]
    tm1: Optional[str]
    pkdir1: Optional[str]
    pkspread1: Optional[str]
    wvdir1: Optional[str]
    wvspread1: Optional[str]
    sst: Optional[float]

    class Config:
        orm_mode = True

class SpotterSystemBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    battery_power: Optional[float]
    battery_voltage: Optional[float]
    humidity: Optional[float]
    solar_voltage: Optional[float]

    class Config:
        orm_mode = True

class SpotterWavesBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    frequency: Optional[str]
    df: Optional[str]
    a1: Optional[str]
    b1: Optional[str]
    a2: Optional[str]
    b2: Optional[str]
    varianceDensity: Optional[str]
    direction: Optional[str]
    directionalSpread: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        orm_mode = True