# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, MetaData, Numeric, SmallInteger, String, Table, Text
from geoalchemy2.types import Geometry

metadata = MetaData()

t_boias = Table(
    'boias', metadata,
    Column('nome', String(30)),
    Column('data_lancamento', Date),
    Column('ultimo_dado', DateTime),
    Column('latitude', Numeric(6, 4)),
    Column('longitude', Numeric(6, 4)),
    Column('geom', Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry')),
    Column('ativa', Boolean),
    Column('link_site', Text),
    Column('secao_metarea', String(10)),
    schema='idem_dhn'
)


t_boias_ativas = Table(
    'boias_ativas', metadata,
    Column('nome', String(30)),
    Column('modelo_boia', Text),
    Column('data_lancamento', Date),
    Column('ultimo_dado', DateTime),
    Column('latitude', Numeric(6, 4)),
    Column('longitude', Numeric(6, 4)),
    Column('geom', Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry')),
    Column('ativa', Boolean),
    Column('link_site', Text),
    Column('secao_metarea', String(10)),
    Column('umidade_relativa', Numeric),
    Column('vel_vento_1', Numeric(4, 2)),
    Column('dir_vento_1', SmallInteger),
    Column('rajada_vento1', Numeric),
    Column('vel_vento2', Numeric),
    Column('temp_ar', Numeric),
    Column('pto_orvalho', Numeric),
    Column('pressao_atm', Numeric),
    Column('radiacao_solar', Numeric),
    Column('tsm', Numeric(4, 2)),
    Column('vel_corrente1', Numeric),
    Column('dir_corrente1', SmallInteger),
    Column('vel_corrente2', Numeric),
    Column('dir_corrente2', SmallInteger),
    Column('vel_corrente3', Numeric),
    Column('dir_corrente3', SmallInteger),
    Column('hs_1', Numeric(4, 2)),
    Column('tp_1', Numeric(4, 2)),
    Column('dir_onda1', SmallInteger),
    Column('hmax1', Numeric),
    Column('dir_espalhamento_onda1', SmallInteger),
    Column('hs_2', Numeric),
    Column('tp_2', Numeric),
    Column('dir_onda2', SmallInteger),
    schema='idem_dhn'
)


t_dados_boias_inativas = Table(
    'dados_boias_inativas', metadata,
    Column('nome', String(30)),
    Column('modelo_boia', String(30)),
    Column('data_lancamento', Date),
    Column('ultimo_dado', DateTime),
    Column('latitude', Numeric(6, 4)),
    Column('longitude', Numeric(6, 4)),
    Column('geom', Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry')),
    Column('ativa', Boolean),
    Column('link_site', Text),
    Column('secao_metarea', String(10)),
    schema='idem_dhn'
)
