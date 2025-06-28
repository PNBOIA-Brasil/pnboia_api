# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text, text, Boolean, Float, Computed
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Use the existing Base from models/__init__.py
from . import Base

class SailbuoyMetadata(Base):
    """
    Table to store sailbuoy metadata information.
    """
    __tablename__ = 'metadata'
    __table_args__ = {'schema': 'sailbuoy', 'comment': 'Table containing sailbuoy metadata information.'}

    sailbuoy_id = Column(String(10), primary_key=True, comment='Sailbuoy identification ID (e.g., SB2432).')
    name = Column(String(30), nullable=False, comment='Component name (e.g., SB2432A for Autopilot, SB2432D for Datalogger).')
    imei = Column(String(15), nullable=False, comment='IMEI number of the sailbuoy component.')
    model = Column(String(30), comment='Model of the sailbuoy component.')
    deploy_date = Column(DateTime, comment='Date when the sailbuoy was deployed.')
    last_date_time = Column(DateTime, comment='Last recorded datetime from the sailbuoy.')
    is_active = Column(Boolean, default=True, comment='Whether the sailbuoy is currently active.')
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), comment='When this record was created.')
    updated_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'), 
                        comment='When this record was last updated.')

    # Relationships
    autopilot_data = relationship(
        "AutopilotData",
        back_populates="sailbuoy",
        foreign_keys="[AutopilotData.sailbuoy_id]"
    )
    datalogger_data = relationship(
        "DataloggerData",
        back_populates="sailbuoy",
        foreign_keys="[DataloggerData.sailbuoy_id]"
    )


class AutopilotData(Base):
    """
    Table to store navigation and control data from the sailbuoy's autopilot.
    """
    __tablename__ = 'autopilot_data'
    __table_args__ = {'schema': 'sailbuoy', 'comment': 'Navigation and control data from sailbuoy autopilot.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('sailbuoy.autopilot_data_id_seq'::regclass)"))
    email_subject = Column(Text, comment='Original email subject line')
    email_datetime = Column(DateTime(timezone=True), server_default=text('now()'), comment='When the email was received')
    sailbuoy_time = Column(DateTime, nullable=False, index=True, comment='Timestamp from the sailbuoy')
    
    # Location and basic telemetry
    lat = Column(Float, comment='Latitude in decimal degrees')
    long = Column(Float, comment='Longitude in decimal degrees')
    ttff = Column(Integer, comment='Time to first fix in seconds')
    warning = Column(Integer, comment='Warning status')
    count = Column(Integer, comment='Message counter')
    leak = Column(Integer, comment='Leak detection status')
    bigleak = Column(Integer, comment='Major leak detection status')
    commands = Column(Integer, comment='Command counter')
    
    # Power and environment
    i = Column(Float, comment='Current in Amperes')
    v = Column(Float, comment='Voltage in Volts')
    temperature = Column(Float, comment='Internal temperature in °C')
    pressure = Column(Float, comment='Atmospheric pressure')
    humidity = Column(Float, comment='Relative humidity in %')
    
    # Navigation
    transmissiontries = Column(Integer, comment='Number of transmission attempts')
    ontimesec = Column(Integer, comment='Uptime in seconds')
    velocity = Column(Float, comment='Speed over ground in m/s')
    heading = Column(Integer, comment='Heading in degrees (0-359)')
    trackdistance = Column(Integer, comment='Track distance')
    waypointdirection = Column(Integer, comment='Direction to waypoint')
    trackradius = Column(Integer, comment='Track radius')
    winddirection = Column(Integer, comment='Wind direction in degrees')
    
    # Autopilot status
    automodeenabled = Column(Integer, comment='Autopilot mode status')
    switchwaypointmodeenabled = Column(Integer, comment='Waypoint switching mode')
    nextautopilottack = Column(Integer, comment='Next autopilot tack')
    currenttack = Column(Integer, comment='Current tack')
    
    # Additional parameters
    t1 = Column(Integer, comment='T1 parameter')
    t2 = Column(Text, comment='T2 parameter')
    t3 = Column(Text, comment='T3 parameter')
    wpreached = Column(Integer, comment='Waypoint reached status')
    withintrackradius = Column(Integer, comment='Within track radius status')
    
    # Sail and rudder positions
    sailatportbow = Column(Integer, comment='Sail at port bow position')
    sailatport = Column(Integer, comment='Sail at port position')
    sailincentre = Column(Integer, comment='Sail in center position')
    sailatstarboard = Column(Integer, comment='Sail at starboard position')
    sailatstarboardbow = Column(Integer, comment='Sail at starboard bow position')
    
    # Navigation parameters
    wpdir = Column(Integer, comment='Waypoint direction')
    rang = Column(Integer, comment='Range')
    rcnt = Column(Integer, comment='Rudder count')
    cang = Column(Integer, comment='Course angle')
    tk_age = Column(Integer, comment='Track age')
    
    # Raw data
    raw_email_body = Column(Text, comment='Complete raw email body')
    
    # Foreign key to metadata
    sailbuoy_id = Column(String(10), ForeignKey('sailbuoy.metadata.sailbuoy_id'), nullable=False, comment='Reference to sailbuoy metadata')
    
    # Relationship to metadata
    sailbuoy = relationship(
        "SailbuoyMetadata",
        back_populates="autopilot_data",
        foreign_keys=[sailbuoy_id]
    )


class DataloggerData(Base):
    """
    Table to store scientific sensor data from the sailbuoy's datalogger.
    """
    __tablename__ = 'datalogger_data'
    __table_args__ = {'schema': 'sailbuoy', 'comment': 'Scientific sensor data from sailbuoy datalogger.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('sailbuoy.datalogger_data_id_seq'::regclass)"))
    email_subject = Column(Text, comment='Original email subject line')
    email_datetime = Column(DateTime(timezone=True), server_default=text('now()'), comment='When the email was received')
    sailbuoy_time = Column(DateTime, nullable=False, index=True, comment='Timestamp from the sailbuoy')
    
    # Location and basic telemetry
    lat = Column(Float, comment='Latitude in decimal degrees')
    long = Column(Float, comment='Longitude in decimal degrees')
    ttff = Column(Integer, comment='Time to first fix in seconds')
    count = Column(Integer, comment='Message counter')
    commands = Column(Integer, comment='Command counter')
    txtries = Column(Integer, comment='Transmission tries')
    ont = Column(Integer, comment='Ontime counter')
    diskused = Column(Integer, comment='Disk space used')
    
    # Power and environment
    i = Column(Float, comment='Current in Amperes')
    v = Column(Float, comment='Voltage in Volts')
    temperature = Column(Float, comment='Internal temperature in °C')
    
    # CTD (Conductivity, Temperature, Depth) data
    cttemp = Column(Float, comment='CTD temperature in °C')
    ctcond = Column(Float, comment='CTD conductivity')
    
    # Environmental sensors
    refined_fuel = Column(Float, comment='Refined fuel measurement')
    crudeoil = Column(Float, comment='Crude oil measurement')
    turbidity = Column(Float, comment='Turbidity measurement')
    
    # Additional sensors
    c3_temperature = Column(Float, comment='C3 temperature sensor')
    mose_onmin = Column(Float, comment='MOSE on minutes')
    
    # Wave data
    hs = Column(Float, comment='Significant wave height')
    ts = Column(Float, comment='Significant wave period')
    t0 = Column(Float, comment='Mean wave period')
    hmax = Column(Float, comment='Maximum wave height')
    
    # Error information
    err = Column(Text, comment='Error messages')
    
    # Weather data
    ft_winddir = Column(Float, comment='Wind direction from Fastrak sensor')
    ft_windspeed = Column(Float, comment='Wind speed from Fastrak sensor')
    ft_windgust = Column(Float, comment='Wind gust from Fastrak sensor')
    
    # Nortek current profiler data
    nortekstatus = Column(Integer, comment='Nortek status code')
    nortekvalidcells = Column(Integer, comment='Number of valid cells')
    nortekcells = Column(Integer, comment='Total number of cells')
    nortekonsec = Column(Integer, comment='Nortek on seconds')
    nortekspeed = Column(Float, comment='Current speed from Nortek')
    nortekdirection = Column(Float, comment='Current direction from Nortek')
    
    # Raw data
    raw_email_body = Column(Text, comment='Complete raw email body')
    
    # Foreign key to metadata
    sailbuoy_id = Column(String(10), ForeignKey('sailbuoy.metadata.sailbuoy_id'), nullable=False, comment='Reference to sailbuoy metadata')
    
    # Relationship to metadata
    sailbuoy = relationship(
        "SailbuoyMetadata",
        back_populates="datalogger_data",
        foreign_keys=[sailbuoy_id]
    )


class AutopilotDataSynoptic(AutopilotData):
    """Model for autopilot synoptic data view (00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00)"""
    __tablename__ = 'autopilot_data_synoptic'
    __table_args__ = {'schema': 'sailbuoy'}


class DataloggerDataSynoptic(DataloggerData):
    """Model for datalogger synoptic data view (00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00)"""
    __tablename__ = 'datalogger_data_synoptic'
    __table_args__ = {'schema': 'sailbuoy'}
