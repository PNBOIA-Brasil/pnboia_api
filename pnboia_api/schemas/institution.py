# coding: utf-8
from sqlalchemy import Column, SmallInteger, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Project(Base):
    __tablename__ = 'project'
    __table_args__ = {'schema': 'institution', 'comment': 'Schema contendo informações dos projetos e instituições parceiras do CHM e PNBOIA.'}

    id = Column(SmallInteger, primary_key=True, comment='Identificação do projeto')
    project = Column(String(50), comment='Nome do projeto.')
    manager = Column(String(50), comment='Gerente ou responsável pelo projeto.')
    institution = Column(String(100), comment='Instituição à qual pertence o projeto.')
    observation = Column(Text, comment='Observações importantes sobre o projeto e/ou dados.')
