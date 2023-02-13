# coding: utf-8
from pydantic import BaseModel, HttpUrl, validator, Json
import datetime
from typing import Optional, Any, List
from geojson_pydantic import Feature, Polygon, Point

from geoalchemy2.shape import to_shape 
from geoalchemy2.elements import WKBElement

from pnboia_api.models.moored import Buoy
from pnboia_api.schemas.moored import BuoyBase

from sqlalchemy import Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, JSON, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.declarative import declarative_base
import numpy as np

def ewkb_to_wkt(geom: WKBElement):
    """
    Converts a geometry formated as WKBE to WKT 
    in order to parse it into pydantic Model

    Args:
        geom (WKBElement): A geometry from GeoAlchemy query
    """
    return to_shape(geom).wkt

class QualifiedDataPetrobrasBase(BaseModel):

    id: Optional[int] = None
    raw_id: Optional[int] = None
    buoy_id: Optional[int] = None
    date_time: Optional[datetime.datetime] = None
    Timestamp: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geom: Optional[str] = None
    battery: Optional[float] = None
    flag_battery: Optional[int] = None
    HMS_HUMIDITY: Optional[float] = None
    flag_HMS_HUMIDITY: Optional[int] = None
    HMS_WIND_SPEED1: Optional[float] = None
    flag_HMS_WIND_SPEED1: Optional[int] = None
    HMS_WIND_DIRECTION1: Optional[int] = None
    flag_HMS_WIND_DIRECTION1: Optional[int] = None
    HMS_WIND_SPEED2: Optional[float] = None
    flag_HMS_WIND_SPEED2: Optional[int] = None
    HMS_WIND_DIRECTION2: Optional[int] = None
    flag_HMS_WIND_DIRECTION2: Optional[int] = None
    gust1: Optional[float] = None
    flag_gust1: Optional[int] = None
    gust2: Optional[float] = None
    flag_gust2: Optional[int] = None
    HMS_TEMPERATURE: Optional[float] = None
    flag_HMS_TEMPERATURE: Optional[int] = None
    HMS_PRESSURE: Optional[float] = None
    flag_HMS_PRESSURE: Optional[int] = None
    srad: Optional[float] = None
    flag_srad: Optional[int] = None
    dewpt: Optional[float] = None
    flag_dewpt: Optional[int] = None
    TEMPERATURA_AGUA: Optional[float] = None
    flag_TEMPERATURA_AGUA: Optional[int] = None
    ADCP_BIN1_SPEED: Optional[float] = None
    flag_ADCP_BIN1_SPEED: Optional[int] = None
    ADCP_BIN1_DIRECTION: Optional[int] = None
    flag_ADCP_BIN1_DIRECTION: Optional[int] = None
    ADCP_BIN2_SPEED: Optional[float] = None
    flag_ADCP_BIN2_SPEED: Optional[int] = None
    ADCP_BIN2_DIRECTION: Optional[int] = None
    flag_ADCP_BIN2_DIRECTION: Optional[int] = None
    ADCP_BIN3_SPEED: Optional[float] = None
    flag_ADCP_BIN3_SPEED: Optional[int] = None
    ADCP_BIN3_DIRECTION: Optional[int] = None
    flag_ADCP_BIN3_DIRECTION: Optional[int] = None
    ADCP_BIN4_SPEED: Optional[float] = None
    flag_ADCP_BIN4_SPEED: Optional[int] = None
    ADCP_BIN4_DIRECTION: Optional[int] = None
    flag_ADCP_BIN4_DIRECTION: Optional[int] = None
    ADCP_BIN5_SPEED: Optional[float] = None
    flag_ADCP_BIN5_SPEED: Optional[int] = None
    ADCP_BIN5_DIRECTION: Optional[int] = None
    flag_ADCP_BIN5_DIRECTION: Optional[int] = None
    ADCP_BIN6_SPEED: Optional[float] = None
    flag_ADCP_BIN6_SPEED: Optional[int] = None
    ADCP_BIN6_DIRECTION: Optional[int] = None
    flag_ADCP_BIN6_DIRECTION: Optional[int] = None
    ADCP_BIN7_SPEED: Optional[float] = None
    flag_ADCP_BIN7_SPEED: Optional[int] = None
    ADCP_BIN7_DIRECTION: Optional[int] = None
    flag_ADCP_BIN7_DIRECTION: Optional[int] = None
    ADCP_BIN8_SPEED: Optional[float] = None
    flag_ADCP_BIN8_SPEED: Optional[int] = None
    ADCP_BIN8_DIRECTION: Optional[int] = None
    flag_ADCP_BIN8_DIRECTION: Optional[int] = None
    ADCP_BIN9_SPEED: Optional[float] = None
    flag_ADCP_BIN9_SPEED: Optional[int] = None
    ADCP_BIN9_DIRECTION: Optional[int] = None
    flag_ADCP_BIN9_DIRECTION: Optional[int] = None
    ADCP_BIN10_SPEED: Optional[float] = None
    flag_ADCP_BIN10_SPEED: Optional[int] = None
    ADCP_BIN10_DIRECTION: Optional[int] = None
    flag_ADCP_BIN10_DIRECTION: Optional[int] = None
    ADCP_BIN11_SPEED: Optional[int] = None
    flag_ADCP_BIN11_SPEED: Optional[int] = None
    ADCP_BIN11_DIRECTION: Optional[int] = None
    flag_ADCP_BIN11_DIRECTION: Optional[int] = None
    ADCP_BIN12_SPEED: Optional[float] = None
    flag_ADCP_BIN12_SPEED: Optional[int] = None
    ADCP_BIN12_DIRECTION: Optional[int] = None
    flag_ADCP_BIN12_DIRECTION: Optional[int] = None
    ADCP_BIN13_SPEED: Optional[float] = None
    flag_ADCP_BIN13_SPEED: Optional[int] = None
    ADCP_BIN13_DIRECTION: Optional[int] = None
    flag_ADCP_BIN13_DIRECTION: Optional[int] = None
    ADCP_BIN14_SPEED: Optional[float] = None
    flag_ADCP_BIN14_SPEED: Optional[int] = None
    ADCP_BIN14_DIRECTION: Optional[int] = None
    flag_ADCP_BIN14_DIRECTION: Optional[int] = None
    ADCP_BIN15_SPEED: Optional[float] = None
    flag_ADCP_BIN15_SPEED: Optional[int] = None
    ADCP_BIN15_DIRECTION: Optional[int] = None
    flag_ADCP_BIN15_DIRECTION: Optional[int] = None
    ADCP_BIN16_SPEED: Optional[float] = None
    flag_ADCP_BIN16_SPEED: Optional[int] = None
    ADCP_BIN16_DIRECTION: Optional[int] = None
    flag_ADCP_BIN16_DIRECTION: Optional[int] = None
    ADCP_BIN17_SPEED: Optional[float] = None
    flag_ADCP_BIN17_SPEED: Optional[int] = None
    ADCP_BIN17_DIRECTION: Optional[int] = None
    flag_ADCP_BIN17_DIRECTION: Optional[int] = None
    ADCP_BIN18_SPEED: Optional[float] = None
    flag_ADCP_BIN18_SPEED: Optional[int] = None
    ADCP_BIN18_DIRECTION: Optional[int] = None
    flag_ADCP_BIN18_DIRECTION: Optional[int] = None
    ADCP_BIN19_SPEED: Optional[float] = None
    flag_ADCP_BIN19_SPEED: Optional[int] = None
    ADCP_BIN19_DIRECTION: Optional[int] = None
    flag_ADCP_BIN19_DIRECTION: Optional[int] = None
    ADCP_BIN20_SPEED: Optional[float] = None
    flag_ADCP_BIN20_SPEED: Optional[int] = None
    ADCP_BIN20_DIRECTION: Optional[int] = None
    flag_ADCP_BIN20_DIRECTION: Optional[int] = None
    ADCP_BIN1_DEPTH: Optional[float] = None
    ADCP_BIN2_DEPTH: Optional[float] = None
    ADCP_BIN3_DEPTH: Optional[float] = None
    ADCP_BIN4_DEPTH: Optional[float] = None
    ADCP_BIN5_DEPTH: Optional[float] = None
    ADCP_BIN6_DEPTH: Optional[float] = None
    ADCP_BIN7_DEPTH: Optional[float] = None
    ADCP_BIN8_DEPTH: Optional[float] = None
    ADCP_BIN9_DEPTH: Optional[float] = None
    ADCP_BIN10_DEPTH: Optional[float] = None
    ADCP_BIN11_DEPTH: Optional[float] = None
    ADCP_BIN12_DEPTH: Optional[float] = None
    ADCP_BIN13_DEPTH: Optional[float] = None
    ADCP_BIN14_DEPTH: Optional[float] = None
    ADCP_BIN15_DEPTH: Optional[float] = None
    ADCP_BIN16_DEPTH: Optional[float] = None
    ADCP_BIN17_DEPTH: Optional[float] = None
    ADCP_BIN18_DEPTH: Optional[float] = None
    ADCP_BIN19_DEPTH: Optional[float] = None
    ADCP_BIN20_DEPTH: Optional[float] = None
    ONDA_ALTURA_SENSOR1: Optional[float] = None
    flag_ONDA_ALTURA_SENSOR1: Optional[int] = None
    ONDA_PERIODO_SENSOR1: Optional[float] = None
    flag_ONDA_PERIODO_SENSOR1: Optional[int] = None
    mxwvht1: Optional[float] = None
    flag_mxwvht1: Optional[int] = None
    ONDA_DIRECAOMED_SENSOR1: Optional[int] = None
    flag_ONDA_DIRECAOMED_SENSOR1: Optional[int] = None
    wvspread1: Optional[int] = None
    flag_wvspread1: Optional[int] = None
    ONDA_ALTURA_SENSOR2: Optional[float] = None
    flag_ONDA_ALTURA_SENSOR2: Optional[int] = None
    ONDA_PERIODO_SENSOR2: Optional[float] = None
    flag_ONDA_PERIODO_SENSOR2: Optional[int] = None
    ONDA_DIRECAOMED_SENSOR2: Optional[int] = None
    flag_ONDA_DIRECAOMED_SENSOR2: Optional[int] = None
    tm1: Optional[float] = None
    flag_tm1: Optional[int] = None
    pkdir1: Optional[float] = None
    flag_pkdir1: Optional[int] = None
    pkspread1: Optional[float] = None
    flag_pkspread1: Optional[int] = None
    sensors_data_flagged: Optional[dict] = None
    cond: Optional[float] = None
    flag_cond: Optional[int] = None
    sss: Optional[float] = None
    flag_sss: Optional[int] = None
    flag_latitude: Optional[float] = None
    flag_longitude: Optional[float] = None

    @validator('geom', pre=True,allow_reuse=True,whole=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)


    class Config:
        orm_mode = True

class QualifiedDataBase(BaseModel):

    id: Optional[int] = None
    raw_id: Optional[int] = None
    buoy_id: Optional[int] = None
    date_time: Optional[datetime.datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geom: Optional[str] = None
    battery: Optional[float] = None
    flag_battery: Optional[int] = None
    rh: Optional[float] = None
    flag_rh: Optional[int] = None
    wspd1: Optional[float] = None
    flag_wspd1: Optional[int] = None
    wdir1: Optional[int] = None
    flag_wdir1: Optional[int] = None
    wspd2: Optional[float] = None
    flag_wspd2: Optional[int] = None
    wdir2: Optional[int] = None
    flag_wdir2: Optional[int] = None
    gust1: Optional[float] = None
    flag_gust1: Optional[int] = None
    gust2: Optional[float] = None
    flag_gust2: Optional[int] = None
    atmp: Optional[float] = None
    flag_atmp: Optional[int] = None
    pres: Optional[float] = None
    flag_pres: Optional[int] = None
    srad: Optional[float] = None
    flag_srad: Optional[int] = None
    dewpt: Optional[float] = None
    flag_dewpt: Optional[int] = None
    sst: Optional[float] = None
    flag_sst: Optional[int] = None
    cspd1: Optional[float] = None
    flag_cspd1: Optional[int] = None
    cdir1: Optional[int] = None
    flag_cdir1: Optional[int] = None
    cspd2: Optional[float] = None
    flag_cspd2: Optional[int] = None
    cdir2: Optional[int] = None
    flag_cdir2: Optional[int] = None
    cspd3: Optional[float] = None
    flag_cspd3: Optional[int] = None
    cdir3: Optional[int] = None
    flag_cdir3: Optional[int] = None
    cspd4: Optional[float] = None
    flag_cspd4: Optional[int] = None
    cdir4: Optional[int] = None
    flag_cdir4: Optional[int] = None
    cspd5: Optional[float] = None
    flag_cspd5: Optional[int] = None
    cdir5: Optional[int] = None
    flag_cdir5: Optional[int] = None
    cspd6: Optional[float] = None
    flag_cspd6: Optional[int] = None
    cdir6: Optional[int] = None
    flag_cdir6: Optional[int] = None
    cspd7: Optional[float] = None
    flag_cspd7: Optional[int] = None
    cdir7: Optional[int] = None
    flag_cdir7: Optional[int] = None
    cspd8: Optional[float] = None
    flag_cspd8: Optional[int] = None
    cdir8: Optional[int] = None
    flag_cdir8: Optional[int] = None
    cspd9: Optional[float] = None
    flag_cspd9: Optional[int] = None
    cdir9: Optional[int] = None
    flag_cdir9: Optional[int] = None
    cspd10: Optional[float] = None
    flag_cspd10: Optional[int] = None
    cdir10: Optional[int] = None
    flag_cdir10: Optional[int] = None
    cspd11: Optional[float] = None
    flag_cspd11: Optional[int] = None
    cdir11: Optional[int] = None
    flag_cdir11: Optional[int] = None
    cspd12: Optional[float] = None
    flag_cspd12: Optional[int] = None
    cdir12: Optional[int] = None
    flag_cdir12: Optional[int] = None
    cspd13: Optional[float] = None
    flag_cspd13: Optional[int] = None
    cdir13: Optional[int] = None
    flag_cdir13: Optional[int] = None
    cspd14: Optional[float] = None
    flag_cspd14: Optional[int] = None
    cdir14: Optional[int] = None
    flag_cdir14: Optional[int] = None
    cspd15: Optional[float] = None
    flag_cspd15: Optional[int] = None
    cdir15: Optional[int] = None
    flag_cdir15: Optional[int] = None
    cspd16: Optional[float] = None
    flag_cspd16: Optional[int] = None
    cdir16: Optional[int] = None
    flag_cdir16: Optional[int] = None
    cspd17: Optional[float] = None
    flag_cspd17: Optional[int] = None
    cdir17: Optional[int] = None
    flag_cdir17: Optional[int] = None
    cspd18: Optional[float] = None
    flag_cspd18: Optional[int] = None
    cdir18: Optional[int] = None
    flag_cdir18: Optional[int] = None
    swvht1: Optional[float] = None
    flag_swvht1: Optional[int] = None
    tp1: Optional[float] = None
    flag_tp1: Optional[int] = None
    mxwvht1: Optional[float] = None
    flag_mxwvht1: Optional[int] = None
    wvdir1: Optional[int] = None
    flag_wvdir1: Optional[int] = None
    wvspread1: Optional[int] = None
    flag_wvspread1: Optional[int] = None
    swvht2: Optional[float] = None
    flag_swvht2: Optional[int] = None
    tp2: Optional[float] = None
    flag_tp2: Optional[int] = None
    wvdir2: Optional[int] = None
    flag_wvdir2: Optional[int] = None
    tm1: Optional[float] = None
    flag_tm1: Optional[int] = None
    pkdir1: Optional[float] = None
    flag_pkdir1: Optional[int] = None
    pkspread1: Optional[float] = None
    flag_pkspread1: Optional[int] = None
    sensors_data_flagged: Optional[dict] = None
    cond: Optional[float] = None
    flag_cond: Optional[int] = None
    sss: Optional[float] = None
    flag_sss: Optional[int] = None
    flag_latitude: Optional[float] = None
    flag_longitude: Optional[float] = None

    @validator('geom', pre=True,allow_reuse=True,whole=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    class Config:
        orm_mode = True


class QualifiedDataBuoyBase(BaseModel):

    id: Optional[int] = None
    raw_id: Optional[int] = None
    buoy_id: Optional[int] = None
    date_time: Optional[datetime.datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geom: Optional[str] = None
    battery: Optional[float] = None
    flag_battery: Optional[int] = None
    rh: Optional[float] = None
    flag_rh: Optional[int] = None
    wspd1: Optional[float] = None
    flag_wspd1: Optional[int] = None
    wdir1: Optional[int] = None
    flag_wdir1: Optional[int] = None
    wspd2: Optional[float] = None
    flag_wspd2: Optional[int] = None
    wdir2: Optional[int] = None
    flag_wdir2: Optional[int] = None
    gust1: Optional[float] = None
    flag_gust1: Optional[int] = None
    gust2: Optional[float] = None
    flag_gust2: Optional[int] = None
    atmp: Optional[float] = None
    flag_atmp: Optional[int] = None
    pres: Optional[float] = None
    flag_pres: Optional[int] = None
    srad: Optional[float] = None
    flag_srad: Optional[int] = None
    dewpt: Optional[float] = None
    flag_dewpt: Optional[int] = None
    sst: Optional[float] = None
    flag_sst: Optional[int] = None
    cspd1: Optional[float] = None
    flag_cspd1: Optional[int] = None
    cdir1: Optional[int] = None
    flag_cdir1: Optional[int] = None
    cspd2: Optional[float] = None
    flag_cspd2: Optional[int] = None
    cdir2: Optional[int] = None
    flag_cdir2: Optional[int] = None
    cspd3: Optional[float] = None
    flag_cspd3: Optional[int] = None
    cdir3: Optional[int] = None
    flag_cdir3: Optional[int] = None
    cspd4: Optional[float] = None
    flag_cspd4: Optional[int] = None
    cdir4: Optional[int] = None
    flag_cdir4: Optional[int] = None
    cspd5: Optional[float] = None
    flag_cspd5: Optional[int] = None
    cdir5: Optional[int] = None
    flag_cdir5: Optional[int] = None
    cspd6: Optional[float] = None
    flag_cspd6: Optional[int] = None
    cdir6: Optional[int] = None
    flag_cdir6: Optional[int] = None
    cspd7: Optional[float] = None
    flag_cspd7: Optional[int] = None
    cdir7: Optional[int] = None
    flag_cdir7: Optional[int] = None
    cspd8: Optional[float] = None
    flag_cspd8: Optional[int] = None
    cdir8: Optional[int] = None
    flag_cdir8: Optional[int] = None
    cspd9: Optional[float] = None
    flag_cspd9: Optional[int] = None
    cdir9: Optional[int] = None
    flag_cdir9: Optional[int] = None
    cspd10: Optional[float] = None
    flag_cspd10: Optional[int] = None
    cdir10: Optional[int] = None
    flag_cdir10: Optional[int] = None
    cspd11: Optional[float] = None
    flag_cspd11: Optional[int] = None
    cdir11: Optional[int] = None
    flag_cdir11: Optional[int] = None
    cspd12: Optional[float] = None
    flag_cspd12: Optional[int] = None
    cdir12: Optional[int] = None
    flag_cdir12: Optional[int] = None
    cspd13: Optional[float] = None
    flag_cspd13: Optional[int] = None
    cdir13: Optional[int] = None
    flag_cdir13: Optional[int] = None
    cspd14: Optional[float] = None
    flag_cspd14: Optional[int] = None
    cdir14: Optional[int] = None
    flag_cdir14: Optional[int] = None
    cspd15: Optional[float] = None
    flag_cspd15: Optional[int] = None
    cdir15: Optional[int] = None
    flag_cdir15: Optional[int] = None
    cspd16: Optional[float] = None
    flag_cspd16: Optional[int] = None
    cdir16: Optional[int] = None
    flag_cdir16: Optional[int] = None
    cspd17: Optional[float] = None
    flag_cspd17: Optional[int] = None
    cdir17: Optional[int] = None
    flag_cdir17: Optional[int] = None
    cspd18: Optional[float] = None
    flag_cspd18: Optional[int] = None
    cdir18: Optional[int] = None
    flag_cdir18: Optional[int] = None
    swvht1: Optional[float] = None
    flag_swvht1: Optional[int] = None
    tp1: Optional[float] = None
    flag_tp1: Optional[int] = None
    mxwvht1: Optional[float] = None
    flag_mxwvht1: Optional[int] = None
    wvdir1: Optional[int] = None
    flag_wvdir1: Optional[int] = None
    wvspread1: Optional[int] = None
    flag_wvspread1: Optional[int] = None
    swvht2: Optional[float] = None
    flag_swvht2: Optional[int] = None
    tp2: Optional[float] = None
    flag_tp2: Optional[int] = None
    wvdir2: Optional[int] = None
    flag_wvdir2: Optional[int] = None
    tm1: Optional[float] = None
    flag_tm1: Optional[int] = None
    pkdir1: Optional[float] = None
    flag_pkdir1: Optional[int] = None
    pkspread1: Optional[float] = None
    flag_pkspread1: Optional[int] = None
    sensors_data_flagged: Optional[dict] = None
    cond: Optional[float] = None
    flag_cond: Optional[int] = None
    sss: Optional[float] = None
    flag_sss: Optional[int] = None
    buoy: Optional[BuoyBase] = None
    flag_latitude: Optional[float] = None
    flag_longitude: Optional[float] = None


    @validator('geom', pre=True,allow_reuse=True,whole=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    class Config:
        orm_mode = True


