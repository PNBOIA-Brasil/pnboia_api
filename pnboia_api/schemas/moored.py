# coding: utf-8
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

	buoy_id: Optional[int]
	hull_id: Optional[int]
	name: Optional[str]
	deploy_date: Optional[datetime.date]
	last_date_time: Optional[datetime.timestamp]
	latitude: Optional[float]
	longitude: Optional[float]
	geom: geometry(POINT 4326) GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude::double precision latitude::double precision)4326)) STORED
	status: Optional[bool]
	mode: Optional[str]
	watch_circle_distance: Optional[int]
	wmo_number: Optional[str]
	antenna_id: Optional[str]
	open_data: Optional[bool]
	link_site_pnboia: text
	metarea_section: Optional[str]
	project_id: Optional[int]
	CONSTRAINT buoys_pk PRIMARY KEY (buoy_id)


    class Config:
        orm_mode = True

from sqlalchemy import Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, JSON, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class MetareaVBase(BaseModel):

    area_id: Optional[int]
    area: Optional[]
    geometry: Optional[]

class BuoyBase(BaseModel):

    buoy_id: Optional[int]
    hull_id: Optional[int]
    name: Optional[]
    deploy_date: Optional[datetime.datetime]
    last_date_time: Optional[]
    latitude: Optional[]
    longitude: Optional[]
    geom: Optional[]
    status: Optional[]
    mode: Optional[]
    watch_circle_distance: Optional[]
    wmo_number: Optional[]
    antenna_id: Optional[int]
    open_data: Optional[]
    link_site_pnboia: Optional[]
    metarea_section: Optional[]
    project_id: Optional[int]

    hull: Optional[]
    metarea_v: Optional[]
    project: Optional[]


class AlertBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    drift: Optional[]
    transmission: Optional[]
    transmission_gap: Optional[]
    sensor_fail: Optional[]
    manual_watch_circle: Optional[]
    auto_drift_alert: Optional[]

    buoy: Optional[]


class AxysAdcpBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    year: Optional[]
    month: Optional[]
    day: Optional[]
    hour: Optional[]
    cspd1: Optional[]
    cdir1: Optional[]
    cspd2: Optional[]
    cdir2: Optional[]
    cspd3: Optional[]
    cdir3: Optional[]
    cspd4: Optional[]
    cdir4: Optional[]
    cspd5: Optional[]
    cdir5: Optional[]
    cspd6: Optional[]
    cdir6: Optional[]
    cspd7: Optional[]
    cdir7: Optional[]
    cspd8: Optional[]
    cdir8: Optional[]
    cspd9: Optional[]
    cdir9: Optional[]
    cspd10: Optional[]
    cdir10: Optional[]
    cspd11: Optional[]
    cdir11: Optional[]
    cspd12: Optional[]
    cdir12: Optional[]
    cspd13: Optional[]
    cdir13: Optional[]
    cspd14: Optional[]
    cdir14: Optional[]
    cspd15: Optional[]
    cdir15: Optional[]
    cspd16: Optional[]
    cdir16: Optional[]
    cspd17: Optional[]
    cdir17: Optional[]
    cspd18: Optional[]
    cdir18: Optional[]
    cspd19: Optional[]
    cdir19: Optional[]
    cspd20: Optional[]
    cdir20: Optional[]

    buoy: Optional[]


class AxysGeneralBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[]
    latitude: Optional[]
    longitude: Optional[]
    geom: Optional[]
    battery: Optional[]
    compass: Optional[]
    wspd1: Optional[]
    wdir1: Optional[]
    gust1: Optional[]
    wspd2: Optional[]
    wdir2: Optional[]
    gust2: Optional[]
    atmp: Optional[]
    srad: Optional[]
    rh: Optional[]
    dewpt: Optional[]
    pres: Optional[]
    sst: Optional[]
    cspd1: Optional[]
    cdir1: Optional[]
    cspd2: Optional[]
    cdir2: Optional[]
    cspd3: Optional[]
    cdir3: Optional[]
    swvht: Optional[]
    tp: Optional[]
    wvdir: Optional[]
    mxwvht: Optional[]
    wvspread: Optional[]

    buoy: Optional[]


class BmobrRawBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[]
    data_string: Optional[]

    buoy: Optional[]


class BmobrTriaxysRawBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[]
    data_string: Optional[]

    buoy: Optional[]


class RegisterBuoyBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    location: Optional[]
    state: Optional[]
    latitude: Optional[]
    longitude: Optional[]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    duration: Optional[]
    current_configuration: Optional[]
    depth: Optional[]
    cable: Optional[]

    buoy: Optional[]

class SpotterGeneralBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[]
    latitude: Optional[]
    longitude: Optional[]
    geom: Optional[]
    wspd: Optional[]
    wdir: Optional[]
    sst: Optional[]
    swvht: Optional[]
    tp: Optional[]
    tm: Optional[]
    pkdir: Optional[]
    wvdir: Optional[]
    pkspread: Optional[]
    wvspread: Optional[]

    buoy: Optional[]


class SpotterSmartMooringBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[]
    latitude: Optional[]
    longitude: Optional[]
    sensors_data: Optional[]

    buoy: Optional[]


class SpotterSmartMoringConfigBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    sensor: Optional[]
    depth: Optional[]

    buoy: Optional[]


class SpotterSystemBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[]
    latitude: Optional[]
    longitude: Optional[]
    geom: Optional[]
    battery_power: Optional[]
    battery_voltage: Optional[]
    solar_voltage: Optional[]
    humidity: Optional[]

    buoy: Optional[]


class TagBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[]
    latitude: Optional[]
    longitude: Optional[]
    geom: Optional[]

    buoy: Optional[]


class BmobrGeneralBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    date_time: Optional[]
    latitude: Optional[]
    longitude: Optional[]
    geom: Optional[]
    battery: Optional[]
    compass: Optional[]
    wspd1: Optional[]
    wdir1: Optional[]
    gust1: Optional[]
    wspd2: Optional[]
    wdir2: Optional[]
    gust2: Optional[]
    atmp: Optional[]
    srad: Optional[]
    rh: Optional[]
    dewpt: Optional[]
    pres: Optional[]
    sst: Optional[]
    cspd1: Optional[]
    cdir1: Optional[]
    cspd2: Optional[]
    cdir2: Optional[]
    cspd3: Optional[]
    cdir3: Optional[]
    cspd4: Optional[]
    cdir4: Optional[]
    cspd5: Optional[]
    cdir5: Optional[]
    cspd6: Optional[]
    cdir6: Optional[]
    cspd7: Optional[]
    cdir7: Optional[]
    cspd8: Optional[]
    cdir8: Optional[]
    cspd9: Optional[]
    cdir9: Optional[]
    cspd10: Optional[]
    cdir10: Optional[]
    cspd11: Optional[]
    cdir11: Optional[]
    cspd12: Optional[]
    cdir12: Optional[]
    cspd13: Optional[]
    cdir13: Optional[]
    cspd14: Optional[]
    cdir14: Optional[]
    cspd15: Optional[]
    cdir15: Optional[]
    cspd16: Optional[]
    cdir16: Optional[]
    cspd17: Optional[]
    cdir17: Optional[]
    cspd18: Optional[]
    cdir18: Optional[]
    swvht1: Optional[]
    tp1: Optional[]
    mxwvht1: Optional[]
    wvdir1: Optional[]
    wvspread1: Optional[]
    swvht2: Optional[]
    tp2: Optional[]
    wvdir2: Optional[]

    buoy: Optional[]
    bmobr_raw: Optional[]


class BmobrTriaxyBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    raw_id: Optional[int]
    date_time: Optional[datetime.datetime]
    mean_average_direction: Optional[float]
    spread_direction: Optional[float]
    period: Optional[float]
    energy: Optional[float]
    wvdir: Optional[float]
    spread: Optional[float]

class OperationBase(BaseModel):

    id: Optional[int]
    ship: Optional[]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    type: Optional[str]
    report: Optional[str]
    team: Optional[dict]
    register_id: Optional[int]

class SensorBase(BaseModel):

    id: Optional[int]
    sensor_id: Optional[int]
    sensor_type: Optional[str]
    register_id: Optional[int]



class SetupBuoyBase(BaseModel):

    id: Optional[int]
    height_anemometer_1: Optional[float]
    height_anemometer_2: Optional[float]
    height_thermohygrometer: Optional[float]
    height_barometer: Optional[float]
    depth_adcp: Optional[float]
    depth_temp_sensor: Optional[float]
    register_id: Optional[int]
