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

