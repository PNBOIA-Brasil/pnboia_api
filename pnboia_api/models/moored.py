# coding: utf-8
from sqlalchemy import Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, JSON, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class MetareaV(Base):
    __tablename__ = 'metarea_v'
    __table_args__ = {'schema': 'moored', 'comment': 'Geom Polygons das subáreas da Metarea V;´'}

    area_id = Column(String(1), primary_key=True, comment='ID da área.')
    area = Column(String(10), comment='Área da Metarea V.')
    geometry = Column(Geometry(srid=4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), comment='Polygon da área.')

class Buoy(Base):
    __tablename__ = 'buoys'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com todas informações sobre as boias fundeadas.'}

    buoy_id = Column(SmallInteger, primary_key=True, comment='Id de identificação da boia.')
    hull_id = Column(ForeignKey('inventory.hull.hull_id', onupdate='CASCADE'), comment='Identificação do casco')
    name = Column(String(30), comment='Nome atribuído à boia.')
    deploy_date = Column(Date, comment='Data em que a boia foi lançada.')
    last_date_time = Column(DateTime, comment='Datetime do último date_time registrado pela boia. Último dado válido (boia em operação).')
    latitude = Column(Numeric(6, 4))
    longitude = Column(Numeric(6, 4))
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    status = Column(Boolean)
    mode = Column(String(10), comment='Modo de operação da boia. Apenas FUNDEADA, DERIVA ou NULL (vazio) são aceitos.')
    watch_circle_distance = Column(SmallInteger, comment='Raio de ação do sistema de fundeio, em metros.')
    wmo_number = Column(String(10), comment='Número da WMO da região de lançamento.')
    antenna_id = Column(String(50), comment='Número da antena ou do registro da boia no sistema de transmissão (varia de empresa para empresa).')
    open_data = Column(Boolean, comment='Se dados são abertos ao público em geral.')
    link_site_pnboia = Column(Text, comment='Caso os dados sejam divulgados, link da página no site do CHM.')
    metarea_section = Column(ForeignKey('moored.metarea_v.area_id', onupdate='CASCADE'), comment='METAREA em que a boia está localizada.')
    project_id = Column(ForeignKey('institution.project.id', onupdate='CASCADE'), comment='ID do projeto responsável pela boia.')

    hull = relationship('Hull')
    metarea_v = relationship('MetareaV')
    project = relationship('Project')


class Alert(Base):
    __tablename__ = 'alerts'
    __table_args__ = {'schema': 'moored', 'comment': 'Configuração do sistema de alertas das boias.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.alerts_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), comment='Id da boia')
    drift = Column(Boolean, nullable=False, comment='Alerta de deriva.')
    transmission = Column(Boolean, nullable=False, comment='Alerta de transmissão. (Gap de transmissão)')
    transmission_gap = Column(SmallInteger, comment='GAP de transmissão, em minutos, usado para disparar o alerta.')
    sensor_fail = Column(Boolean, nullable=False, comment='Alerta para falha de sensor.')
    manual_watch_circle = Column(SmallInteger, comment='Raio de ação do sistema de fundeio, em metros (CONFIGURAÇÃO MANUAL).')
    auto_drift_alert = Column(Boolean, comment='Alerta automático de deriva. Caso positivo, o alerta automático estará ativo.')

    buoy = relationship('Buoy')


class AxysAdcp(Base):
    __tablename__ = 'axys_adcp'
    __table_args__ = {'schema': 'moored'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.axys_adcp_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id'))
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

    buoy = relationship('Buoy')


class AxysGeneral(Base):
    __tablename__ = 'axys_general'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com todos os dados brutos das boias Axys-3M.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.axys_general_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id'), comment='Identificação da boia')
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

    buoy = relationship('Buoy')


class BmobrRaw(Base):
    __tablename__ = 'bmobr_raw'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com os dados brutos da BMO-BR, sem tratamento algum.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.bmobr_raw_id_seq'::regclass)"), comment='ID do dado.')
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP dos dados em horário ZULU. Esse TIMESTAMP é retirado da mensagem principal, tratado (transformado em datetime ZULU).')
    data_string = Column(Text, comment="Mensagem/string transmitida pelo DataLogger contendo os dados. Os campos são separados por ';'.")

    buoy = relationship('Buoy')


class BmobrTriaxysRaw(Base):
    __tablename__ = 'bmobr_triaxys_raw'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela de dados brutos do triaxys das boias BMO-BR. Dados enviados via satélite em tempo real.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.bmobr_triaxys_raw_id_seq'::regclass)"), comment='ID do dado.')
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado. Dado retirado da string e transformado em TIMESTAMP horário ZULU.')
    data_string = Column(Text, comment='String contendo todos os dados.')

    buoy = relationship('Buoy')


class RegisterBuoy(Base):
    __tablename__ = 'register_buoys'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com estações do PNBOIA com períodos de funcionamento.'}

    id = Column(SmallInteger, primary_key=True, server_default=text("nextval('moored.register_buoys_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id'), nullable=False, comment='ID da boia.')
    location = Column(String(20), comment='Nome da estação.')
    state = Column(String(20), comment='Estado federativo onde a estação está localizada.')
    latitude = Column(Numeric(6, 4))
    longitude = Column(Numeric(6, 4))
    start_date = Column(DateTime, comment='Datahora de início do período de funcionamento.')
    end_date = Column(DateTime, comment='Datahora de fim do período de funcionamento.')
    duration = Column(INTERVAL(fields='day'), Computed('(end_date - start_date)', persisted=True), comment='Duração em dias do período de funcionamento.')
    current_configuration = Column(Boolean, comment='Caso seja a configuração atual da boia, TRUE, caso contrário, será FALSE.')
    depth = Column(SmallInteger, comment='Profundidade do local do fundeio.')
    cable = Column(SmallInteger, comment='Quantidade total de cabo no sistema de fundeio, em metros.')

    buoy = relationship('Buoy')


class SpotterGeneral(Base):
    __tablename__ = 'spotter_general'
    __table_args__ = {'schema': 'moored', 'comment': 'Dados gerais das boias spotters.'}

    id = Column(Integer, nullable=False, unique=True, server_default=text("nextval('moored.spotter_general_id_seq'::regclass)"), comment='ID do dado.')
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), primary_key=True, nullable=False, comment='ID da boia spotter.')
    date_time = Column(DateTime, primary_key=True, nullable=False, comment='TIMESTAMP em horário ZULU.')
    latitude = Column(Numeric(6, 4))
    longitude = Column(Numeric(6, 4))
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    wspd = Column(Numeric(4, 2), comment='Wind Speed - Velocidade de Vento, em m/s. (variável calculada pela boia, não é observação direta)')
    wdir = Column(SmallInteger, comment='Wind Direction - Direção de Vento, em graus (variável calculada pela boia, não é observação direta).')
    sst = Column(Numeric(4, 2), comment='Sea Surface Temperature - Temperatura da Superfície do Mar, em graus Celius.')
    swvht = Column(Numeric(4, 2), comment='Sea Wave Height - Altura Significativa, em metros.')
    tp = Column(Numeric(4, 2), comment='Peak Period - Período de Pico, em segundos.')
    tm = Column(Numeric(4, 2), comment='Mean Period - Período Médio, em segundos.')
    pkdir = Column(SmallInteger, comment='Peak Wave Direction - Direção de Pico, em graus.')
    wvdir = Column(SmallInteger, comment='Mean Wave Direction - Direção Média de Onda, em graus.')
    pkspread = Column(SmallInteger, comment='Peak Directional Spread - Direção de Pico de Espalhamento, em graus.')
    wvspread = Column(SmallInteger, comment='Mean Wave Direction - Direção Média de Espalhamento, em graus.')

    buoy = relationship('Buoy')


class SpotterSmartMooring(Base):
    __tablename__ = 'spotter_smart_mooring'
    __table_args__ = {'schema': 'moored', 'comment': 'Dados de temperatura do smart mooring (fundeio inteligente) da Spotter.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.spotter_smart_mooring_id_seq'::regclass)"), comment='Id do dado')
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), nullable=False, comment='Id da boia.')
    date_time = Column(DateTime, nullable=False)
    latitude = Column(Numeric(8, 6), nullable=False)
    longitude = Column(Numeric(8, 6), nullable=False)
    sensors_data = Column(JSON, comment='Dados dos sensores.')

    buoy = relationship('Buoy')


class SpotterSmartMoringConfig(Base):
    __tablename__ = 'spotter_smart_moring_config'
    __table_args__ = {'schema': 'moored', 'comment': 'Configuração da disposição dos sensores na linha de fundeio do smart mooring da Spotter.'}

    id = Column(SmallInteger, primary_key=True, server_default=text("nextval('moored.spotter_smart_moring_config_id_seq'::regclass)"), comment='Id do registro.')
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), comment='Id da boia')
    sensor = Column(String(20), comment='Tipo de sensor (Temp, Pres, ...)')
    depth = Column(SmallInteger, comment='Profundidade do sensor na linha de fundeio, em metros.')

    buoy = relationship('Buoy')


class SpotterSystem(Base):
    __tablename__ = 'spotter_system'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com informações sobre o sistema da spotter, como bateria e umidade interna.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.spotter_system_id_seq'::regclass)"), comment='ID único do dado')
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), nullable=False, comment='ID da boia.')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado, em ZULU.')
    latitude = Column(Numeric(6, 4), nullable=False)
    longitude = Column(Numeric(6, 4), nullable=False)
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    battery_power = Column(Numeric(4, 2), comment='Energia da bateria, em Volts.')
    battery_voltage = Column(Numeric(4, 2), comment='Voltagem da bateria, em Volts.')
    solar_voltage = Column(Numeric(4, 2), comment='Voltagem da bateria solar.')
    humidity = Column(Numeric(3, 1), comment='Umidade INTERNA da boia.')

    buoy = relationship('Buoy')


class Tag(Base):
    __tablename__ = 'tags'
    __table_args__ = {'schema': 'moored', 'comment': 'Coordenadas das tags argos de segurança usada nas boias.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.tags_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), nullable=False, comment='Id da boia em que a tag está instalada.')
    date_time = Column(DateTime, nullable=False, comment='DATETIME em horário ZULU.')
    latitude = Column(Numeric(8, 6), nullable=False)
    longitude = Column(Numeric(8, 6), nullable=False)
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')

    buoy = relationship('Buoy')


class BmobrGeneral(Base):
    __tablename__ = 'bmobr_general'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com os dados gerais das boias BMO-BR, com tratamento das strings e dados de acordo com seu DataType e tamanho.'}

    id = Column(ForeignKey('moored.bmobr_raw.id', onupdate='CASCADE'), nullable=False, unique=True, comment='ID do dado.')
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'), primary_key=True, nullable=False, comment='ID da boia.')
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

    buoy = relationship('Buoy')
    bmobr_raw = relationship('BmobrRaw', uselist=False)


class BmobrTriaxy(Base):
    __tablename__ = 'bmobr_triaxys'
    __table_args__ = {'schema': 'moored'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.bmobr_triaxys_id_seq'::regclass)"))
    buoy_id = Column(ForeignKey('moored.buoys.buoy_id', onupdate='CASCADE'))
    raw_id = Column(ForeignKey('moored.bmobr_triaxys_raw.id', onupdate='CASCADE'))
    date_time = Column(DateTime)
    mean_average_direction = Column(Numeric)
    spread_direction = Column(Numeric)
    period = Column(Numeric)
    energy = Column(Numeric)
    wvdir = Column(Numeric)
    spread = Column(Numeric)

    buoy = relationship('Buoy')
    raw = relationship('BmobrTriaxysRaw')


class Operation(Base):
    __tablename__ = 'operations'
    __table_args__ = {'schema': 'moored', 'comment': 'Registros de comissões realizadas para as boias.'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.operations_id_seq'::regclass)"))
    ship = Column(String(100), nullable=False, comment='Navio usado para comissão')
    start_date = Column(Date, nullable=False, comment='Início da comissão.')
    end_date = Column(Date, nullable=False, comment='Fim da comissão')
    type = Column(String(30), nullable=False, comment='Tipo de Operação: Lançamento, Manutenção, Recolhimento')
    report = Column(Text, comment='Pequeno relato de como foi a operação de lançamento. Ex:\n\n"A comissão ocorreu 100% conforme o previsto."\n"Por mal tempo, não foi possível recolher o cartão de memória. O anemomêtro 1 estava quebrado"\n"Houve problemas no lançamento, a linha de fundeio precisou ser modificada para xxxx".')
    team = Column(JSON, comment='Equipe presente na comissão. Tanto membros do CHM quanto membros externos, de empresas ou outras instituições.')
    register_id = Column(ForeignKey('moored.register_buoys.id'))

    register = relationship('RegisterBuoy')


class Sensor(Base):
    __tablename__ = 'sensors'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com informações dos sensores em uso nas boias meteoceonográficas (ex: Axys, BMO...).'}

    id = Column(Integer, primary_key=True, server_default=text("nextval('moored.sensors_id_seq'::regclass)"))
    sensor_id = Column(ForeignKey('inventory.sensors.sensor_id'), nullable=False, server_default=text("nextval('moored.sensors_sensor_id_seq'::regclass)"), comment='ID de identificação do sensor.')
    sensor_type = Column(String(40), comment='Tipo de sensor e número (ANEMOMETRO_1, ANEMOMETRO_2, HIGROTERMOGRAFO, ADCP, etc)...')
    register_id = Column(ForeignKey('moored.register_buoys.id'))

    register = relationship('RegisterBuoy')
    sensor = relationship('Sensor', remote_side=[id])


class SetupBuoy(Base):
    __tablename__ = 'setup_buoy'
    __table_args__ = {'schema': 'moored', 'comment': 'Tabela com a configuração (altura, profundidade...) dos sensores nas boias. Todas as medidas de distância em metros.'}

    id = Column(SmallInteger, primary_key=True, comment='Configuração única da boia.')
    height_anemometer_1 = Column(Numeric(3, 2), comment='Altura do anemomêtro 1, em metros.')
    height_anemometer_2 = Column(Numeric(3, 2), comment='Altura do anemômetro 2.')
    height_thermohygrometer = Column(Numeric(3, 2), comment='Altura do higromêtro.')
    height_barometer = Column(Numeric(3, 2), comment='Altura do barômetro.')
    depth_adcp = Column(Numeric(3, 2), comment='Profundidade do ADCP.')
    depth_temp_sensor = Column(Numeric(3, 2), comment='Profundidade sensor de temperatura.')
    register_id = Column(ForeignKey('moored.register_buoys.id'))

    register = relationship('RegisterBuoy')
