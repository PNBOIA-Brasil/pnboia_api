# coding: utf-8
from pydantic import BaseModel, HttpUrl, validator, Json, Field
import datetime
from typing import Optional, Any, List
from geojson_pydantic import Feature, Polygon, Point

from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement

from pnboia_api.models.moored import Buoy
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

class QualifiedDataBase(BaseModel):

    id: Optional[int]
    raw_id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    geom: Optional[str]
    battery: Optional[float]
    flag_battery: Optional[int]
    rh: Optional[float]
    flag_rh: Optional[int]
    wspd1: Optional[float]
    flag_wspd1: Optional[int]
    wdir1: Optional[int]
    flag_wdir1: Optional[int]
    wspd2: Optional[float]
    flag_wspd2: Optional[int]
    wdir2: Optional[int]
    flag_wdir2: Optional[int]
    gust1: Optional[float]
    flag_gust1: Optional[int]
    gust2: Optional[float]
    flag_gust2: Optional[int]
    atmp: Optional[float]
    flag_atmp: Optional[int]
    pres: Optional[float]
    flag_pres: Optional[int]
    srad: Optional[float]
    flag_srad: Optional[int]
    dewpt: Optional[float]
    flag_dewpt: Optional[int]
    sst: Optional[float]
    flag_sst: Optional[int]
    cspd1: Optional[float]
    flag_cspd1: Optional[int]
    cdir1: Optional[int]
    flag_cdir1: Optional[int]
    cspd2: Optional[float]
    flag_cspd2: Optional[int]
    cdir2: Optional[int]
    flag_cdir2: Optional[int]
    cspd3: Optional[float]
    flag_cspd3: Optional[int]
    cdir3: Optional[int]
    flag_cdir3: Optional[int]
    cspd4: Optional[float]
    flag_cspd4: Optional[int]
    cdir4: Optional[int]
    flag_cdir4: Optional[int]
    cspd5: Optional[float] #= Field(alias="ADCP5_TEST")
    flag_cspd5: Optional[int]
    cdir5: Optional[int]
    flag_cdir5: Optional[int]
    cspd6: Optional[float]
    flag_cspd6: Optional[int]
    cdir6: Optional[int]
    flag_cdir6: Optional[int]
    cspd7: Optional[float]
    flag_cspd7: Optional[int]
    cdir7: Optional[int]
    flag_cdir7: Optional[int]
    cspd8: Optional[float]
    flag_cspd8: Optional[int]
    cdir8: Optional[int]
    flag_cdir8: Optional[int]
    cspd9: Optional[float]
    flag_cspd9: Optional[int]
    cdir9: Optional[int]
    flag_cdir9: Optional[int]
    cspd10: Optional[float]
    flag_cspd10: Optional[int]
    cdir10: Optional[int]
    flag_cdir10: Optional[int]
    cspd11: Optional[int]
    flag_cspd11: Optional[int]
    cdir11: Optional[int]
    flag_cdir11: Optional[int]
    cspd12: Optional[float]
    flag_cspd12: Optional[int]
    cdir12: Optional[int]
    flag_cdir12: Optional[int]
    cspd13: Optional[float]
    flag_cspd13: Optional[int]
    cdir13: Optional[int]
    flag_cdir13: Optional[int]
    cspd14: Optional[float]
    flag_cspd14: Optional[int]
    cdir14: Optional[int]
    flag_cdir14: Optional[int]
    cspd15: Optional[float]
    flag_cspd15: Optional[int]
    cdir15: Optional[int]
    flag_cdir15: Optional[int]
    cspd16: Optional[float]
    flag_cspd16: Optional[int]
    cdir16: Optional[int]
    flag_cdir16: Optional[int]
    cspd17: Optional[float]
    flag_cspd17: Optional[int]
    cdir17: Optional[int]
    flag_cdir17: Optional[int]
    cspd18: Optional[float]
    flag_cspd18: Optional[int]
    cdir18: Optional[int]
    flag_cdir18: Optional[int]
    swvht1: Optional[float]
    flag_swvht1: Optional[int]
    tp1: Optional[float]
    flag_tp1: Optional[int]
    mxwvht1: Optional[float]
    flag_mxwvht1: Optional[int]
    wvdir1: Optional[int]
    flag_wvdir1: Optional[int]
    wvspread1: Optional[int]
    flag_wvspread1: Optional[int]
    swvht2: Optional[float]
    flag_swvht2: Optional[int]
    tp2: Optional[float]
    flag_tp2: Optional[int]
    wvdir2: Optional[int]
    flag_wvdir2: Optional[int]
    tm1: Optional[float]
    flag_tm1: Optional[int]
    pkdir1: Optional[float]
    flag_pkdir1: Optional[int]
    pkspread1: Optional[float]
    flag_pkspread1: Optional[int]
    sensors_data_flagged: Optional[dict]
    cond: Optional[float]
    flag_cond: Optional[int]
    sss: Optional[float]
    flag_sss: Optional[int]

    @validator('geom', pre=True,allow_reuse=True,whole=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)


    class Config:
        orm_mode = True
        #allow_population_by_field_name = True
