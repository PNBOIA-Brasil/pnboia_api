# coding: utf-8
from pydantic import BaseModel, HttpUrl, validator, Json
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

class QualityControlBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    qc_config: Optional[dict]

    class Config:
        orm_mode = True