
# coding: utf-8
from sqlalchemy import Boolean, Column, Computed, Date, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, text
from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pnboia_api.models.moored import *

Base = declarative_base()
metadata = Base.metadata

class QualifiedData(Base):
    __tablename__ = 'qualified_data'
    __table_args__ = {'schema': 'qualified_data', 'comment': 'Tabela contendo todos os dados qualificados e com suas respectivas flags.'}

    id = Column(SmallInteger, primary_key=True, comment='Id da boia.')
    raw_id = Column(Integer, comment='ID do dado. O ID é o mesmo ID do dado nas tabelas originais dos dados brutos.')
    buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), comment='ID da boia')
    date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado, em horário ZULU.')
    latitude = Column(Numeric(8, 6), nullable=False)
    longitude = Column(Numeric(8, 6), nullable=False)
    geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
    battery = Column(Numeric(4, 2), comment='Voltagem da Bateria (Volts).')
    flag_battery = Column(SmallInteger, comment='Flag para bateria.')
    rh = Column(Numeric(4, 2), comment='Relative Humidity - Umidade Relativa, em %.')
    flag_rh = Column(SmallInteger)
    wspd1 = Column(Numeric(4, 2), comment='Wind Speed 1 - Velocidade do Vento, Anemomêtro 1, em m/s.')
    flag_wspd1 = Column(SmallInteger)
    wdir1 = Column(SmallInteger, comment='Wind Direction 1 - Direção do Vento, Anemomêtro 1, em graus.')
    flag_wdir1 = Column(SmallInteger)
    wspd2 = Column(Numeric(4, 2), comment='Wind Speed 2 - Velocidade de Vento, Anemomêtro 2, em m/s.')
    flag_wspd2 = Column(SmallInteger)
    wdir2 = Column(SmallInteger, comment='Wind Direction 2 - Direção de Vento 2, em graus.')
    flag_wdir2 = Column(SmallInteger)
    gust1 = Column(Numeric(4, 2), comment='Wind Gust 1 - Rajada de Vento, Anemômetro 1, em m/s.')
    flag_gust1 = Column(SmallInteger)
    gust2 = Column(Numeric(4, 2), comment='Wind Gust 2 - Rajada de Vento, Anemômetro 2, em m/s.')
    flag_gust2 = Column(SmallInteger)
    atmp = Column(Numeric(4, 2), comment='Air Temperature - Temperatura do Ar, em graus Celsius.')
    flag_atmp = Column(SmallInteger)
    pres = Column(Numeric(6, 2), comment='Atmospheric Pressure - Pressão Atmosférica, em mBar.')
    flag_pres = Column(SmallInteger)
    srad = Column(Numeric(4, 2), comment='Solar Radiation - Radiação Solar, em W/m².')
    flag_srad = Column(SmallInteger)
    dewpt = Column(Numeric(4, 2), comment='Dew Point - Temperatura de Orvalho, em °C.')
    flag_dewpt = Column(SmallInteger)
    sst = Column(Numeric(4, 2), comment='Sea Surface Temperature - Temperatura da Superfície do Mar, em °C.')
    flag_sst = Column(SmallInteger)
    cspd1 = Column(Numeric(4, 2), comment='Current Speed 1 - Velocidade de Corrente nível 1, em m/s.')
    flag_cspd1 = Column(SmallInteger)
    cdir1 = Column(SmallInteger)
    flag_cdir1 = Column(SmallInteger)
    cspd2 = Column(Numeric(4, 2))
    flag_cspd2 = Column(SmallInteger)
    cdir2 = Column(SmallInteger)
    flag_cdir2 = Column(SmallInteger)
    cspd3 = Column(Numeric(4, 2))
    flag_cspd3 = Column(SmallInteger)
    cdir3 = Column(SmallInteger)
    flag_cdir3 = Column(SmallInteger)
    cspd4 = Column(Numeric(4, 2))
    flag_cspd4 = Column(SmallInteger)
    cdir4 = Column(SmallInteger)
    flag_cdir4 = Column(SmallInteger)
    cspd5 = Column(Numeric(4, 2))
    flag_cspd5 = Column(SmallInteger)
    cdir5 = Column(SmallInteger)
    flag_cdir5 = Column(SmallInteger)
    cspd6 = Column(Numeric(4, 2))
    flag_cspd6 = Column(SmallInteger)
    cdir6 = Column(SmallInteger)
    flag_cdir6 = Column(SmallInteger)
    cspd7 = Column(Numeric(4, 2))
    flag_cspd7 = Column(SmallInteger)
    cdir7 = Column(SmallInteger)
    flag_cdir7 = Column(SmallInteger)
    cspd8 = Column(Numeric(4, 2))
    flag_cspd8 = Column(SmallInteger)
    cdir8 = Column(SmallInteger)
    flag_cdir8 = Column(SmallInteger)
    cspd9 = Column(Numeric(4, 2))
    flag_cspd9 = Column(SmallInteger)
    cdir9 = Column(SmallInteger)
    flag_cdir9 = Column(SmallInteger)
    cspd10 = Column(Numeric(4, 2))
    flag_cspd10 = Column(SmallInteger)
    cdir10 = Column(SmallInteger)
    flag_cdir10 = Column(SmallInteger)
    cspd11 = Column(SmallInteger)
    flag_cspd11 = Column(SmallInteger)
    cdir11 = Column(SmallInteger)
    flag_cdir11 = Column(SmallInteger)
    cspd12 = Column(Numeric(4, 2))
    flag_cspd12 = Column(SmallInteger)
    cdir12 = Column(SmallInteger)
    flag_cdir12 = Column(SmallInteger)
    cspd13 = Column(Numeric(4, 2))
    flag_cspd13 = Column(SmallInteger)
    cdir13 = Column(SmallInteger)
    flag_cdir13 = Column(SmallInteger)
    cspd14 = Column(Numeric(4, 2))
    flag_cspd14 = Column(SmallInteger)
    cdir14 = Column(SmallInteger)
    flag_cdir14 = Column(SmallInteger)
    cspd15 = Column(Numeric(4, 2))
    flag_cspd15 = Column(SmallInteger)
    cdir15 = Column(SmallInteger)
    flag_cdir15 = Column(SmallInteger)
    cspd16 = Column(Numeric(4, 2))
    flag_cspd16 = Column(SmallInteger)
    cdir16 = Column(SmallInteger)
    flag_cdir16 = Column(SmallInteger)
    cspd17 = Column(Numeric(4, 2))
    flag_cspd17 = Column(SmallInteger)
    cdir17 = Column(SmallInteger)
    flag_cdir17 = Column(SmallInteger)
    cspd18 = Column(Numeric(4, 2))
    flag_cspd18 = Column(SmallInteger)
    cdir18 = Column(SmallInteger)
    flag_cdir18 = Column(SmallInteger)
    cspd19 = Column(Numeric(4, 2))
    flag_cspd19 = Column(SmallInteger)
    cdir19 = Column(SmallInteger)
    flag_cdir19 = Column(SmallInteger)
    cspd20 = Column(Numeric(4, 2))
    flag_cspd20 = Column(SmallInteger)
    cdir20 = Column(SmallInteger)
    flag_cdir20 = Column(SmallInteger)
    swvht1 = Column(Numeric(4, 2), comment='Sea Wave Height 1 - Altura Significativa de Onda, Sensor 1,')
    flag_swvht1 = Column(SmallInteger)
    tp1 = Column(Numeric(4, 2), comment='Peak Period 1 - Período de Pico, sensor 1 (Triaxys), em segundos.')
    flag_tp1 = Column(SmallInteger)
    mxwvht1 = Column(Numeric(4, 2), comment='Maximum Wave Height 1 - Altura Máxima de Onda, sensor 1 (Triaxys), em metros.')
    flag_mxwvht1 = Column(SmallInteger)
    wvdir1 = Column(SmallInteger, comment='Mean Wave Diretction 1 - Direção Média de Onda, sensor 1.')
    flag_wvdir1 = Column(SmallInteger)
    wvspread1 = Column(SmallInteger, comment='Wave Spread 1 - Direção de Espalhamento de Onda, Sensor 1')
    flag_wvspread1 = Column(SmallInteger)
    swvht2 = Column(Numeric(4, 2), comment='Sea Wave Height 2 - Altura Significativa de Onda, sensor 2 (UCMO - Nacional), em metros.')
    flag_swvht2 = Column(SmallInteger)
    tp2 = Column(Numeric(4, 2), comment='Peak Period 2 - Período de Pico, sensor 2 (UCMO - Nacional), em segundos.')
    flag_tp2 = Column(SmallInteger)
    wvdir2 = Column(SmallInteger, comment='Wave Peak Direction 2 - Direção de Pico Primário de Onda, sensor 2 (UCMO - Nacional), em graus.')
    flag_wvdir2 = Column(SmallInteger)
    tm1 = Column(Numeric)
    flag_tm1 = Column(SmallInteger)
    pkdir1 = Column(Numeric)
    flag_pkdir1 = Column(SmallInteger)
    pkspread1 = Column(Numeric)
    flag_pkspread1 = Column(SmallInteger)
    sensors_data_flagged = Column(JSON)
    cond = Column(Numeric)
    flag_cond = Column(SmallInteger)
    sss = Column(Numeric)
    flag_sss = Column(SmallInteger)

    buoy = relationship(Buoy, foreign_keys=[buoy_id])

# class QualifiedDataPetrobras(Base):

#     id = Column(SmallInteger, primary_key=True, comment='Id da boia.')
#     raw_id = Column(Integer, comment='ID do dado. O ID é o mesmo ID do dado nas tabelas originais dos dados brutos.')
#     buoy_id = Column(ForeignKey(Buoy.buoy_id, onupdate='CASCADE'), comment='ID da boia')
#     date_time = Column(DateTime, nullable=False, comment='TIMESTAMP do dado, em horário ZULU.')
#     Timestamp = Column(Numeric, nullable=False)
#     latitude = Column(Numeric(8, 6), nullable=False)
#     longitude = Column(Numeric(8, 6), nullable=False)
#     geom = Column(Geometry('POINT', 4326, spatial_index=False, from_text='ST_GeomFromEWKT', name='geometry'), Computed('st_setsrid(st_makepoint((longitude)::double precision, (latitude)::double precision), 4326)', persisted=True), comment='Coordenadas espacializadas (x, y) - (Longitude, Latitude)')
#     battery = Column(Numeric(4, 2), comment='Voltagem da Bateria (Volts).')
#     flag_battery = Column(SmallInteger, comment='Flag para bateria.')
#     HMS_HUMIDITY = Column(Numeric(4, 2), comment='Relative Humidity - Umidade Relativa, em %.')
#     flag_HMS_HUMIDITY = Column(SmallInteger)
#     HMS_WIND_SPEED1 = Column(Numeric(4, 2), comment='Wind Speed 1 - Velocidade do Vento, Anemomêtro 1, em m/s.')
#     flag_HMS_WIND_SPEED1 = Column(SmallInteger)
#     HMS_WIND_DIRECTION1 = Column(SmallInteger, comment='Wind Direction 1 - Direção do Vento, Anemomêtro 1, em graus.')
#     flag_HMS_WIND_DIRECTION1 = Column(SmallInteger)
#     HMS_WIND_SPEED2 = Column(Numeric(4, 2), comment='Wind Speed 2 - Velocidade de Vento, Anemomêtro 2, em m/s.')
#     flag_HMS_WIND_SPEED2 = Column(SmallInteger)
#     HMS_WIND_DIRECTION2 = Column(SmallInteger, comment='Wind Direction 2 - Direção de Vento 2, em graus.')
#     flag_HMS_WIND_DIRECTION2 = Column(SmallInteger)
#     gust1 = Column(Numeric(4, 2), comment='Wind Gust 1 - Rajada de Vento, Anemômetro 1, em m/s.')
#     flag_gust1 = Column(SmallInteger)
#     gust2 = Column(Numeric(4, 2), comment='Wind Gust 2 - Rajada de Vento, Anemômetro 2, em m/s.')
#     flag_gust2 = Column(SmallInteger)
#     HMS_TEMPERATURE = Column(Numeric(4, 2), comment='Air Temperature - Temperatura do Ar, em graus Celsius.')
#     flag_HMS_TEMPERATURE = Column(SmallInteger)
#     HMS_PRESSURE = Column(Numeric(6, 2), comment='Atmospheric Pressure - Pressão Atmosférica, em mBar.')
#     flag_HMS_PRESSURE = Column(SmallInteger)
#     srad = Column(Numeric(4, 2), comment='Solar Radiation - Radiação Solar, em W/m².')
#     flag_srad = Column(SmallInteger)
#     dewpt = Column(Numeric(4, 2), comment='Dew Point - Temperatura de Orvalho, em °C.')
#     flag_dewpt = Column(SmallInteger)
#     TEMPERATURA_AGUA = Column(Numeric(4, 2), comment='Sea Surface Temperature - Temperatura da Superfície do Mar, em °C.')
#     flag_TEMPERATURA_AGUA = Column(SmallInteger)
#     ADCP_BIN1_SPEED = Column(Numeric(4, 2), comment='Current Speed 1 - Velocidade de Corrente nível 1, em m/s.')
#     flag_ADCP_BIN1_SPEED = Column(SmallInteger)
#     ADCP_BIN1_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN1_DIRECTION = Column(SmallInteger)
#     ADCP_BIN2_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN2_SPEED = Column(SmallInteger)
#     ADCP_BIN2_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN2_DIRECTION = Column(SmallInteger)
#     ADCP_BIN3_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN3_SPEED = Column(SmallInteger)
#     ADCP_BIN3_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN3_DIRECTION = Column(SmallInteger)
#     ADCP_BIN4_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN4_SPEED = Column(SmallInteger)
#     ADCP_BIN4_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN4_DIRECTION = Column(SmallInteger)
#     ADCP_BIN5_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN5_SPEED = Column(SmallInteger)
#     ADCP_BIN5_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN5_DIRECTION = Column(SmallInteger)
#     ADCP_BIN6_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN6_SPEED = Column(SmallInteger)
#     ADCP_BIN6_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN6_DIRECTION = Column(SmallInteger)
#     ADCP_BIN7_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN7_SPEED = Column(SmallInteger)
#     ADCP_BIN7_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN7_DIRECTION = Column(SmallInteger)
#     ADCP_BIN8_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN8_SPEED = Column(SmallInteger)
#     ADCP_BIN8_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN8_DIRECTION = Column(SmallInteger)
#     ADCP_BIN9_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN9_SPEED = Column(SmallInteger)
#     ADCP_BIN9_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN9_DIRECTION = Column(SmallInteger)
#     ADCP_BIN10_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN10_SPEED = Column(SmallInteger)
#     ADCP_BIN10_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN10_DIRECTION = Column(SmallInteger)
#     ADCP_BIN11_SPEED = Column(SmallInteger)
#     flag_ADCP_BIN11_SPEED = Column(SmallInteger)
#     ADCP_BIN11_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN11_DIRECTION = Column(SmallInteger)
#     ADCP_BIN12_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN12_SPEED = Column(SmallInteger)
#     ADCP_BIN12_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN12_DIRECTION = Column(SmallInteger)
#     ADCP_BIN13_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN13_SPEED = Column(SmallInteger)
#     ADCP_BIN13_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN13_DIRECTION = Column(SmallInteger)
#     ADCP_BIN14_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN14_SPEED = Column(SmallInteger)
#     ADCP_BIN14_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN14_DIRECTION = Column(SmallInteger)
#     ADCP_BIN15_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN15_SPEED = Column(SmallInteger)
#     ADCP_BIN15_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN15_DIRECTION = Column(SmallInteger)
#     ADCP_BIN16_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN16_SPEED = Column(SmallInteger)
#     ADCP_BIN16_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN16_DIRECTION = Column(SmallInteger)
#     ADCP_BIN17_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN17_SPEED = Column(SmallInteger)
#     ADCP_BIN17_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN17_DIRECTION = Column(SmallInteger)
#     ADCP_BIN18_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN18_SPEED = Column(SmallInteger)
#     ADCP_BIN18_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN18_DIRECTION = Column(SmallInteger)
#     ADCP_BIN19_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN19_SPEED = Column(SmallInteger)
#     ADCP_BIN19_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN19_DIRECTION = Column(SmallInteger)
#     ADCP_BIN20_SPEED = Column(Numeric(4, 2))
#     flag_ADCP_BIN20_SPEED = Column(SmallInteger)
#     ADCP_BIN20_DIRECTION = Column(SmallInteger)
#     flag_ADCP_BIN20_DIRECTION = Column(SmallInteger)
#     ADCP_BIN1_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN2_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN3_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN4_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN5_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN6_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN7_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN8_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN9_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN10_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN11_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN12_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN13_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN14_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN15_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN16_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN17_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN18_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN19_DEPTH = Column(Numeric(4,2))
#     ADCP_BIN20_DEPTH = Column(Numeric(4,2))
#     ONDA_ALTURA_SENSOR1 = Column(Numeric(4, 2), comment='Sea Wave Height 1 - Altura Significativa de Onda, Sensor 1,')
#     flag_ONDA_ALTURA_SENSOR1 = Column(SmallInteger)
#     ONDA_PERIODO_SENSOR1 = Column(Numeric(4, 2), comment='Peak Period 1 - Período de Pico, sensor 1 (Triaxys), em segundos.')
#     flag_ONDA_PERIODO_SENSOR1 = Column(SmallInteger)
#     mxwvht1 = Column(Numeric(4, 2), comment='Maximum Wave Height 1 - Altura Máxima de Onda, sensor 1 (Triaxys), em metros.')
#     flag_mxwvht1 = Column(SmallInteger)
#     ONDA_DIRECAOMED_SENSOR1 = Column(SmallInteger, comment='Mean Wave Diretction 1 - Direção Média de Onda, sensor 1.')
#     flag_ONDA_DIRECAOMED_SENSOR1 = Column(SmallInteger)
#     wvspread1 = Column(SmallInteger, comment='Wave Spread 1 - Direção de Espalhamento de Onda, Sensor 1')
#     flag_wvspread1 = Column(SmallInteger)
#     ONDA_ALTURA_SENSOR2 = Column(Numeric(4, 2), comment='Sea Wave Height 2 - Altura Significativa de Onda, sensor 2 (UCMO - Nacional), em metros.')
#     flag_ONDA_ALTURA_SENSOR2 = Column(SmallInteger)
#     ONDA_PERIODO_SENSOR2 = Column(Numeric(4, 2), comment='Peak Period 2 - Período de Pico, sensor 2 (UCMO - Nacional), em segundos.')
#     flag_ONDA_PERIODO_SENSOR2 = Column(SmallInteger)
#     ONDA_DIRECAOMED_SENSOR2 = Column(SmallInteger, comment='Wave Peak Direction 2 - Direção de Pico Primário de Onda, sensor 2 (UCMO - Nacional), em graus.')
#     flag_ONDA_DIRECAOMED_SENSOR2 = Column(SmallInteger)
#     tm1 = Column(Numeric)
#     flag_tm1 = Column(SmallInteger)
#     pkdir1 = Column(Numeric)
#     flag_pkdir1 = Column(SmallInteger)
#     pkspread1 = Column(Numeric)
#     flag_pkspread1 = Column(SmallInteger)
#     sensors_data_flagged = Column(JSON)
#     cond = Column(Numeric)
#     flag_cond = Column(SmallInteger)
#     sss = Column(Numeric)
#     flag_sss = Column(SmallInteger)

#     buoy = relationship(Buoy, foreign_keys=[buoy_id])
