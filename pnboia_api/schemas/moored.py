# coding: utf-8
from pydantic import BaseModel, HttpUrl, validator, Json
import datetime
from typing import Optional, Any, List
# from geojson_pydantic import Feature, Polygon, Point

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

class BuoyBase(BaseModel):

    buoy_id: Optional[int]
    hull_id: Optional[int]
    name: Optional[str]
    deploy_date: Optional[datetime.date]
    last_date_time: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    geom: Optional[str]
    status: Optional[bool]
    mode: Optional[str]
    watch_circle_distance: Optional[int]
    wmo_number: Optional[str]
    antenna_id: Optional[str]
    open_data: Optional[bool]
    link_site_pnboia: Optional[str]
    metarea_section: Optional[str]
    project_id: Optional[int]

    @validator('geom', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    class Config:
        orm_mode = True

class BuoyNewBase(BaseModel):

    hull_id: Optional[int]
    name: Optional[str]
    deploy_date: Optional[datetime.date]
    latitude: Optional[float]
    longitude: Optional[float]
    status: Optional[bool]
    mode: Optional[str]
    wmo_number: Optional[str]
    antenna_id: Optional[str]
    open_data: Optional[bool]
    link_site_pnboia: Optional[str]
    metarea_section: Optional[str]
    project_id: Optional[int]

    class Config:
        orm_mode = True

class AxysAdcpBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    hour: Optional[int]
    cspd1: Optional[float]
    cdir1: Optional[int]
    cspd2: Optional[float]
    cdir2: Optional[int]
    cspd3: Optional[float]
    cdir3: Optional[int]
    cspd4: Optional[float]
    cdir4: Optional[int]
    cspd5: Optional[float]
    cdir5: Optional[int]
    cspd6: Optional[float]
    cdir6: Optional[int]
    cspd7: Optional[float]
    cdir7: Optional[int]
    cspd8: Optional[float]
    cdir8: Optional[int]
    cspd9: Optional[float]
    cdir9: Optional[int]
    cspd10: Optional[float]
    cdir10: Optional[int]
    cspd11: Optional[float]
    cdir11: Optional[int]
    cspd12: Optional[float]
    cdir12: Optional[int]
    cspd13: Optional[float]
    cdir13: Optional[int]
    cspd14: Optional[float]
    cdir14: Optional[int]
    cspd15: Optional[float]
    cdir15: Optional[int]
    cspd16: Optional[float]
    cdir16: Optional[int]
    cspd17: Optional[float]
    cdir17: Optional[int]
    cspd18: Optional[float]
    cdir18: Optional[int]
    cspd19: Optional[float]
    cdir19: Optional[int]
    cspd20: Optional[float]
    cdir20: Optional[int]

    class Config:
        orm_mode = True

class AxysGeneralBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    geom: Optional[str]
    battery: Optional[float]
    compass: Optional[int]
    wspd1: Optional[float]
    wdir1: Optional[int]
    gust1: Optional[float]
    wspd2: Optional[float]
    wdir2: Optional[int]
    gust2: Optional[float]
    atmp: Optional[float]
    srad: Optional[float]
    rh: Optional[float]
    dewpt: Optional[float]
    pres: Optional[float]
    sst: Optional[float]
    cspd1: Optional[float]
    cdir1: Optional[int]
    cspd2: Optional[float]
    cdir2: Optional[int]
    cspd3: Optional[float]
    cdir3: Optional[int]
    swvht: Optional[float]
    tp: Optional[float]
    wvdir: Optional[float]
    mxwvht: Optional[float]
    wvspread: Optional[float]

    @validator('geom', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    # buoy: Optional[Buoy]
    class Config:
        orm_mode = True

class BmobrGeneralBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    geom: Optional[str]
    battery: Optional[float]
    compass: Optional[float]
    wspd1: Optional[float]
    wdir1: Optional[int]
    gust1: Optional[float]
    wspd2: Optional[float]
    wdir2: Optional[int]
    gust2: Optional[float]
    atmp: Optional[float]
    srad: Optional[float]
    rh: Optional[float]
    dewpt: Optional[float]
    pres: Optional[float]
    sst: Optional[float]
    cspd1: Optional[float]
    cdir1: Optional[int]
    cspd2: Optional[float]
    cdir2: Optional[int]
    cspd3: Optional[float]
    cdir3: Optional[int]
    cspd4: Optional[float]
    cdir4: Optional[int]
    cspd5: Optional[float]
    cdir5: Optional[int]
    cspd6: Optional[float]
    cdir6: Optional[int]
    cspd7: Optional[float]
    cdir7: Optional[int]
    cspd8: Optional[float]
    cdir8: Optional[int]
    cspd9: Optional[float]
    cdir9: Optional[int]
    cspd10: Optional[float]
    cdir10: Optional[int]
    cspd11: Optional[float]
    cdir11: Optional[int]
    cspd12: Optional[float]
    cdir12: Optional[int]
    cspd13: Optional[float]
    cdir13: Optional[int]
    cspd14: Optional[float]
    cdir14: Optional[int]
    cspd15: Optional[float]
    cdir15: Optional[int]
    cspd16: Optional[float]
    cdir16: Optional[int]
    cspd17: Optional[float]
    cdir17: Optional[int]
    cspd18: Optional[float]
    cdir18: Optional[int]
    swvht1: Optional[float]
    tp1: Optional[float]
    mxwvht1: Optional[float]
    wvdir1: Optional[int]
    wvspread1: Optional[int]
    swvht2: Optional[float]
    tp2: Optional[float]
    wvdir2: Optional[int]

    @validator('geom', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    # buoy: Optional[Buoy]
    # bmobr_raw: Optional[BmobrRaw]
    class Config:
        orm_mode = True


class BmobrRawBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    data_string: Optional[str]

    # buoy: Optional[Buoy]

    class Config:
        orm_mode = True

class BmobrTriaxysRawBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    data_string: Optional[str]

    # buoy: Optional[Buoy]
    class Config:
        orm_mode = True

class CriosferaGeneralBase(BaseModel):

    id: Optional[float]
    buoy_id: Optional[float]
    date_time: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    geom: Optional[str]
    battery: Optional[float]
    temp_datalogger: Optional[float]
    atmp: Optional[float]
    pres: Optional[float]
    rh: Optional[float]
    srad: Optional[float]
    cond: Optional[float]
    sss: Optional[float]
    sst: Optional[float]
    wspd1: Optional[float]
    wdir1: Optional[float]
    status1: Optional[float]
    wspd2: Optional[float]
    wdir2: Optional[float]

    @validator('geom', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    # buoy: Optional[Buoy]
    # bmobr_raw: Optional[BmobrRaw]
    class Config:
        orm_mode = True

class SpotterAllBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    geom: Optional[str]
    wspd1: Optional[float]
    wdir1: Optional[int]
    sst: Optional[float]
    swvht1: Optional[float]
    tp1: Optional[float]
    tm1: Optional[float]
    pkdir1: Optional[int]
    wvdir1: Optional[int]
    pkspread1: Optional[int]
    wvspread1: Optional[int]
    sensors_data: Optional[dict]

    @validator('geom', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    # buoy: Optional[Buoy]
    class Config:
        orm_mode = True

class SpotterSmartMooringConfigBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    sensor: Optional[str]
    depth: Optional[int]

    class Config:
        orm_mode = True

class SpotterSmartMooringConfigNewBase(BaseModel):

    buoy_id: Optional[int]
    sensor: Optional[str]
    depth: Optional[int]

    class Config:
        orm_mode = True

class SpotterSystemBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    geom: Optional[str]
    battery_power: Optional[float]
    battery_voltage: Optional[float]
    solar_voltage: Optional[float]
    humidity: Optional[float]

    @validator('geom', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    # buoy: Optional[Buoy]
    class Config:
        orm_mode = True


class TriaxysGeneralBase(BaseModel):
    id: Optional[int]
    buoy_id: Optional[int]
    raw_id: Optional[int]
    message_id: Optional[str]
    date_time: Optional[datetime.datetime]
    latitude: Optional[str]
    longitude: Optional[float]
    geom: Optional[str]
    wavestats_timestamp: Optional[int]
    wavestats_duration: Optional[int]
    zero_crossings: Optional[int]
    avwvht: Optional[float]
    tav: Optional[float]
    mxwvht1: Optional[float]
    tmax: Optional[float]
    pk_crest: Optional[float]
    swvht1: Optional[float]
    tsig: Optional[float]
    h110: Optional[float]
    t110: Optional[float]
    tm02: Optional[float]
    tp1: Optional[float]
    tp_dir: Optional[float]
    tp_spread: Optional[float]
    tp5: Optional[float]
    hm0: Optional[float]
    te: Optional[float]
    wvdir1: Optional[int]
    tm01: Optional[float]
    sst: Optional[float]

    @validator('geom', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    # buoy: Optional[Buoy]
    class Config:
        orm_mode = True

class TriaxysRawBase(BaseModel):
    id: Optional[int]
    buoy_id: Optional[int]
    prime_id: Optional[int]
    data_type: Optional[str]
    date_time_transm: Optional[datetime.datetime]
    date_time: Optional[datetime.datetime]
    string: Optional[str]

    class Config:
        orm_mode = True

class TriaxysStatusBase(BaseModel):
    id: Optional[int]
    raw_id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    geom: Optional[str]
    watch_circle_status: Optional[int]
    av_serv_persec: Optional[float]
    inst_node_current: Optional[float]
    battery: Optional[float]
    pcb_temp: Optional[float]
    n_resets: Optional[int]
    curr_boot_timestamp: Optional[int]
    shutdown_type: Optional[int]
    memory_max_free: Optional[int]
    log_error_count: Optional[int]
    last_log_error: Optional[int]
    free_space: Optional[int]
    error_count: Optional[int]
    solar_voltage: Optional[float]
    water_intrusion_voltage: Optional[float]
    time_sync: Optional[float]
    terminal_cnr: Optional[float]


    @validator('geom', pre=True,allow_reuse=True, always=True)
    def correct_geom_format(cls, v):
        if not isinstance(v, WKBElement):
            return None
            # raise ValueError('must be a valid WKBE element')
        return ewkb_to_wkt(v)

    # buoy: Optional[Buoy]
    class Config:
        orm_mode = True

class AlertBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    position: Optional[float]
    transmission: Optional[float]
    transmission_gap: Optional[float]
    high_values: Optional[dict]
    sensor_fail: Optional[dict]
    low_values: Optional[dict]
    email: Optional[str]

    class Config:
        orm_mode = True

class AlertNewBase(BaseModel):

    buoy_id: Optional[int]
    position: Optional[float]
    transmission: Optional[float]
    transmission_gap: Optional[float]
    high_values: Optional[dict]
    sensor_fail: Optional[dict]
    low_values: Optional[dict]
    email: Optional[str]

    class Config:
        orm_mode = True
