# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Use the existing Base from models/__init__.py
from . import Base

class SailbuoyBuoy(Base):
    """
    Table to store sailbuoy buoy information.
    Similar to the Buoy model in moored.py but specific to sailbuoys.
    """
    __tablename__ = 'buoys'
    __table_args__ = {'schema': 'sailbuoy', 'comment': 'Table containing sailbuoy information.'}

    buoy_id = Column(SmallInteger, primary_key=True, comment='Buoy identification ID.')
    name = Column(String(30), comment='Name assigned to the sailbuoy.')
    imei = Column(String(15), comment='IMEI number of the sailbuoy.')
    model = Column(String(50), comment='Model of the sailbuoy.')
    deploy_date = Column(DateTime, comment='Date when the sailbuoy was deployed.')
    last_date_time = Column(DateTime, comment='Last recorded datetime from the sailbuoy.')
    is_active = Column(Boolean, default=True, comment='Whether the sailbuoy is currently active.')

    # Relationships
    autopilot_data = relationship("AutopilotData", back_populates="buoy")
    datalogger_data = relationship("DataloggerData", back_populates="buoy")


class AutopilotData(Base):
    """
    Table to store navigation and control data from the sailbuoy's autopilot.
    """
    __tablename__ = 'autopilot_data'
    __table_args__ = {'schema': 'sailbuoy', 'comment': 'Navigation and control data from sailbuoy autopilot.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('sailbuoy.autopilot_data_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('sailbuoy.buoys.buoy_id', onupdate='CASCADE'), nullable=False, comment='ID of the sailbuoy.')
    date_time = Column(DateTime, nullable=False, index=True, comment='Timestamp of the data record in UTC.')
    
    # Navigation data
    latitude = Column(Numeric(10, 6), comment='Latitude in decimal degrees (WGS84).')
    longitude = Column(Numeric(10, 6), comment='Longitude in decimal degrees (WGS84).')
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), 
                 Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', 
                         persisted=True), 
                 comment='Spatial point geometry (x, y) - (Longitude, Latitude)')
    
    # Vehicle state
    heading = Column(Numeric(5, 2), comment='Compass heading in degrees (0-360).')
    speed = Column(Numeric(5, 2), comment='Speed over ground in m/s.')
    distance = Column(Numeric(10, 2), comment='Total distance traveled in meters.')
    
    # Environmental data
    wind_speed = Column(Numeric(5, 2), comment='Wind speed in m/s.')
    wind_direction = Column(Numeric(5, 2), comment='Wind direction in degrees (0-360).')
    battery_voltage = Column(Numeric(5, 2), comment='Battery voltage in Volts.')
    
    # Mission data
    waypoint_id = Column(SmallInteger, comment='Current waypoint ID.')
    distance_to_waypoint = Column(Numeric(10, 2), comment='Distance to next waypoint in meters.')
    
    # System status
    cpu_temperature = Column(Numeric(5, 2), comment='CPU temperature in degrees Celsius.')
    leak_detected = Column(Boolean, comment='Whether a leak is detected in the hull.')
    
    # Relationships
    buoy = relationship("SailbuoyBuoy", foreign_keys=[buoy_id], back_populates="autopilot_data")


class DataloggerData(Base):
    """
    Table to store scientific sensor data from the sailbuoy's datalogger.
    """
    __tablename__ = 'datalogger_data'
    __table_args__ = {'schema': 'sailbuoy', 'comment': 'Scientific sensor data from sailbuoy datalogger.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('sailbuoy.datalogger_data_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('sailbuoy.buoys.buoy_id', onupdate='CASCADE'), nullable=False, comment='ID of the sailbuoy.')
    date_time = Column(DateTime, nullable=False, index=True, comment='Timestamp of the data record in UTC.')
    
    # Location data (may be interpolated from autopilot)
    latitude = Column(Numeric(10, 6), comment='Latitude in decimal degrees (WGS84).')
    longitude = Column(Numeric(10, 6), comment='Longitude in decimal degrees (WGS84).')
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), 
                 Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', 
                         persisted=True), 
                 comment='Spatial point geometry (x, y) - (Longitude, Latitude)')
    
    # Water properties
    water_temperature = Column(Numeric(5, 2), comment='Water temperature in degrees Celsius.')
    salinity = Column(Numeric(5, 2), comment='Salinity in PSU (Practical Salinity Units).')
    conductivity = Column(Numeric(8, 2), comment='Conductivity in mS/cm.')
    pressure = Column(Numeric(8, 2), comment='Water pressure in dbar.')
    
    # Optical measurements
    chlorophyll = Column(Numeric(8, 4), comment='Chlorophyll concentration in µg/L.')
    cdom = Column(Numeric(8, 4), comment='Colored Dissolved Organic Matter in ppb.')
    turbidity = Column(Numeric(8, 4), comment='Turbidity in NTU.')
    
    # Meteorological data (may be redundant with autopilot but more precise)
    air_temperature = Column(Numeric(5, 2), comment='Air temperature in degrees Celsius.')
    air_pressure = Column(Numeric(7, 2), comment='Atmospheric pressure in hPa.')
    relative_humidity = Column(Numeric(5, 2), comment='Relative humidity in %.')
    
    # System data
    battery_voltage = Column(Numeric(5, 2), comment='Battery voltage in Volts.')
    internal_temperature = Column(Numeric(5, 2), comment='Internal temperature in degrees Celsius.')
    
    # Relationships
    buoy = relationship("SailbuoyBuoy", foreign_keys=[buoy_id], back_populates="datalogger_data")
