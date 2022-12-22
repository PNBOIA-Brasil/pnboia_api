# coding: utf-8
from sqlalchemy import Boolean, Column, Computed, Date, ARRAY, DateTime, ForeignKey, Integer, JSON, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Buoy(Base):
    __tablename__ = 'buoys'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com todas informações sobre as boias fundeadas.'}

    buoy_id = Column(SmallInteger, primary_key=True, comment='Id de identificação da boia.')
    hull_id = Column(SmallInteger, comment='Identificação do casco')
    name = Column(String(30), comment='Nome atribuído à boia.')
    deploy_date = Column(Date, comment='Data em que a boia foi lançada.')
    last_date_time = Column(DateTime, comment='Datetime do último date_time registrado pela boia. Último dado válido (boia em operação).')
    latitude = Column(Numeric(10, 4))
    longitude = Column(Numeric(10, 4))
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    status = Column(Boolean)
    mode = Column(String(10), comment='Modo de operação da boia. Apenas FUNDEADA, DERIVA ou NULL (vazio) são aceitos.')
    watch_circle_distance = Column(SmallInteger, comment='Raio de ação do sistema de fundeio, em metros.')
    wmo_number = Column(String(10), comment='Número da WMO da região de lançamento.')
    antenna_id = Column(String(50), comment='Número da antena ou do registro da boia no sistema de transmissão (varia de empresa para empresa).')
    open_data = Column(Boolean, comment='Se dados são abertos ao público em geral.')
    link_site_pnboia = Column(Text, comment='Caso os dados sejam divulgados, link da página no site do CHM.')
    metarea_section = Column(String(10), comment='METAREA em que a boia está localizada.')
    project_id = Column(SmallInteger, comment='ID do projeto responsável pela boia.')
    
class AxysAdcp(Base):
    __tablename__ = 'axys_adcp'
    __table_args__ = {'schema': 'moored'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.axys_adcp_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), nullable=False)
    year = Column(SmallInteger)
    month = Column(SmallInteger)
    day = Column(SmallInteger)
    hour = Column(SmallInteger)
    cspd1 = Column(Numeric)
    cdir1 = Column(SmallInteger)
    cspd2 = Column(Numeric)
    cdir2 = Column(SmallInteger)
    cspd3 = Column(Numeric)
    cdir3 = Column(SmallInteger)
    cspd4 = Column(Numeric)
    cdir4 = Column(SmallInteger)
    cspd5 = Column(Numeric)
    cdir5 = Column(SmallInteger)
    cspd6 = Column(Numeric)
    cdir6 = Column(SmallInteger)
    cspd7 = Column(Numeric)
    cdir7 = Column(SmallInteger)
    cspd8 = Column(Numeric)
    cdir8 = Column(SmallInteger)
    cspd9 = Column(Numeric)
    cdir9 = Column(SmallInteger)
    cspd10 = Column(Numeric)
    cdir10 = Column(SmallInteger)
    cspd11 = Column(Numeric)
    cdir11 = Column(SmallInteger)
    cspd12 = Column(Numeric)
    cdir12 = Column(SmallInteger)
    cspd13 = Column(Numeric)
    cdir13 = Column(SmallInteger)
    cspd14 = Column(Numeric)
    cdir14 = Column(SmallInteger)
    cspd15 = Column(Numeric)
    cdir15 = Column(SmallInteger)
    cspd16 = Column(Numeric)
    cdir16 = Column(SmallInteger)
    cspd17 = Column(Numeric)
    cdir17 = Column(SmallInteger)
    cspd18 = Column(Numeric)
    cdir18 = Column(SmallInteger)
    cspd19 = Column(Numeric)
    cdir19 = Column(SmallInteger)
    cspd20 = Column(Numeric)
    cdir20 = Column(SmallInteger)

    buoy = relationship(Buoy, foreign_keys=[buoy_id])

class AxysGeneral(Base):
    __tablename__ = 'axys_general'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com todos os dados brutos das boias Axys-3M.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.axys_general_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey(Buoy.buoy_id), comment='Identificação da boia')
    date_time = Column(DateTime, nullable=False, comment='Data hora, em ZULU.')
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True))
    battery = Column(Numeric)
    compass = Column(SmallInteger, comment='Norte da bússola.')
    wspd1 = Column(Numeric, comment='Wind Speed - Velocidade do Vento, em m/s. Anemômetro 1.')
    wdir1 = Column(Integer, comment='Wind Direction 1, Direção do Vento. Sensor 1.')
    gust1 = Column(Numeric, comment='Wind Gust 1, Rajada do Vento sensor1.')
    wspd2 = Column(Numeric, comment='Wind Speed - Velocidade do Vento, em m/s. Anemômetro 2.')
    wdir2 = Column(SmallInteger, comment='Wind Direction - Direção do Vento, em graus. Anemômetro 2.')
    gust2 = Column(Numeric, comment='Wind Gust - Rajada de Vento, em m/s. Anemomêtro 2.')
    atmp = Column(Numeric, comment='Air Temperature - Temperatura do Ar, em graus Celsius.')
    srad = Column(Numeric, comment='Solar Radiation - Radiação Solar Média - W/m²')
    rh = Column(Numeric, comment='Relative Humidity - Umidade Relativa, em %.')
    dewpt = Column(Numeric, comment='Dew Point - Ponto de Orvalho, em graus Celsius.')
    pres = Column(Numeric, comment='Atmospheric Pressure - Pressão Atmosférica, em hbar.')
    sst = Column(Numeric, comment='Sea Surface Temperature - Temperatura da Superfície do Mar, em graus Celsius.')
    cspd1 = Column(Numeric, comment='Current Speed Level 1 - Velocidade de Corrente Nível 1, em m/s.')
    cdir1 = Column(SmallInteger, comment='Current Direction Level 1 - Direção de Corrente Nível 1, em graus.')
    cspd2 = Column(Numeric)
    cdir2 = Column(SmallInteger)
    cspd3 = Column(Numeric)
    cdir3 = Column(SmallInteger)
    swvht = Column(Numeric)
    tp = Column(Numeric)
    wvdir = Column(Numeric)
    mxwvht = Column(Numeric)
    wvspread = Column(Numeric)

    buoy = relationship(Buoy, foreign_keys=[buoy_id])

class BmobrRaw(Base):
    __tablename__ = 'bmobr_raw'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com os dados brutos da BMO-BR, sem tratamento algum.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.bmobr_raw_id_seq'::regclass)"), comment='ID do dado.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP dos dados em horário ZULU. Esse TIMESTAMP é retirado da mensagem principal, tratado (transformado em datetime ZULU).')
    data_string = Column(Text, comment="Mensagem/string transmitida pelo DataLogger contendo os dados. Os campos são separados por ';'.")

    buoy = relationship(Buoy, foreign_keys=[buoy_id])


class BmobrGeneral(Base):
    __tablename__ = 'bmobr_general'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com os dados gerais das boias BMO-BR, com tratamento das strings e dados de acordo com seu DataType e tamanho.'}

    id = Column(ForeignKey(BmobrRaw.id, onupdate='CASCADE'), nullable=False, unique=True, comment='ID do dado.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), primary_key=True, nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, primary_key=True, nullable=False, comment='TIMESTAMP do dado em horário ZULU.')
    latitude = Column(Numeric, nullable=False, comment='Latitude das observações, em graus.')
    longitude = Column(Numeric, nullable=False, comment='Longitude das observações, em graus.')
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    battery = Column(Numeric, comment='Voltagem da bateria (Volts).')
    compass = Column(Numeric, comment='Bússola, em graus.')
    wspd1 = Column(Numeric, comment='Wind Speed - Velocidade do Vento, em m/s. Anemomêtro 1.')
    wdir1 = Column(SmallInteger, comment='Wind Direction - Direção de Vento, em graus. Anemomêtro 1.')
    gust1 = Column(Numeric, comment='Wind Gust - Rajada de Vento, em m/s. Anemomêtro 1.')
    wspd2 = Column(Numeric, comment='Wind Speed - Velocidade do Vento, em m/s. Anemomêtro 2.')
    wdir2 = Column(SmallInteger, comment='Wind Direction - Direção de Vento, em graus. Anemomêtro 2.')
    gust2 = Column(Numeric, comment='Wind Gust - Rajada de Vento, em m/s. Anemomêtro 2.')
    atmp = Column(Numeric, comment='Air Temperature - Temperature do Ar, em graus Celsius.')
    srad = Column(Numeric, comment='Solar Radiation - Radiação Solar Média - W/m²')
    rh = Column(Numeric, comment='Relative Humidity - Umidade Relativa, em %.')
    dewpt = Column(Numeric, comment='Dew Point - Ponto de Orvalho, em graus Celsius.')
    pres = Column(Numeric, comment='Atmospheric Pressure - Pressão Atmosférica, em hbar.')
    sst = Column(Numeric, comment='Sea Surface Temperature - Temperature da Superfície do Mar, em graus Celsius.')
    cspd1 = Column(Numeric, comment='Current Speed Level 1 - Velocidade de Corrente nível 1, em m/s.')
    cdir1 = Column(SmallInteger, comment='Current Direction Level 1 - Direção de Corrente nível 1, em graus.')
    cspd2 = Column(Numeric, comment='Current Speed Level 2 - Velocidade de Corrente nível 2, em m/s')
    cdir2 = Column(SmallInteger, comment='Current Direction Level 2 - Direção de Corrente nível 2, em graus.')
    cspd3 = Column(Numeric)
    cdir3 = Column(SmallInteger)
    cspd4 = Column(Numeric)
    cdir4 = Column(SmallInteger)
    cspd5 = Column(Numeric)
    cdir5 = Column(SmallInteger)
    cspd6 = Column(Numeric)
    cdir6 = Column(SmallInteger)
    cspd7 = Column(Numeric)
    cdir7 = Column(SmallInteger)
    cspd8 = Column(Numeric)
    cdir8 = Column(SmallInteger)
    cspd9 = Column(Numeric)
    cdir9 = Column(SmallInteger)
    cspd10 = Column(Numeric)
    cdir10 = Column(SmallInteger)
    cspd11 = Column(Numeric)
    cdir11 = Column(SmallInteger)
    cspd12 = Column(Numeric)
    cdir12 = Column(SmallInteger)
    cspd13 = Column(Numeric)
    cdir13 = Column(SmallInteger)
    cspd14 = Column(Numeric)
    cdir14 = Column(SmallInteger)
    cspd15 = Column(Numeric)
    cdir15 = Column(SmallInteger)
    cspd16 = Column(Numeric)
    cdir16 = Column(SmallInteger)
    cspd17 = Column(Numeric)
    cdir17 = Column(SmallInteger)
    cspd18 = Column(Numeric)
    cdir18 = Column(SmallInteger)
    swvht1 = Column(Numeric, comment='Sea Wave Height 1 - Altura Significativa de Onda, sensor 1 (Triaxys), em metros.')
    tp1 = Column(Numeric, comment='Peak Period 1 - Período de Pico, sensor 1 (Triaxys), em segundos.')
    mxwvht1 = Column(Numeric, comment='Maximum Wave Height 1 - Altura Máxima de Onda, sensor 1 (Triaxys), em metros.')
    wvdir1 = Column(SmallInteger, comment='Wave Direction 1 - Direção Média de Onda, sensor 1 (Triaxys), em graus.')
    wvspread1 = Column(SmallInteger, comment='Wave Spread 1 - Direção de Espalhamento, sensor 1 (Triaxys), em graus.')
    swvht2 = Column(Numeric, comment='Sea Wave Height 2 - Altura Significativa de Onda, sensor 2 (UCMO - Nacional), em metros.')
    tp2 = Column(Numeric, comment='Peak Period 2 - Período de Pico, sensor 2 (UCMO - Nacional), em segundos.')
    wvdir2 = Column(SmallInteger, comment='Wave Peak Direction 2 - Direção de Pico Primário de Onda, sensor 2 (UCMO - Nacional), em graus.')

    buoy = relationship(Buoy, foreign_keys=[buoy_id])

    bmobr_raw = relationship(BmobrRaw, foreign_keys=[id])


class BmobrTriaxysRaw(Base):
    __tablename__ = 'bmobr_triaxys_raw'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela de dados brutos do triaxys das boias BMO-BR. Dados enviados via satélite em tempo real.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.bmobr_triaxys_raw_id_seq'::regclass)"), comment='ID do dado.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado. Dado retirado da string e transformado em TIMESTAMP horário ZULU.')
    data_string = Column(Text, comment='String contendo todos os dados.')

    buoy = relationship(Buoy, foreign_keys=[buoy_id])

class CriosferaGeneral(Base):
    __tablename__ = 'criosfera_general'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com os dados gerais das boias Criosfera.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.bmobr_raw_id_seq'::regclass)"), comment='ID do dado.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), primary_key=True, nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, primary_key=True, nullable=False, comment='TIMESTAMP do dado em horário ZULU.')
    latitude = Column(Numeric, nullable=False, comment='Latitude das observações, em graus.')
    longitude = Column(Numeric, nullable=False, comment='Longitude das observações, em graus.')
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    battery = Column(Numeric, comment='Voltagem da bateria (Volts).')
    temp_datalogger = Column(Numeric)
    atmp = Column(Numeric, comment='Air Temperature - Temperature do Ar, em graus Celsius.')
    pres = Column(Numeric, comment='Atmospheric Pressure - Pressão Atmosférica, em hbar.')
    rh = Column(Numeric, comment='Relative Humidity - Umidade Relativa, em %.')
    srad = Column(Numeric, comment='Solar Radiation - Radiação Solar Média - W/m²')
    cond = Column(Numeric)
    sss = Column(Numeric)
    sst = Column(Numeric, comment='Sea Surface Temperature - Temperature da Superfície do Mar, em graus Celsius.')
    wspd1 = Column(Numeric, comment='Wind Speed - Velocidade do Vento, em m/s. Anemomêtro 1.')
    wdir1 = Column(Numeric, comment='Wind Direction - Direção de Vento, em graus. Anemomêtro 1.')
    status1 = Column(Numeric)
    wspd2 = Column(Numeric, comment='Wind Speed - Velocidade do Vento, em m/s. Anemomêtro 2.')
    wdir2 = Column(Numeric, comment='Wind Direction - Direção de Vento, em graus. Anemomêtro 2.')

    buoy = relationship(Buoy, foreign_keys=[buoy_id])

class SpotterAll(Base):
    __tablename__ = 'spotter_all'
    __table_args__ = {'schema': 'moored', 'comment': 'Dados gerais das boias spotters.'}

    id = Column(Integer, nullable=False, unique=True, server_default=text("nextval('moored.spotter_general_id_seq'::regclass)"), comment='ID do dado.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), primary_key=True, nullable=False, comment='ID da boia spotter.')
    date_time = Column(DateTime, primary_key=True, nullable=False, comment='TIMESTAMP em horário ZULU.')
    latitude = Column(Numeric(10, 4))
    longitude = Column(Numeric(10, 4))
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    wspd1 = Column(Numeric(10, 2), comment='Wind Speed - Velocidade de Vento, em m/s. (variável calculada pela boia, não é observação direta)')
    wdir1 = Column(SmallInteger, comment='Wind Direction - Direção de Vento, em graus (variável calculada pela boia, não é observação direta).')
    sst = Column(Numeric(10, 2), comment='Sea Surface Temperature - Temperatura da Superfície do Mar, em graus Celius.')
    swvht1 = Column(Numeric(10, 2), comment='Sea Wave Height - Altura Significativa, em metros.')
    tp1 = Column(Numeric(10, 2), comment='Peak Period - Período de Pico, em segundos.')
    tm1 = Column(Numeric(10, 2), comment='Mean Period - Período Médio, em segundos.')
    pkdir1 = Column(SmallInteger, comment='Peak Wave Direction - Direção de Pico, em graus.')
    wvdir1 = Column(SmallInteger, comment='Mean Wave Direction - Direção Média de Onda, em graus.')
    pkspread1 = Column(SmallInteger, comment='Peak Directional Spread - Direção de Pico de Espalhamento, em graus.')
    wvspread1 = Column(SmallInteger, comment='Mean Wave Direction - Direção Média de Espalhamento, em graus.')
    sensors_data = Column(ARRAY(Numeric))

    buoy = relationship(Buoy, foreign_keys=[buoy_id])

class SpotterSmartMooringConfig(Base):
    __tablename__ = 'spotter_smart_mooring_config'
    __table_args__ = {'schema': 'moored', 'comment': 'Configuração da disposição dos sensores na linha de fundeio do smart mooring da Spotter.'}

    id = Column(SmallInteger, primary_key=True, server_default=text("nextval('moored.spotter_smart_moring_config_id_seq'::regclass)"), comment='Id do registro.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), comment='Id da boia')
    sensor = Column(String(20), comment='Tipo de sensor (Temp, Pres, ...)')
    depth = Column(SmallInteger, comment='Profundidade do sensor na linha de fundeio, em metros.')

    buoy = relationship(Buoy, foreign_keys=[buoy_id])

class SpotterSystem(Base):
    __tablename__ = 'spotter_system'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com informações sobre o sistema da spotter, como bateria e umidade interna.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.spotter_system_id_seq'::regclass)"), comment='ID único do dado')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado, em ZULU.')
    latitude = Column(Numeric(10, 4), nullable=False)
    longitude = Column(Numeric(10, 4), nullable=False)
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    battery_power = Column(Numeric(10, 2), comment='Energia da bateria, em Volts.')
    battery_voltage = Column(Numeric(10, 2), comment='Voltagem da bateria, em Volts.')
    solar_voltage = Column(Numeric(10, 2), comment='Voltagem da bateria solar.')
    humidity = Column(Numeric(10, 1), comment='Umidade INTERNA da boia.')

    buoy = relationship(Buoy, foreign_keys=[buoy_id])


class TriaxysGeneral(Base):
    __tablename__ = 'triaxys_general'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com os dados gerais das boias Triaxys, com tratamento das strings e dados de acordo com seu DataType e tamanho.'}

    id = Column(ForeignKey(BmobrRaw.id, onupdate='CASCADE'), nullable=False, unique=True, comment='ID do dado.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), primary_key=True, nullable=False, comment='ID da boia.')
    raw_id = Column(ARRAY(Integer))
    message_id = Column(String(3))
    date_time = Column(DateTime, primary_key=True, nullable=False, comment='TIMESTAMP do dado em horário ZULU.')
    latitude = Column(Text)
    longitude = Column(Numeric, nullable=False, comment='Longitude das observações, em graus.')
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    wavestats_timestamp = Column(Integer)
    wavestats_duration = Column(Integer)
    zero_crossings = Column(Integer)
    avwvht = Column(Numeric)
    tav = Column(Numeric)
    mxwvht1 = Column(Numeric, comment='Maximum Wave Height 1 - Altura Máxima de Onda, sensor 1 (Triaxys), em metros.')
    tmax = Column(Numeric)
    pk_crest = Column(Numeric)
    swvht1 = Column(Numeric, comment='Sea Wave Height 1 - Altura Significativa de Onda, sensor 1 (Triaxys), em metros.')
    tsig = Column(Numeric)
    h110 = Column(Numeric)
    t110 = Column(Numeric)
    tm02 = Column(Numeric)
    tp1 = Column(Numeric, comment='Peak Period 1 - Período de Pico, sensor 1 (Triaxys), em segundos.')
    tp_dir = Column(Numeric)
    tp_spread = Column(Numeric)
    tp5 = Column(Numeric)
    hm0 = Column(Numeric)
    wvdir1 = Column(SmallInteger, comment='Wave Direction 1 - Direção Média de Onda, sensor 1 (Triaxys), em graus.')
    tm01 = Column(Numeric)
    sst = Column(Integer)

    buoy = relationship(Buoy, foreign_keys=[buoy_id])


class TriaxysRaw(Base):
    __tablename__ = 'triaxys_raw'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela de dados brutos do triaxys das boias BMO-BR. Dados enviados via satélite em tempo real.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.bmobr_triaxys_raw_id_seq'::regclass)"), comment='ID do dado.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    prime_id = Column(Integer)
    data_type = Column(String(40))
    date_time_trans = Column(DateTime, nullable=False, comment='TIMESTAMP do dado. Dado retirado da string e transformado em TIMESTAMP horário ZULU.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado. Dado retirado da string e transformado em TIMESTAMP horário ZULU.')
    string = Column(Text, comment='String contendo todos os dados.')

    buoy = relationship(Buoy, foreign_keys=[buoy_id])

class TriaxysStatus(Base):
    __tablename__ = 'triaxys_status'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela de dados brutos do triaxys das boias BMO-BR. Dados enviados via satélite em tempo real.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.bmobr_triaxys_raw_id_seq'::regclass)"), comment='ID do dado.')
    raw_id = Column(Integer)
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado. Dado retirado da string e transformado em TIMESTAMP horário ZULU.')
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    watch_circle_status = Column(Integer)
    av_serv_persec = Column(Numeric)
    inst_node = Column(Numeric)
    battery = Column(Numeric)
    pcb_temp = Column(Numeric)
    n_resets = Column(Integer)
    curr_boot_timestamp = Column(Integer)
    shutdown_type = Column(Integer)
    memory_max_free = Column(Integer)
    log_error_count = Column(Integer)
    last_log_error = Column(Integer)
    free_space = Column(Integer)
    error_count = Column(Integer)
    solar_voltage = Column(Numeric)
    water_intrusion_voltage = Column(Numeric)
    time_sync = Column(Numeric)
    terminal_cnr = Column(Numeric)

    buoy = relationship(Buoy, foreign_keys=[buoy_id])
