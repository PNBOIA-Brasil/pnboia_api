from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, Sequence
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.types import Date
from pnboia_api.db.base import Base

class Buoy(Base):
    __tablename__ = "buoys"

    id = Column(Integer, primary_key=True, index=True)
    name_buoy = Column(String(20), nullable=False)
    model = Column(String(20), nullable=False)
    lat = Column(Numeric(9,6), nullable=True)
    lon = Column(Numeric(9,6), nullable=True)
    depth = Column(Integer, nullable=True)
    deploy_date = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=False)
    wmo_number = Column(String(20), nullable=True)
    duration_wave = Column(Integer, nullable=True)
    h_sensor_pres = Column(Numeric, nullable=True)
    d_sensor_wtmp = Column(Numeric, nullable=True)
    wtmp_prec = Column(Numeric, nullable=True)
    wind_avg = Column(Numeric, nullable=True)
    h_sensor_wind = Column(Numeric, nullable=True)
    h_sensor_atmp = Column(Numeric, nullable=True)
    gust_avg = Column(Integer, nullable=True) 
    atmp_avg = Column(Integer, nullable=True)
    d_curr = Column(Numeric, nullable=True)
    h_sensor_wind_2 = Column(Numeric, nullable=True)
    data_buoys = relationship("DataBuoy", back_populates="buoy",uselist=False)
