# coding: utf-8
from sqlalchemy import Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pnboia_api.models.moored import *

Base = declarative_base()
metadata = Base.metadata

class General(Base):
    __tablename__ = 'general'
    __table_args__ = {'schema': 'quality_control'}

    id = Column(SmallInteger, primary_key=True, comment='Id da boia.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), comment='ID da boia')
    qc_config = Column(JSON)

    buoy = relationship(Buoy, foreign_keys=[buoy_id])
