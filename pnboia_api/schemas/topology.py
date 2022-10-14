# coding: utf-8
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Topology(Base):
    __tablename__ = 'topology'
    __table_args__ = {'schema': 'topology'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('topology.topology_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)
    srid = Column(Integer, nullable=False)
    precision = Column(Float(53), nullable=False)
    hasz = Column(Boolean, nullable=False, server_default=text("false"))


class Layer(Base):
    __tablename__ = 'layer'
    __table_args__ = (
        UniqueConstraint('schema_name', 'table_name', 'feature_column'),
        {'schema': 'topology'}
    )

    topology_id = Column(ForeignKey('topology.topology.id'), primary_key=True, nullable=False)
    layer_id = Column(Integer, primary_key=True, nullable=False)
    schema_name = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    feature_column = Column(String, nullable=False)
    feature_type = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False, server_default=text("0"))
    child_id = Column(Integer)

    topology = relationship('Topology')
