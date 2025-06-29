from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement
from sqlalchemy.engine import Row

# Base schema with common configurations
class SailbuoyBase(BaseModel):
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            WKBElement: lambda v: to_shape(v).__geo_interface__ if v else None
        }
        arbitrary_types_allowed = True

# Sailbuoy Metadata Schemas
class SailbuoyMetadataBase(SailbuoyBase):
    """Base schema for sailbuoy metadata."""
    sailbuoy_id: str = Field(..., description="Sailbuoy identification ID (e.g., SB2432)")
    name: str = Field(..., description="Component name (e.g., SB2432A for Autopilot, SB2432D for Datalogger)")
    imei: str = Field(..., max_length=15, description="IMEI number of the sailbuoy component")
    model: Optional[str] = Field(None, max_length=30, description="Model of the sailbuoy component")
    deploy_date: Optional[datetime] = Field(None, description="Date when the sailbuoy was deployed")
    last_date_time: Optional[datetime] = Field(None, description="Last recorded datetime from the sailbuoy")
    is_active: bool = Field(True, description="Whether the sailbuoy is currently active")

    # Validator for name format
    @validator('name')
    def validate_name_format(cls, v):
        if not any(v.endswith(suffix) for suffix in ('A', 'D')):
            raise ValueError("Name must end with 'A' (Autopilot) or 'D' (Datalogger)")
        return v

class SailbuoyMetadataCreate(SailbuoyMetadataBase):
    """Schema for creating a new sailbuoy metadata entry."""
    pass

class SailbuoyMetadataUpdate(SailbuoyBase):
    """Schema for updating an existing sailbuoy metadata entry."""
    imei: Optional[str] = Field(None, max_length=15)
    model: Optional[str] = Field(None, max_length=30)
    deploy_date: Optional[datetime] = None
    last_date_time: Optional[datetime] = None
    is_active: Optional[bool] = None

class SailbuoyMetadataInDB(SailbuoyMetadataBase):
    """Schema for sailbuoy metadata as stored in the database."""
    created_at: datetime
    updated_at: datetime

    class Config(SailbuoyMetadataBase.Config):
        pass

# Autopilot Data Schemas
class AutopilotDataBase(SailbuoyBase):
    """Base schema for autopilot data."""
    email_subject: Optional[str] = Field(None, description="Email subject line from the sailbuoy")
    email_datetime: Optional[datetime] = Field(None, description="Timestamp when the email was received")
    sailbuoy_time: datetime = Field(..., description="Timestamp from the sailbuoy")
    
    # Location and basic telemetry
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude in decimal degrees")
    long: Optional[float] = Field(None, ge=-180, le=180, description="Longitude in decimal degrees")
    ttff: Optional[int] = Field(None, ge=0, description="Time to first fix in seconds")
    warning: Optional[int] = Field(None, description="Warning status")
    count: Optional[int] = Field(None, description="Message counter")
    leak: Optional[int] = Field(None, description="Leak detection status")
    bigleak: Optional[int] = Field(None, description="Major leak detection status")
    commands: Optional[int] = Field(None, description="Command status")
    
    # Power and environment
    i: Optional[float] = Field(None, description="Current in Amperes")
    v: Optional[float] = Field(None, description="Voltage in Volts")
    temperature: Optional[float] = Field(None, description="Internal temperature in °C")
    pressure: Optional[float] = Field(None, description="Atmospheric pressure in hPa")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Relative humidity in %")
    
    # System status
    transmissiontries: Optional[int] = Field(None, ge=0, description="Number of transmission attempts")
    ontimesec: Optional[int] = Field(None, ge=0, description="Uptime in seconds")
    
    # Navigation
    velocity: Optional[float] = Field(None, ge=0, description="Speed over ground in m/s")
    heading: Optional[int] = Field(None, ge=0, le=359, description="Heading in degrees")
    trackdistance: Optional[int] = Field(None, description="Distance to track in meters")
    waypointdirection: Optional[int] = Field(None, ge=0, le=359, description="Direction to waypoint in degrees")
    trackradius: Optional[int] = Field(None, description="Track radius in meters")
    winddirection: Optional[int] = Field(None, ge=0, description="Wind direction in degrees (will be normalized to 0-359)")
    
    # Autopilot settings
    automodeenabled: Optional[int] = Field(None, description="Auto mode status")
    switchwaypointmodeenabled: Optional[int] = Field(None, description="Waypoint switching mode status")
    nextautopilottack: Optional[int] = Field(None, description="Next tack direction")
    currenttack: Optional[int] = Field(None, description="Current tack direction")
    
    # Additional telemetry
    t1: Optional[int] = Field(None, description="Telemetry field 1")
    t2: Optional[str] = Field(None, description="Telemetry field 2")
    t3: Optional[str] = Field(None, description="Telemetry field 3")
    
    # Navigation status
    wpreached: Optional[int] = Field(None, description="Waypoint reached status")
    withintrackradius: Optional[int] = Field(None, description="Within track radius status")
    sailatportbow: Optional[int] = Field(None, description="Sail at port bow status")
    sailatport: Optional[int] = Field(None, description="Sail at port status")
    sailincentre: Optional[int] = Field(None, description="Sail in center status")
    sailatstarboard: Optional[int] = Field(None, description="Sail at starboard status")
    sailatstarboardbow: Optional[int] = Field(None, description="Sail at starboard bow status")
    
    # Additional navigation
    wpdir: Optional[int] = Field(None, ge=0, le=359, description="Waypoint direction in degrees")
    rang: Optional[int] = Field(None, description="Range to waypoint in meters")
    rcnt: Optional[int] = Field(None, description="Message counter")
    cang: Optional[int] = Field(None, description="Course and ground track angle")
    tk_age: Optional[int] = Field(None, description="Track age in seconds")
    raw_email_body: Optional[str] = Field(None, description="Raw email body content")
    
    # Validator to handle wind direction values > 359
    @validator('winddirection', 'heading', 'waypointdirection', 'wpdir')
    def normalize_degrees(cls, v):
        if v is not None and isinstance(v, (int, float)):
            return int(v) % 360
        return v

class AutopilotDataCreate(AutopilotDataBase):
    """Schema for creating new autopilot data."""
    sailbuoy_id: str
    name: str  # Component name (e.g., SB2432A)

class AutopilotDataUpdate(SailbuoyBase):
    """Schema for updating autopilot data."""
    # Only include fields that should be updatable
    warning: Optional[int] = None
    count: Optional[int] = None
    i: Optional[float] = None
    v: Optional[float] = None
    temperature: Optional[float] = None
    velocity: Optional[float] = None
    heading: Optional[int] = None
    winddirection: Optional[int] = None

class AutopilotDataInDB(AutopilotDataBase):
    """Schema for autopilot data as stored in the database."""
    id: int
    sailbuoy_id: str
    name: str
    email_datetime: datetime
    
    class Config(SailbuoyBase.Config):
        pass

# Datalogger Data Schemas
class DataloggerDataBase(SailbuoyBase):
    """Base schema for datalogger data."""
    email_subject: Optional[str] = None
    email_datetime: Optional[datetime] = None
    sailbuoy_time: datetime = Field(..., description="Timestamp from the sailbuoy")
    
    # Location and basic telemetry
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude in decimal degrees")
    long: Optional[float] = Field(None, ge=-180, le=180, description="Longitude in decimal degrees")
    ttff: Optional[int] = Field(None, ge=0, description="Time to first fix in seconds")
    
    # CTD data
    cttemp: Optional[float] = Field(None, description="CTD temperature in °C")
    ctcond: Optional[float] = Field(None, description="CTD conductivity")
    
    # Wave data
    hs: Optional[float] = Field(None, ge=0, description="Significant wave height")
    ts: Optional[float] = Field(None, ge=0, description="Significant wave period")
    
    # Weather data
    ft_winddir: Optional[float] = Field(None, ge=0, le=360, description="Wind direction from Fastrak sensor")
    ft_windspeed: Optional[float] = Field(None, ge=0, description="Wind speed from Fastrak sensor")

class DataloggerDataCreate(DataloggerDataBase):
    """Schema for creating new datalogger data."""
    sailbuoy_id: str
    name: str  # Component name (e.g., SB2432D)

class DataloggerDataUpdate(SailbuoyBase):
    """Schema for updating datalogger data."""
    # Only include fields that should be updatable
    cttemp: Optional[float] = None
    ctcond: Optional[float] = None
    hs: Optional[float] = None
    ts: Optional[float] = None
    ft_winddir: Optional[float] = None
    ft_windspeed: Optional[float] = None

class DataloggerDataInDB(DataloggerDataBase):
    """Schema for datalogger data as stored in the database."""
    id: int
    sailbuoy_id: str
    name: str
    email_datetime: datetime
    
    class Config(SailbuoyBase.Config):
        pass

# Response models for API endpoints
class SailbuoyMetadataResponse(SailbuoyMetadataInDB):
    """Response model for sailbuoy metadata."""
    pass

# New response models that match our database schema
class AutopilotDataSynopticResponse(SailbuoyBase):
    """Response model for synoptic autopilot data."""
    id: int
    sailbuoy_time: datetime = Field(..., description="Timestamp from the sailbuoy")
    
    # Location and basic telemetry
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude in decimal degrees")
    long: Optional[float] = Field(None, ge=-180, le=180, description="Longitude in decimal degrees")
    ttff: Optional[int] = Field(None, ge=0, description="Time to first fix in seconds")
    warning: Optional[int] = Field(None, description="Warning status")
    count: Optional[int] = Field(None, description="Message counter")
    leak: Optional[int] = Field(None, description="Leak detection status")
    bigleak: Optional[int] = Field(None, description="Major leak detection status")
    commands: Optional[int] = Field(None, description="Command status")
    
    # Power and environment
    i: Optional[float] = Field(None, description="Current in Amperes")
    v: Optional[float] = Field(None, description="Voltage in Volts")
    temperature: Optional[float] = Field(None, description="Internal temperature in °C")
    pressure: Optional[float] = Field(None, description="Atmospheric pressure in hPa")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Relative humidity in %")
    
    # System status
    transmissiontries: Optional[int] = Field(None, ge=0, description="Number of transmission attempts")
    ontimesec: Optional[int] = Field(None, ge=0, description="Uptime in seconds")
    
    # Navigation
    velocity: Optional[float] = Field(None, ge=0, description="Speed over ground in m/s")
    heading: Optional[int] = Field(None, ge=0, le=359, description="Heading in degrees")
    trackdistance: Optional[int] = Field(None, description="Distance to track in meters")
    waypointdirection: Optional[int] = Field(None, ge=0, le=359, description="Direction to waypoint in degrees")
    trackradius: Optional[int] = Field(None, description="Track radius in meters")
    winddirection: Optional[int] = Field(None, ge=0, description="Wind direction in degrees")
    
    # Autopilot settings
    automodeenabled: Optional[int] = Field(None, description="Auto mode status")
    switchwaypointmodeenabled: Optional[int] = Field(None, description="Waypoint switching mode status")
    nextautopilottack: Optional[int] = Field(None, description="Next tack direction")
    currenttack: Optional[int] = Field(None, description="Current tack direction")
    
    # Additional telemetry
    t1: Optional[int] = Field(None, description="Telemetry field 1")
    t2: Optional[str] = Field(None, description="Telemetry field 2")
    t3: Optional[str] = Field(None, description="Telemetry field 3")
    
    # Navigation status
    wpreached: Optional[int] = Field(None, description="Waypoint reached status")
    withintrackradius: Optional[int] = Field(None, description="Within track radius status")
    sailatportbow: Optional[int] = Field(None, description="Sail at port bow status")
    sailatport: Optional[int] = Field(None, description="Sail at port status")
    sailincentre: Optional[int] = Field(None, description="Sail in center status")
    sailatstarboard: Optional[int] = Field(None, description="Sail at starboard status")
    sailatstarboardbow: Optional[int] = Field(None, description="Sail at starboard bow status")
    
    # Additional navigation
    wpdir: Optional[int] = Field(None, ge=0, le=359, description="Waypoint direction in degrees")
    rang: Optional[int] = Field(None, description="Range to waypoint in meters")
    rcnt: Optional[int] = Field(None, description="Message counter")
    cang: Optional[int] = Field(None, description="Course and ground track angle")
    tk_age: Optional[int] = Field(None, description="Track age in seconds")
    
    class Config(SailbuoyBase.Config):
        pass

class DataloggerDataSynopticResponse(SailbuoyBase):
    """Response model for synoptic datalogger data."""
    id: int
    sailbuoy_time: datetime = Field(..., description="Timestamp from the sailbuoy")
    
    # Location and basic telemetry
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude in decimal degrees")
    long: Optional[float] = Field(None, ge=-180, le=180, description="Longitude in decimal degrees")
    ttff: Optional[int] = Field(None, ge=0, description="Time to first fix in seconds")
    
    # System status
    count: Optional[int] = Field(None, description="Message counter")
    commands: Optional[int] = Field(None, description="Command status")
    txtries: Optional[int] = Field(None, description="Transmission attempts count")
    ont: Optional[int] = Field(None, description="On time in minutes")
    diskused: Optional[int] = Field(None, description="Disk space used in bytes")
    
    # Power and environment
    i: Optional[float] = Field(None, description="Current in Amperes")
    v: Optional[float] = Field(None, description="Voltage in Volts")
    temperature: Optional[float] = Field(None, description="Internal temperature in °C")
    
    # CTD data
    cttemp: Optional[float] = Field(None, description="CTD temperature in °C")
    ctcond: Optional[float] = Field(None, description="CTD conductivity")
    
    # Environmental measurements
    refined_fuel: Optional[float] = Field(None, description="Refined fuel measurement")
    crudeoil: Optional[float] = Field(None, description="Crude oil measurement")
    turbidity: Optional[float] = Field(None, description="Turbidity measurement")
    c3_temperature: Optional[float] = Field(None, description="C3 temperature")
    mose_onmin: Optional[float] = Field(None, description="MOSE on minutes")
    
    # Wave data
    hs: Optional[float] = Field(None, ge=0, description="Significant wave height")
    ts: Optional[float] = Field(None, ge=0, description="Significant wave period")
    t0: Optional[float] = Field(None, description="Wave period")
    hmax: Optional[float] = Field(None, description="Maximum wave height")
    
    # Weather data
    ft_winddir: Optional[float] = Field(None, ge=0, le=360, description="Wind direction from Fastrak sensor")
    ft_windspeed: Optional[float] = Field(None, ge=0, description="Wind speed from Fastrak sensor")
    ft_windgust: Optional[float] = Field(None, ge=0, description="Wind gust speed from Fastrak sensor")
    
    # Nortek current profiler data
    nortekstatus: Optional[int] = Field(None, description="Nortek status code")
    nortekvalidcells: Optional[int] = Field(None, description="Number of valid cells from Nortek")
    nortekcells: Optional[int] = Field(None, description="Total number of cells from Nortek")
    nortekonsec: Optional[int] = Field(None, description="Nortek sensor on time in seconds")
    nortekspeed: Optional[float] = Field(None, description="Current speed from Nortek sensor in m/s")
    nortekdirection: Optional[float] = Field(None, ge=0, le=360, description="Current direction from Nortek sensor in degrees")
    
    class Config(SailbuoyBase.Config):
        pass

class AutopilotDataResponse(SailbuoyBase):
    """Response model for autopilot data."""
    id: int
    sailbuoy_time: datetime = Field(..., description="Timestamp from the sailbuoy")
    
    # Location and basic telemetry
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude in decimal degrees")
    long: Optional[float] = Field(None, ge=-180, le=180, description="Longitude in decimal degrees")
    ttff: Optional[int] = Field(None, ge=0, description="Time to first fix in seconds")
    warning: Optional[int] = Field(None, description="Warning status")
    count: Optional[int] = Field(None, description="Message counter")
    leak: Optional[int] = Field(None, description="Leak detection status")
    bigleak: Optional[int] = Field(None, description="Major leak detection status")
    commands: Optional[int] = Field(None, description="Command status")
    
    # Power and environment
    i: Optional[float] = Field(None, description="Current in Amperes")
    v: Optional[float] = Field(None, description="Voltage in Volts")
    temperature: Optional[float] = Field(None, description="Internal temperature in °C")
    pressure: Optional[float] = Field(None, description="Atmospheric pressure in hPa")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Relative humidity in %")
    
    # System status
    transmissiontries: Optional[int] = Field(None, ge=0, description="Number of transmission attempts")
    ontimesec: Optional[int] = Field(None, ge=0, description="Uptime in seconds")
    
    # Navigation
    velocity: Optional[float] = Field(None, ge=0, description="Speed over ground in m/s")
    heading: Optional[int] = Field(None, ge=0, le=359, description="Heading in degrees")
    trackdistance: Optional[int] = Field(None, description="Distance to track in meters")
    waypointdirection: Optional[int] = Field(None, ge=0, le=359, description="Direction to waypoint in degrees")
    trackradius: Optional[int] = Field(None, description="Track radius in meters")
    winddirection: Optional[int] = Field(None, ge=0, description="Wind direction in degrees")
    
    # Autopilot settings
    automodeenabled: Optional[int] = Field(None, description="Auto mode status")
    switchwaypointmodeenabled: Optional[int] = Field(None, description="Waypoint switching mode status")
    nextautopilottack: Optional[int] = Field(None, description="Next tack direction")
    currenttack: Optional[int] = Field(None, description="Current tack direction")
    
    # Additional telemetry
    t1: Optional[int] = Field(None, description="Telemetry field 1")
    t2: Optional[str] = Field(None, description="Telemetry field 2")
    t3: Optional[str] = Field(None, description="Telemetry field 3")
    
    # Navigation status
    wpreached: Optional[int] = Field(None, description="Waypoint reached status")
    withintrackradius: Optional[int] = Field(None, description="Within track radius status")
    sailatportbow: Optional[int] = Field(None, description="Sail at port bow status")
    sailatport: Optional[int] = Field(None, description="Sail at port status")
    sailincentre: Optional[int] = Field(None, description="Sail in center status")
    sailatstarboard: Optional[int] = Field(None, description="Sail at starboard status")
    sailatstarboardbow: Optional[int] = Field(None, description="Sail at starboard bow status")
    
    # Additional navigation
    wpdir: Optional[int] = Field(None, ge=0, le=359, description="Waypoint direction in degrees")
    rang: Optional[int] = Field(None, description="Range to waypoint in meters")
    rcnt: Optional[int] = Field(None, description="Message counter")
    cang: Optional[int] = Field(None, description="Course and ground track angle")
    tk_age: Optional[int] = Field(None, description="Track age in seconds")
    
    class Config(SailbuoyBase.Config):
        pass

class DataloggerDataResponse(SailbuoyBase):
    """Response model for datalogger data."""
    id: int
    sailbuoy_time: datetime = Field(..., description="Timestamp from the sailbuoy")
    
    # Location and basic telemetry
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude in decimal degrees")
    long: Optional[float] = Field(None, ge=-180, le=180, description="Longitude in decimal degrees")
    ttff: Optional[int] = Field(None, ge=0, description="Time to first fix in seconds")
    
    # System status
    count: Optional[int] = Field(None, description="Message counter")
    commands: Optional[int] = Field(None, description="Command status")
    txtries: Optional[int] = Field(None, description="Transmission attempts count")
    ont: Optional[int] = Field(None, description="On time in minutes")
    diskused: Optional[int] = Field(None, description="Disk space used in bytes")
    
    # Power and environment
    i: Optional[float] = Field(None, description="Current in Amperes")
    v: Optional[float] = Field(None, description="Voltage in Volts")
    temperature: Optional[float] = Field(None, description="Internal temperature in °C")
    
    # CTD data
    cttemp: Optional[float] = Field(None, description="CTD temperature in °C")
    ctcond: Optional[float] = Field(None, description="CTD conductivity")
    
    # Environmental data
    refined_fuel: Optional[float] = Field(None, description="Refined fuel measurement")
    crudeoil: Optional[float] = Field(None, description="Crude oil measurement")
    turbidity: Optional[float] = Field(None, description="Water turbidity measurement")
    c3_temperature: Optional[float] = Field(None, description="C3 sensor temperature")
    
    # Wave data
    hs: Optional[float] = Field(None, ge=0, description="Significant wave height in meters")
    ts: Optional[float] = Field(None, ge=0, description="Significant wave period in seconds")
    t0: Optional[float] = Field(None, description="Zero-upcrossing wave period")
    hmax: Optional[float] = Field(None, description="Maximum wave height in meters")
    
    # Wind data
    ft_winddir: Optional[float] = Field(None, ge=0, le=360, description="Wind direction from Fastrak sensor in degrees")
    ft_windspeed: Optional[float] = Field(None, ge=0, description="Wind speed from Fastrak sensor in m/s")
    ft_windgust: Optional[float] = Field(None, ge=0, description="Wind gust speed from Fastrak sensor in m/s")
    
    # Error information
    err: Optional[str] = Field(None, description="Error message if any")
    
    # Nortek sensor data
    nortekstatus: Optional[int] = Field(None, description="Nortek sensor status code")
    nortekvalidcells: Optional[int] = Field(None, description="Number of valid cells from Nortek")
    nortekcells: Optional[int] = Field(None, description="Total number of cells from Nortek")
    nortekonsec: Optional[int] = Field(None, description="Nortek sensor on time in seconds")
    nortekspeed: Optional[float] = Field(None, description="Current speed from Nortek sensor in m/s")
    nortekdirection: Optional[float] = Field(None, ge=0, le=360, description="Current direction from Nortek sensor in degrees")
    
    class Config(SailbuoyBase.Config):
        pass

class PaginatedResponse(BaseModel):
    """Generic paginated response model."""
    total: int
    page: int
    page_size: int
    items: List[Any]

# Example usage in type hints:
# class PaginatedSailbuoyMetadata(PaginatedResponse):
#     items: List[SailbuoyMetadataResponse]

# class PaginatedAutopilotData(PaginatedResponse):
#     items: List[AutopilotDataResponse]

# class PaginatedDataloggerData(PaginatedResponse):
#     items: List[DataloggerDataResponse]
