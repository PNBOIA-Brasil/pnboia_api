# coding: utf-8
from sqlalchemy import ARRAY, Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, JSON, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Metocean(Base):
    __tablename__ = 'metocean'
    __table_args__ = {'schema': 'quality_control', 'comment': 'Tabela com todos os parâmetros usados no Controle de Qualidade. Os parâmetros variam desde o instrumento/sensor utilzado à região em que a boia está fundeada.'}

    id = Column(SmallInteger, primary_key=True, server_default=text("nextval('quality_control.metocean_id_seq'::regclass)"))
    buoy_id = Column(SmallInteger, comment='ID da boia.')
    interval_hours = Column(SmallInteger, comment='Intervalo de horas usado para qualificar os dados brutos. Por exemplo, se interval_hours = 72, as últimas 72 horas de dados serão usadas para fazer a qualificação.')
    continuity_limit = Column(SmallInteger, comment='Limite de continuidade. Número de dados usados para verificar a consistência dos dados no tempo. Verifica se a variação temporal está dentro de um intervalo aceitável.')
    stuck_limit = Column(SmallInteger, comment='Stuck Limit - Limite Preso. Número de dados usados para verificar se o sensor está "preso" em um mesmo valor, indicando algum erro na decodificação ou no próprio sensor.')
    outlier_limits_rh = Column(ARRAY(SmallInteger()), comment='Limites mínimo e máximo para Relative Humidity - Umidade Relativa.')
    outlier_limits_atmp = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Air Temperature - Temperatura do Ar.')
    outlier_limits_srad = Column(ARRAY(Numeric()), comment='Limites mínimos e máximos para o Solar Radiation - Radiação Solar.')
    outlier_limits_wspd1 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Wind Speed 1 - Intensidade do Vento, Anemomêtro 1.')
    outlier_limits_wspd2 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Wind Speed 2 - Intensidade do Vento, Anemomêtro 2.')
    outlier_limits_gust1 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Gust 1 - Rajada de Vento, Anemomêtro 1.')
    outlier_limits_gust2 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Gust 2 - Rajada de Vento, Anemomêtro 2.')
    outlier_limits_pres = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para o Atmospheric Pressure - Pressão Atmosféria.')
    outlier_limits_dewpt = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Dew Point - Ponto de Orvalho.')
    outlier_limits_sst = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Sea Surface Temperature - Temperatura da Superfície do Mar, em graus Celsius.')
    outlier_limits_swvht1 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Sea Wave Height 1 - Altura Significativa de Onda, Ondógrafo 1.')
    outlier_limits_mxwvht1 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Maximum Wave Height 1 - Altura Máxima de Onda, Ondógrafo 1.')
    outlier_limits_tp1 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Peak Period 1 - Período de Pico, Ondógrafo 1.')
    outlier_limits_swvht2 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Sea Wave Height 2 - Altura Significativa de Onda, Ondógrafo 2.')
    outlier_limits_tp2 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Peak Period 2 - Período de Pico, Ondógrafo 2.')
    outlier_limits_cspd1 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Current Speed 1 - Velocidade de corrente, nível 1.')
    outlier_limits_cspd2 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Current Speed 2 - Velocidade de corrente, nível 2.')
    outlier_limits_cspd3 = Column(ARRAY(Numeric()), comment='Limites mínimo e máximo para Current Speed 3 - Velocidade de corrente, nível 3.')


class SensorsLimit(Base):
    __tablename__ = 'sensors_limits'
    __table_args__ = {'schema': 'quality_control', 'comment': 'Tabela com os limites de medição dos sensores.'}

    id = Column(SmallInteger, primary_key=True, server_default=text("nextval('quality_control.sensors_limits_id_seq'::regclass)"), comment='Id do registro.')
    model = Column(String(40), unique=True, comment='Modelo do sensor.')
    limits = Column(JSON, comment='Limites de medição do sensor.')


class SensorsLimitsSpotter(Base):
    __tablename__ = 'sensors_limits_spotter'
    __table_args__ = {'schema': 'quality_control', 'comment': 'Limites de medição para as variáveis da boia do tipo Spotter V2.'}

    id = Column(SmallInteger, primary_key=True, server_default=text("nextval('quality_control.sensors_limits_spotter_id_seq'::regclass)"))
    model = Column(String(20), comment='Modelo da Spotter (Spotter V2, Spotter V3, ...)')
    sst = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo do sensor de SST (TSM).')
    wspd = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo para o valor de WSPD (calculado).')
    wdir = Column(ARRAY(SmallInteger()), comment='Limites mínimo e máximo para o WDIR (calculado)')
    swvht = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo para o sensor de ondas, variável SWVHT (Altura significativa).')
    tp = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo para TP (Período de Pico).')
    tm = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo para TM (Período Médio).')
    wvdir = Column(ARRAY(SmallInteger()), comment='Limites mínimo e máximo para WVDIR.')
    pkspread = Column(ARRAY(SmallInteger()), comment='Limites mínimo e máximo para PKSPREAD.')
    wvspread = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo para WVSPREAD.')



class Buoy(Base):
    __tablename__ = 'buoys'
    __table_args__ = {'schema': 'quality_control', 'comment': 'Configuração dos testes do controle de qualidade.'}

    id = Column(SmallInteger, primary_key=True, server_default=text("nextval('quality_control.buoys_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), nullable=False, unique=True, comment='ID da boia.')
    continuity_test = Column(Boolean, comment='Teste de continuidade.')
    stuck_sensor_test = Column(Boolean, comment='Teste de stuck_sensor.')
    climatological_test = Column(Boolean, comment='Teste de limites climatológicos.')
    outlier_test = Column(Boolean, comment='Teste de outlier')
    sensor_limits_test = Column(Boolean, comment='Teste de limites de sensores')

    buoy = relationship('Buoy', uselist=False, remote_side=[id])


class Spotter(Base):
    __tablename__ = 'spotter'
    __table_args__ = {'schema': 'quality_control', 'comment': 'Parâmetros de QC para as boias do tipo Spotter'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('quality_control.spotter_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('quality_control.buoys.buoy_id', onupdate='CASCADE'), comment='ID da boia de configuração')
    interval_hours = Column(SmallInteger, comment='Intervalo de horas usado para qualificar os dados brutos. Por exemplo, se interval_hours = 72, as últimas 72 horas de dados serão usadas para fazer a qualificação.')
    stuck_limit = Column(SmallInteger, comment='Stuck Limit - Limite Preso. Número de dados usados para verificar se o sensor está "preso" em um mesmo valor, indicando algum erro na decodificação ou no próprio sensor.')
    continuity_limit = Column(SmallInteger, comment='Limite de continuidade. Número de dados usados para verificar a consistência dos dados no tempo. Verifica se a variação temporal está dentro de um intervalo aceitável.')
    outlier_limits_wspd = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimos e máximo de OUTLIER para a variável WSPD. (Velocidade do Vento)')
    outlier_limits_wdir = Column(ARRAY(SmallInteger()), comment='Limites mínimo e máximo de OUTLIER para WDIR (Direção de Vento).')
    outlier_limits_sst = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo de OUTLIER para SST.')
    outlier_limits_swvht = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo de OUTLIER para SWVHT (Altura Significativa de Onda, Hs).')
    outlier_limits_tp = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo de OUTLIER para TP (Período de Pico)')
    outlier_limits_tm = Column(ARRAY(Numeric(precision=4, scale=2)), comment='Limites mínimo e máximo de OUTLIER para TM (Período Médio)')
    outlier_limits_wvdir = Column(ARRAY(SmallInteger()), comment='Limites mínimo e máximo de OUTLIER para WVDIR (Direção de Onda)')
    outlier_limits_pkdir = Column(ARRAY(SmallInteger()), comment='Limites mínimo e máximo de OUTLIER para PKDIR (Direção de Pico)')
    outlier_limits_pkspread = Column(ARRAY(SmallInteger()), comment='Limites mínimo e máximo de OUTLIER para PKSPREAD. (Direção de Espalhamento)')
    outlier_limits_wvspread = Column(ARRAY(SmallInteger()), comment='Limites mínimo e máximo de OUTLIER para WVSPREAD (Direção Média de Espalhamento)')
    sensors_limits_id = Column(ForeignKey('quality_control.sensors_limits_spotter.id'), comment='Chave com a tabela de limites de medição dos parâmetros dos sensores da Spotter')

    buoy = relationship('Buoy')
    sensors_limits = relationship('SensorsLimitsSpotter')
