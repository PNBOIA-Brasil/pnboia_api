# coding: utf-8
from sqlalchemy import Column, Computed, Date, DateTime, ForeignKey, Numeric, SmallInteger, String, Text
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Buoy(Base):
    __tablename__ = 'buoys'
    __table_args__ = {'schema': 'drift', 'comment': 'Tabela com as informações de todas as boias de DERIVA do programa PNBOIA/REMOBS.'}

    buoy_id = Column(SmallInteger, primary_key=True, comment='Id da boia.')
    hull_id = Column(ForeignKey('inventory.hull.hull_id', onupdate='CASCADE'), comment='Identificação do casco.')
    model = Column(String(30), nullable=False, comment='Modelo da boia.')
    latitude_deploy = Column(Numeric(6, 4), nullable=False, comment='Latitude do lançamento da boia.')
    longitude_deploy = Column(Numeric(6, 4), nullable=False, comment='Ponto de longitude do lançamento da boia.')
    deploy_date = Column(Date, nullable=False, comment='Data do lançamento da boia.')
    last_date_time = Column(DateTime, comment='Timestamp do último dado da boia.')
    last_latitude = Column(Numeric(6, 4))
    last_longitude = Column(Numeric(6, 4), comment='Última posição de longitude.')
    geom_deploy = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude_deploy)::double precision, (latitude_deploy)::double precision), 4326)', persisted=True))
    geom_last_position = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((last_longitude)::double precision, (last_latitude)::double precision), 4326)', persisted=True))
    project_id = Column(ForeignKey('institution.project.id'), comment='Id do projeto da boia')

    hull = relationship('Hull')
    project = relationship('Project')
