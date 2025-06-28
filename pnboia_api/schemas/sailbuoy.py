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
    email_subject: Optional[str] = None
    email_datetime: Optional[datetime] = None
    sailbuoy_time: datetime = Field(..., description="Timestamp from the sailbuoy")
    
    # Location and basic telemetry
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude in decimal degrees")
    long: Optional[float] = Field(None, ge=-180, le=180, description="Longitude in decimal degrees")
    ttff: Optional[int] = Field(None, ge=0, description="Time to first fix in seconds")
    warning: Optional[int] = Field(None, description="Warning status")
    count: Optional[int] = Field(None, description="Message counter")
    
    # Power and environment
    i: Optional[float] = Field(None, description="Current in Amperes")
    v: Optional[float] = Field(None, description="Voltage in Volts")
    temperature: Optional[float] = Field(None, description="Internal temperature in °C")
    
    # Navigation
    velocity: Optional[float] = Field(None, ge=0, description="Speed over ground in m/s")
    heading: Optional[int] = Field(None, ge=0, le=359, description="Heading in degrees")
    winddirection: Optional[int] = Field(None, ge=0, le=359, description="Wind direction in degrees")

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

class AutopilotDataResponse(AutopilotDataInDB):
    """Response model for autopilot data."""
    pass

class DataloggerDataResponse(DataloggerDataInDB):
    """Response model for datalogger data."""
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
