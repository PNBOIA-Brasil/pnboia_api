# coding: utf-8
from sqlalchemy import Column, Computed, Date, DateTime, ForeignKey, Numeric, SmallInteger, String, Text
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class BuoyDrift(Base):
    __tablename__ = 'buoys'
    __table_args__ = {'schema': 'drift', 'comment': 'Tabela com as informações de todas as boias de DERIVA do programa PNBOIA/REMOBS.'}

    buoy_id = Column(SmallInteger, primary_key=True, comment='Id da boia.')
    hull_id = Column(SmallInteger, comment='Identificação do casco.')
    model = Column(String(30), nullable=False, comment='Modelo da boia.')
    latitude_deploy = Column(Numeric(10, 4), nullable=False, comment='Latitude do lançamento da boia.')
    longitude_deploy = Column(Numeric(10, 4), nullable=False, comment='Ponto de longitude do lançamento da boia.')
    deploy_date = Column(Date, nullable=False, comment='Data do lançamento da boia.')
    last_date_time = Column(DateTime, comment='Timestamp do último dado da boia.')
    last_latitude = Column(Numeric(10, 4))
    last_longitude = Column(Numeric(10, 4), comment='Última posição de longitude.')
    geom_deploy = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude_deploy)::double precision, (latitude_deploy)::double precision), 4326)', persisted=True))
    geom_last_position = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((last_longitude)::double precision, (last_latitude)::double precision), 4326)', persisted=True))
    project_id = Column(SmallInteger, comment='Id do projeto da boia')
    antenna_id = Column(String(30), nullable=False)

class SpotterGeneralDrift(Base):
    __tablename__ = 'spotter_general'
    __table_args__ = {'schema': 'drift', 'comment': 'Tabela com as informações de todas as boias de DERIVA do programa PNBOIA/REMOBS.'}

    id = Column(SmallInteger, primary_key=True, comment='Id da boia.')
    buoy_id = Column(ForeignKey(BuoyDrift.buoy_id, onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    wspd1 = Column(Numeric)
    wdir1 = Column(Numeric)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado. Dado retirado da string e transformado em TIMESTAMP horário ZULU.')
    swvht1 = Column(Numeric)
    tp1 = Column(Numeric)
    tm1 = Column(Numeric)
    pkdir1 = Column(Numeric)
    pkspread1 = Column(Numeric)
    wvdir1 = Column(Numeric)
    wvspread1 = Column(Numeric)
    sst = Column(Numeric)

    
    buoy = relationship(BuoyDrift, foreign_keys=[buoy_id])


class SpotterSystemDrift(Base):
    __tablename__ = 'spotter_system'
    __table_args__ = {'schema': 'drift', 'comment': 'Tabela com as informações de todas as boias de DERIVA do programa PNBOIA/REMOBS.'}


    id = Column(SmallInteger, primary_key=True, comment='Id da boia.')
    buoy_id = Column(ForeignKey(BuoyDrift.buoy_id, onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado. Dado retirado da string e transformado em TIMESTAMP horário ZULU.')
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    battery_power = Column(Numeric)
    battery_voltage = Column(Numeric)
    humidity = Column(Numeric)
    solar_voltage = Column(Numeric)

    buoy = relationship(BuoyDrift, foreign_keys=[buoy_id])

class SpotterWavesDrift(Base):
    __tablename__ = 'spotter_waves'
    __table_args__ = {'schema': 'drift', 'comment': 'Tabela com as informações de todas as boias de DERIVA do programa PNBOIA/REMOBS.'}

    id = Column(SmallInteger, primary_key=True, comment='Id da boia.')
    buoy_id = Column(ForeignKey(BuoyDrift.buoy_id, onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado. Dado retirado da string e transformado em TIMESTAMP horário ZULU.')
    frequency = Column(Text)
    df = Column(Text)
    a1 = Column(Text)
    b1 = Column(Text)
    a2 = Column(Text)
    b2 = Column(Text)
    varianceDensity = Column(Text)
    direction = Column(Text)
    directionalSpread = Column(Text)
    latitude = Column(Numeric)
    longitude = Column(Numeric)

    buoy = relationship(BuoyDrift, foreign_keys=[buoy_id])
