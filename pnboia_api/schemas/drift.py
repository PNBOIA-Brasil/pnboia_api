# coding: utf-8
from pydantic import BaseModel, HttpUrl, validator, Json
import datetime
from typing import Optional, Any, List
# from geojson_pydantic import Feature, Polygon, Point

from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement

from pnboia_api.models.drift import BuoyDrift
from sqlalchemy import Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, JSON, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.declarative import declarative_base


def ewkb_to_wkt(geom: WKBElement):
    """
    Converts a geometry formated as WKBE to WKT
    in order to parse it into pydantic Model

    Args:
        geom (WKBElement): A geometry from GeoAlchemy query
    """
    return to_shape(geom).wkt




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
    antenna_id: Optional[str]

    @validator('geom_last_position', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    @validator('geom_deploy', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)


    class Config:
        orm_mode = True


class BuoyDriftNewBase(BaseModel):
    hull_id: Optional[int]
    model: Optional[str]
    latitude_deploy: Optional[float]
    longitude_deploy: Optional[float]
    deploy_date: Optional[datetime.date]
    project_id: Optional[int]
    antenna_id: Optional[str]

    class Config:
        orm_mode = True

class SpotterGeneralDriftBase(BaseModel):
    id: Optional[int]
    buoy_id: Optional[int]
    wspd1: Optional[float]
    wdir1: Optional[float]
    latitude: Optional[float]
    longitude: Optional[float]
    date_time: Optional[datetime.datetime]
    swvht1: Optional[float]
    tp1: Optional[float]
    tm1: Optional[float]
    pkdir1: Optional[float]
    pkspread1: Optional[float]
    wvdir1: Optional[float]
    wvspread1: Optional[float]
    sst: Optional[float]

    class Config:
        orm_mode = True

class SpotterSystemDriftBase(BaseModel):

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

class SpotterWavesDriftBase(BaseModel):

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
