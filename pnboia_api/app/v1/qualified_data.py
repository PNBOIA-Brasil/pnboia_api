import pandas as pd
import numpy as np

from typing import Optional, Any, List
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from pnboia_api.schemas.qualified_data import *
from pnboia_api.schemas.qualified_data import QualifiedDataPetrobrasBase

from pnboia_api.models.qualified_data import *

import pnboia_api.crud as crud

from  pnboia_api.db.base import Base, engine
from datetime import datetime, timedelta, date

from pnboia_api.app.deps import get_db

from pnboia_api.app.utils import APIUtils

Base.metadata.create_all(bind=engine)

router = APIRouter()

#######################
# QUALIFIED_DATA.QualifiedData ENDPOINT
#######################

@router.get("/qualified_data", status_code=200, response_model=List[QualifiedDataBase])
def qualified_data_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-ddTHH:MM:SS",
            regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-ddTHH:MM:SS",
            regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        db: Session = Depends(get_db),
        flag: str = None,
        limit: int = None,
        order:Optional[bool]=True,
        response_type:str="json"
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    except:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 30:
        end_date = (start_date + timedelta(days=30))


    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%dT%H:%M:%S"), 'date_time<=': end_date.strftime("%Y-%m-%dT%H:%M:%S")}

    buoy = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

    if buoy.project_id == 2:
        if user.user_type not in ['admin', 'petrobras']:
            arguments['extract(hour from date_time)'] = ['in', [0, 3, 6, 9, 12, 15, 18, 21]]

    if not buoy.open_data and not user.user_type == 'admin':
        if not user.user_type == 'admin':
            raise HTTPException(
                status_code=400,
                detail="You do not have permission to do this action",
            )
    else:
        result = crud.crud_qualified_data.qualified_data.index(db=db, order=order, arguments=arguments, limit=limit)

    if flag:
        result_dict = []
        for r in result:
            result_dict.append(vars(r))
        result_df = pd.DataFrame(result_dict)
        column_flag = []
        for column in result_df.columns:
            if column[0:4] == "flag":
                column_flag.append(column.split("_")[1])
        for c in column_flag:
            if c not in ['latitude', 'longitude']:
                if flag == 'all':
                    result_df.loc[result_df[f"flag_{c}"]>0, f'{c}'] = np.nan
                elif flag == 'soft':
                    result_df.loc[(result_df[f"flag_{c}"]>0)&(result_df[f"flag_{c}"]<50), f'{c}'] = np.nan
        result_dict = result_df.to_dict(orient='records')
        for idx, r in enumerate(result):
            for key,value in result_dict[idx].items():
                if value == np.nan:
                    delattr(result[idx],key)
                    delattr(result[idx],f"flag_{key}")


    if response_type == "csv":
        filename = APIUtils().file_name_composition(buoy_name=buoy.name, start_date=start_date, end_date=end_date)
        return APIUtils().csv_response(result=result, filename=filename)
    elif response_type == "json":
        return result


@router.get("/petrobras", status_code=200, response_model=List[QualifiedDataPetrobrasBase])
def qualified_data_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(datetime.utcnow() - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S"),
            title="date_time format is yyyy-mm-ddTHH:MM:SS",
            regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        end_date: Optional[str] = Query(default=(datetime.utcnow() + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S"),
            title="date_time format is yyyy-mm-ddTHH:MM:SS",
            regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        db: Session = Depends(get_db),
        flag: str = None,
        limit: int = None,
        order:Optional[bool]=True,
        last: bool = False,
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
    end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")


    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))

    print(start_date)
    print(end_date)

    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%dT%H:%M:%S"), 'date_time<=': end_date.strftime("%Y-%m-%dT%H:%M:%S")}

    buoy = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

    if buoy.project_id == 2:
        if user.user_type not in ['admin', 'petrobras']:
            arguments['extract(hour from date_time)'] = ['in', [0, 3, 6, 9, 12, 15, 18, 21]]

    if not buoy.open_data and not user.user_type == 'admin':
        if not user.user_type == 'admin':
            raise HTTPException(
                status_code=400,
                detail="You do not have permission to do this action",
            )
    else:
        result = crud.crud_qualified_data.qualified_data.index(db=db, order=order, arguments=arguments, limit=limit)


    if flag:
        result_dict = []
        for r in result:
            result_dict.append(vars(r))
        result_df = pd.DataFrame(result_dict)
        column_flag = []
        for column in result_df.columns:
            if column[0:4] == "flag":
                column_flag.append(column.split("_")[1])
        for c in column_flag:
            if c not in ['latitude', 'longitude']:
                if flag == 'all':
                    result_df.loc[result_df[f"flag_{c}"]>0, f'{c}'] = np.nan
                elif flag == 'soft':
                    result_df.loc[(result_df[f"flag_{c}"]>0)&(result_df[f"flag_{c}"]<50), f'{c}'] = np.nan
        result_dict = result_df.to_dict(orient='records')
        for idx, r in enumerate(result):
            for key,value in result_dict[idx].items():
                if value == np.nan:
                    delattr(result[idx],key)
                    delattr(result[idx],f"flag_{key}")

    result1 = []
    for r in result:
        r1 =  QualifiedDataPetrobrasBase()
        r1.HMS_HUMIDITY = r.rh
        r1.flag_HMS_HUMIDITY = r.flag_rh
        r1.HMS_PRESSURE = r.pres
        r1.flag_HMS_PRESSURE = r.flag_pres
        r1.HMS_TEMPERATURE = r.atmp
        r1.flag_HMS_TEMPERATURE = r.flag_atmp
        r1.HMS_WIND_SPEED1 = r.wspd1
        r1.flag_HMS_WIND_SPEED1 = r.flag_wspd1
        r1.HMS_WIND_DIRECTION1 = r.wdir1
        r1.flag_HMS_WIND_DIRECTION1 = r.flag_wdir1
        r1.HMS_WIND_SPEED2 = r.wspd2
        r1.flag_HMS_WIND_SPEED2 = r.flag_wspd2
        r1.HMS_WIND_DIRECTION2 = r.wdir2
        r1.flag_HMS_WIND_DIRECTION2 = r.flag_wdir2
        r1.TEMPERATURA_AGUA = r.sst
        r1.flag_TEMPERATURA_AGUA = r.flag_sst
        r1.ADCP_BIN1_SPEED = r.cspd1
        r1.flag_ADCP_BIN1_SPEED = r.flag_cspd1
        r1.ADCP_BIN1_DIRECTION = r.cdir1
        r1.flag_ADCP_BIN1_DIRECTION = r.flag_cdir1
        r1.ADCP_BIN2_SPEED = r.cspd2
        r1.flag_ADCP_BIN2_SPEED = r.flag_cspd2
        r1.ADCP_BIN2_DIRECTION = r.cdir2
        r1.flag_ADCP_BIN2_DIRECTION = r.flag_cdir2
        r1.ADCP_BIN3_SPEED = r.cspd3
        r1.flag_ADCP_BIN3_SPEED = r.flag_cspd3
        r1.ADCP_BIN3_DIRECTION = r.cdir3
        r1.flag_ADCP_BIN3_DIRECTION = r.flag_cdir3
        r1.ADCP_BIN4_SPEED = r.cspd4
        r1.flag_ADCP_BIN4_SPEED = r.flag_cspd4
        r1.ADCP_BIN4_DIRECTION = r.cdir4
        r1.flag_ADCP_BIN4_DIRECTION = r.flag_cdir4
        r1.ADCP_BIN5_SPEED = r.cspd5
        r1.flag_ADCP_BIN5_SPEED = r.flag_cspd5
        r1.ADCP_BIN5_DIRECTION = r.cdir5
        r1.flag_ADCP_BIN5_DIRECTION = r.flag_cdir5
        r1.ADCP_BIN6_SPEED = r.cspd6
        r1.flag_ADCP_BIN6_SPEED = r.flag_cspd6
        r1.ADCP_BIN6_DIRECTION = r.cdir6
        r1.flag_ADCP_BIN6_DIRECTION = r.flag_cdir6
        r1.ADCP_BIN7_SPEED = r.cspd7
        r1.flag_ADCP_BIN7_SPEED = r.flag_cspd7
        r1.ADCP_BIN7_DIRECTION = r.cdir7
        r1.flag_ADCP_BIN7_DIRECTION = r.flag_cdir7
        r1.ADCP_BIN8_SPEED = r.cspd8
        r1.flag_ADCP_BIN8_SPEED = r.flag_cspd8
        r1.ADCP_BIN8_DIRECTION = r.cdir8
        r1.flag_ADCP_BIN8_DIRECTION = r.flag_cdir8
        r1.ADCP_BIN9_SPEED = r.cspd9
        r1.flag_ADCP_BIN9_SPEED = r.flag_cspd9
        r1.ADCP_BIN9_DIRECTION = r.cdir9
        r1.flag_ADCP_BIN9_DIRECTION = r.flag_cdir9
        r1.ADCP_BIN10_SPEED = r.cspd10
        r1.flag_ADCP_BIN10_SPEED = r.flag_cspd10
        r1.ADCP_BIN10_DIRECTION = r.cdir10
        r1.flag_ADCP_BIN10_DIRECTION = r.flag_cdir10
        r1.ADCP_BIN11_SPEED = r.cspd11
        r1.flag_ADCP_BIN11_SPEED = r.flag_cspd11
        r1.ADCP_BIN11_DIRECTION = r.cdir11
        r1.flag_ADCP_BIN11_DIRECTION = r.flag_cdir11
        r1.ADCP_BIN12_SPEED = r.cspd12
        r1.flag_ADCP_BIN12_SPEED = r.flag_cspd12
        r1.ADCP_BIN12_DIRECTION = r.cdir12
        r1.flag_ADCP_BIN12_DIRECTION = r.flag_cdir12
        r1.ADCP_BIN13_SPEED = r.cspd13
        r1.flag_ADCP_BIN13_SPEED = r.flag_cspd13
        r1.ADCP_BIN13_DIRECTION = r.cdir13
        r1.flag_ADCP_BIN13_DIRECTION = r.flag_cdir13
        r1.ADCP_BIN14_SPEED = r.cspd14
        r1.flag_ADCP_BIN14_SPEED = r.flag_cspd14
        r1.ADCP_BIN14_DIRECTION = r.cdir14
        r1.flag_ADCP_BIN14_DIRECTION = r.flag_cdir14
        r1.ADCP_BIN15_SPEED = r.cspd15
        r1.flag_ADCP_BIN15_SPEED = r.flag_cspd15
        r1.ADCP_BIN15_DIRECTION = r.cdir15
        r1.flag_ADCP_BIN15_DIRECTION = r.flag_cdir15
        r1.ADCP_BIN16_SPEED = r.cspd16
        r1.flag_ADCP_BIN16_SPEED = r.flag_cspd16
        r1.ADCP_BIN16_DIRECTION = r.cdir16
        r1.flag_ADCP_BIN16_DIRECTION = r.flag_cdir16
        r1.ADCP_BIN17_SPEED = r.cspd17
        r1.flag_ADCP_BIN17_SPEED = r.flag_cspd17
        r1.ADCP_BIN17_DIRECTION = r.cdir17
        r1.flag_ADCP_BIN17_DIRECTION = r.flag_cdir17
        r1.ADCP_BIN18_SPEED = r.cspd18
        r1.flag_ADCP_BIN18_SPEED = r.flag_cspd18
        r1.ADCP_BIN18_DIRECTION = r.cdir18
        r1.flag_ADCP_BIN18_DIRECTION = r.flag_cdir18
        r1.ADCP_BIN19_SPEED = r.cspd19
        r1.flag_ADCP_BIN19_SPEED = r.flag_cspd19
        r1.ADCP_BIN19_DIRECTION = r.cdir19
        r1.flag_ADCP_BIN19_DIRECTION = r.flag_cdir19
        r1.ADCP_BIN20_SPEED = r.cspd20
        r1.flag_ADCP_BIN20_SPEED = r.flag_cspd20
        r1.ADCP_BIN20_DIRECTION = r.cdir20
        r1.flag_ADCP_BIN20_DIRECTION = r.flag_cdir20
        if r.buoy_id in (2,36):
            r1.ADCP_BIN1_DEPTH = 5.0
            r1.ADCP_BIN2_DEPTH = 8.5
            r1.ADCP_BIN3_DEPTH = 12.0
            r1.ADCP_BIN4_DEPTH = 15.5
            r1.ADCP_BIN5_DEPTH = 19.0
            r1.ADCP_BIN6_DEPTH = 22.5
            r1.ADCP_BIN7_DEPTH = 26.0
            r1.ADCP_BIN8_DEPTH = 29.5
            r1.ADCP_BIN9_DEPTH = 33.0
            r1.ADCP_BIN10_DEPTH = 36.5
            r1.ADCP_BIN11_DEPTH = 40.0
            r1.ADCP_BIN12_DEPTH = 43.5
            r1.ADCP_BIN13_DEPTH = 47.0
            r1.ADCP_BIN14_DEPTH = 50.5
            r1.ADCP_BIN15_DEPTH = 54.0
            r1.ADCP_BIN16_DEPTH = 57.5
            r1.ADCP_BIN17_DEPTH = 61.0
            r1.ADCP_BIN18_DEPTH = 64.5
            r1.ADCP_BIN19_DEPTH = 68.0
            r1.ADCP_BIN20_DEPTH = 71.5
        elif r.buoy_id in (22,37):
            r1.ADCP_BIN1_DEPTH = 1.5
            r1.ADCP_BIN2_DEPTH = 5.0
            r1.ADCP_BIN3_DEPTH = 8.5
            r1.ADCP_BIN4_DEPTH = 12.0
            r1.ADCP_BIN5_DEPTH = 15.5
            r1.ADCP_BIN6_DEPTH = 19.0
            r1.ADCP_BIN7_DEPTH = 22.5
            r1.ADCP_BIN8_DEPTH = 26.0
            r1.ADCP_BIN9_DEPTH = 29.5
            r1.ADCP_BIN10_DEPTH = 33.0
            r1.ADCP_BIN11_DEPTH = 36.5
            r1.ADCP_BIN12_DEPTH = 40.0
            r1.ADCP_BIN13_DEPTH = 43.5
            r1.ADCP_BIN14_DEPTH = 47.0
            r1.ADCP_BIN15_DEPTH = 50.5
            r1.ADCP_BIN16_DEPTH = 54.0
            r1.ADCP_BIN17_DEPTH = 57.5
            r1.ADCP_BIN18_DEPTH = 61.0
            r1.ADCP_BIN19_DEPTH = 64.5
            r1.ADCP_BIN20_DEPTH = 68.0
        r1.ONDA_ALTURA_SENSOR1 = r.swvht1
        r1.flag_ONDA_ALTURA_SENSOR1 = r.flag_swvht1
        r1.ONDA_PERIODO_SENSOR1 = r.tp1
        r1.flag_ONDA_PERIODO_SENSOR1 = r.flag_tp1
        r1.ONDA_DIRECAOMED_SENSOR1 = r.wvdir1
        r1.flag_ONDA_DIRECAOMED_SENSOR1 = r.flag_wvdir1
        r1.ONDA_ALTURA_SENSOR2 = r.swvht2
        r1.flag_ONDA_ALTURA_SENSOR2 = r.flag_swvht2
        r1.ONDA_PERIODO_SENSOR2 = r.tp2
        r1.flag_ONDA_PERIODO_SENSOR2 = r.flag_tp2
        r1.ONDA_DIRECAOMED_SENSOR2 = r.wvdir2
        r1.flag_ONDA_DIRECAOMED_SENSOR2 = r.flag_wvdir2
        r1.Timestamp = int(r.date_time.timestamp()*1000)
        r1.id = r.id
        # r1.raw_id = r.raw_id
        r1.buoy_id = r.buoy_id
        r1.date_time = r.date_time
        r1.latitude = r.latitude
        r1.longitude = r.longitude
        # r1.geom = r.geom
        r1.battery = r.battery
        r1.flag_battery = r.flag_battery
        r1.HMS_WIND_RAJADA1 = r.gust1
        r1.flag_HMS_WIND_RAJADA1 = r.flag_gust1
        r1.HMS_WIND_RAJADA2 = r.gust2
        r1.flag_HMS_WIND_RAJADA2 = r.flag_gust2
        # r1.srad = r.srad
        # r1.flag_srad = r.flag_srad
        # r1.dewpt = r.dewpt
        # r1.flag_dewpt = r.flag_dewpt
        r1.ONDA_ALTURAMAX_SENSOR1 = r.mxwvht1
        r1.flag_ONDA_ALTURAMAX_SENSOR1 = r.flag_mxwvht1
        r1.ONDA_ESPALHAMENTO1 = r.wvspread1
        r1.flag_ONDA_ESPALHAMENTO1 = r.flag_wvspread1
        # r1.tm1 = r.tm1
        # r1.flag_tm1 = r.flag_tm1
        # r1.pkdir1 = r.pkdir1
        # r1.flag_pkdir1 = r.flag_pkdir1
        # r1.pkspread1 = r.pkspread1
        # r1.flag_pkspread1 = r.flag_pkspread1
        # r1.sensors_data_flagged = r.sensors_data_flagged
        # r1.cond = r.cond
        # r1.flag_cond = r.flag_cond
        # r1.sss = r.sss
        # r1.flag_sss = r.flag_sss

        result1.append(r1)

    return result1




@router.get("/petrobras/last", status_code=200, response_model=List[QualifiedDataPetrobrasBase])
def qualified_data_last(
        token: str,
        buoy_id:int = None,
        db: Session = Depends(get_db),
        last: bool = True,
        open_data: bool = False,
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {'buoy_id=': buoy_id}

    if open_data:
        arguments['open_data='] = True

    result = crud.crud_qualified_data.qualified_data.last(db=db, arguments=arguments, last=last, buoy_sel=True)

    result1 = []
    for r in result:
        r1 =  QualifiedDataPetrobrasBase()
        r1.HMS_HUMIDITY = r.rh
        r1.flag_HMS_HUMIDITY = r.flag_rh
        r1.HMS_PRESSURE = r.pres
        r1.flag_HMS_PRESSURE = r.flag_pres
        r1.HMS_TEMPERATURE = r.atmp
        r1.flag_HMS_TEMPERATURE = r.flag_atmp
        r1.HMS_WIND_SPEED1 = r.wspd1
        r1.flag_HMS_WIND_SPEED1 = r.flag_wspd1
        r1.HMS_WIND_DIRECTION1 = r.wdir1
        r1.flag_HMS_WIND_DIRECTION1 = r.flag_wdir1
        r1.HMS_WIND_SPEED2 = r.wspd2
        r1.flag_HMS_WIND_SPEED2 = r.flag_wspd2
        r1.HMS_WIND_DIRECTION2 = r.wdir2
        r1.flag_HMS_WIND_DIRECTION2 = r.flag_wdir2
        r1.TEMPERATURA_AGUA = r.sst
        r1.flag_TEMPERATURA_AGUA = r.flag_sst
        r1.ADCP_BIN1_SPEED = r.cspd1
        r1.flag_ADCP_BIN1_SPEED = r.flag_cspd1
        r1.ADCP_BIN1_DIRECTION = r.cdir1
        r1.flag_ADCP_BIN1_DIRECTION = r.flag_cdir1
        r1.ADCP_BIN2_SPEED = r.cspd2
        r1.flag_ADCP_BIN2_SPEED = r.flag_cspd2
        r1.ADCP_BIN2_DIRECTION = r.cdir2
        r1.flag_ADCP_BIN2_DIRECTION = r.flag_cdir2
        r1.ADCP_BIN3_SPEED = r.cspd3
        r1.flag_ADCP_BIN3_SPEED = r.flag_cspd3
        r1.ADCP_BIN3_DIRECTION = r.cdir3
        r1.flag_ADCP_BIN3_DIRECTION = r.flag_cdir3
        r1.ADCP_BIN4_SPEED = r.cspd4
        r1.flag_ADCP_BIN4_SPEED = r.flag_cspd4
        r1.ADCP_BIN4_DIRECTION = r.cdir4
        r1.flag_ADCP_BIN4_DIRECTION = r.flag_cdir4
        r1.ADCP_BIN5_SPEED = r.cspd5
        r1.flag_ADCP_BIN5_SPEED = r.flag_cspd5
        r1.ADCP_BIN5_DIRECTION = r.cdir5
        r1.flag_ADCP_BIN5_DIRECTION = r.flag_cdir5
        r1.ADCP_BIN6_SPEED = r.cspd6
        r1.flag_ADCP_BIN6_SPEED = r.flag_cspd6
        r1.ADCP_BIN6_DIRECTION = r.cdir6
        r1.flag_ADCP_BIN6_DIRECTION = r.flag_cdir6
        r1.ADCP_BIN7_SPEED = r.cspd7
        r1.flag_ADCP_BIN7_SPEED = r.flag_cspd7
        r1.ADCP_BIN7_DIRECTION = r.cdir7
        r1.flag_ADCP_BIN7_DIRECTION = r.flag_cdir7
        r1.ADCP_BIN8_SPEED = r.cspd8
        r1.flag_ADCP_BIN8_SPEED = r.flag_cspd8
        r1.ADCP_BIN8_DIRECTION = r.cdir8
        r1.flag_ADCP_BIN8_DIRECTION = r.flag_cdir8
        r1.ADCP_BIN9_SPEED = r.cspd9
        r1.flag_ADCP_BIN9_SPEED = r.flag_cspd9
        r1.ADCP_BIN9_DIRECTION = r.cdir9
        r1.flag_ADCP_BIN9_DIRECTION = r.flag_cdir9
        r1.ADCP_BIN10_SPEED = r.cspd10
        r1.flag_ADCP_BIN10_SPEED = r.flag_cspd10
        r1.ADCP_BIN10_DIRECTION = r.cdir10
        r1.flag_ADCP_BIN10_DIRECTION = r.flag_cdir10
        r1.ADCP_BIN11_SPEED = r.cspd11
        r1.flag_ADCP_BIN11_SPEED = r.flag_cspd11
        r1.ADCP_BIN11_DIRECTION = r.cdir11
        r1.flag_ADCP_BIN11_DIRECTION = r.flag_cdir11
        r1.ADCP_BIN12_SPEED = r.cspd12
        r1.flag_ADCP_BIN12_SPEED = r.flag_cspd12
        r1.ADCP_BIN12_DIRECTION = r.cdir12
        r1.flag_ADCP_BIN12_DIRECTION = r.flag_cdir12
        r1.ADCP_BIN13_SPEED = r.cspd13
        r1.flag_ADCP_BIN13_SPEED = r.flag_cspd13
        r1.ADCP_BIN13_DIRECTION = r.cdir13
        r1.flag_ADCP_BIN13_DIRECTION = r.flag_cdir13
        r1.ADCP_BIN14_SPEED = r.cspd14
        r1.flag_ADCP_BIN14_SPEED = r.flag_cspd14
        r1.ADCP_BIN14_DIRECTION = r.cdir14
        r1.flag_ADCP_BIN14_DIRECTION = r.flag_cdir14
        r1.ADCP_BIN15_SPEED = r.cspd15
        r1.flag_ADCP_BIN15_SPEED = r.flag_cspd15
        r1.ADCP_BIN15_DIRECTION = r.cdir15
        r1.flag_ADCP_BIN15_DIRECTION = r.flag_cdir15
        r1.ADCP_BIN16_SPEED = r.cspd16
        r1.flag_ADCP_BIN16_SPEED = r.flag_cspd16
        r1.ADCP_BIN16_DIRECTION = r.cdir16
        r1.flag_ADCP_BIN16_DIRECTION = r.flag_cdir16
        r1.ADCP_BIN17_SPEED = r.cspd17
        r1.flag_ADCP_BIN17_SPEED = r.flag_cspd17
        r1.ADCP_BIN17_DIRECTION = r.cdir17
        r1.flag_ADCP_BIN17_DIRECTION = r.flag_cdir17
        r1.ADCP_BIN18_SPEED = r.cspd18
        r1.flag_ADCP_BIN18_SPEED = r.flag_cspd18
        r1.ADCP_BIN18_DIRECTION = r.cdir18
        r1.flag_ADCP_BIN18_DIRECTION = r.flag_cdir18
        r1.ADCP_BIN19_SPEED = r.cspd19
        r1.flag_ADCP_BIN19_SPEED = r.flag_cspd19
        r1.ADCP_BIN19_DIRECTION = r.cdir19
        r1.flag_ADCP_BIN19_DIRECTION = r.flag_cdir19
        r1.ADCP_BIN20_SPEED = r.cspd20
        r1.flag_ADCP_BIN20_SPEED = r.flag_cspd20
        r1.ADCP_BIN20_DIRECTION = r.cdir20
        r1.flag_ADCP_BIN20_DIRECTION = r.flag_cdir20
        if r.buoy_id in (2,36):
            r1.ADCP_BIN1_DEPTH = 5.0
            r1.ADCP_BIN2_DEPTH = 8.5
            r1.ADCP_BIN3_DEPTH = 12.0
            r1.ADCP_BIN4_DEPTH = 15.5
            r1.ADCP_BIN5_DEPTH = 19.0
            r1.ADCP_BIN6_DEPTH = 22.5
            r1.ADCP_BIN7_DEPTH = 26.0
            r1.ADCP_BIN8_DEPTH = 29.5
            r1.ADCP_BIN9_DEPTH = 33.0
            r1.ADCP_BIN10_DEPTH = 36.5
            r1.ADCP_BIN11_DEPTH = 40.0
            r1.ADCP_BIN12_DEPTH = 43.5
            r1.ADCP_BIN13_DEPTH = 47.0
            r1.ADCP_BIN14_DEPTH = 50.5
            r1.ADCP_BIN15_DEPTH = 54.0
            r1.ADCP_BIN16_DEPTH = 57.5
            r1.ADCP_BIN17_DEPTH = 61.0
            r1.ADCP_BIN18_DEPTH = 64.5
            r1.ADCP_BIN19_DEPTH = 68.0
            r1.ADCP_BIN20_DEPTH = 71.5
        elif r.buoy_id in (22,37):
            r1.ADCP_BIN1_DEPTH = 1.5
            r1.ADCP_BIN2_DEPTH = 5.0
            r1.ADCP_BIN3_DEPTH = 8.5
            r1.ADCP_BIN4_DEPTH = 12.0
            r1.ADCP_BIN5_DEPTH = 15.5
            r1.ADCP_BIN6_DEPTH = 19.0
            r1.ADCP_BIN7_DEPTH = 22.5
            r1.ADCP_BIN8_DEPTH = 26.0
            r1.ADCP_BIN9_DEPTH = 29.5
            r1.ADCP_BIN10_DEPTH = 33.0
            r1.ADCP_BIN11_DEPTH = 36.5
            r1.ADCP_BIN12_DEPTH = 40.0
            r1.ADCP_BIN13_DEPTH = 43.5
            r1.ADCP_BIN14_DEPTH = 47.0
            r1.ADCP_BIN15_DEPTH = 50.5
            r1.ADCP_BIN16_DEPTH = 54.0
            r1.ADCP_BIN17_DEPTH = 57.5
            r1.ADCP_BIN18_DEPTH = 61.0
            r1.ADCP_BIN19_DEPTH = 64.5
            r1.ADCP_BIN20_DEPTH = 68.0
        r1.ONDA_ALTURA_SENSOR1 = r.swvht1
        r1.flag_ONDA_ALTURA_SENSOR1 = r.flag_swvht1
        r1.ONDA_PERIODO_SENSOR1 = r.tp1
        r1.flag_ONDA_PERIODO_SENSOR1 = r.flag_tp1
        r1.ONDA_DIRECAOMED_SENSOR1 = r.wvdir1
        r1.flag_ONDA_DIRECAOMED_SENSOR1 = r.flag_wvdir1
        r1.ONDA_ALTURA_SENSOR2 = r.swvht2
        r1.flag_ONDA_ALTURA_SENSOR2 = r.flag_swvht2
        r1.ONDA_PERIODO_SENSOR2 = r.tp2
        r1.flag_ONDA_PERIODO_SENSOR2 = r.flag_tp2
        r1.ONDA_DIRECAOMED_SENSOR2 = r.wvdir2
        r1.flag_ONDA_DIRECAOMED_SENSOR2 = r.flag_wvdir2
        r1.Timestamp = int(r.date_time.timestamp()*1000)
        r1.id = r.id
        # r1.raw_id = r.raw_id
        r1.buoy_id = r.buoy_id
        r1.date_time = r.date_time
        r1.latitude = r.latitude
        r1.longitude = r.longitude
        # r1.geom = r.geom
        r1.battery = r.battery
        r1.flag_battery = r.flag_battery
        r1.HMS_WIND_RAJADA1 = r.gust1
        r1.flag_HMS_WIND_RAJADA1 = r.flag_gust1
        r1.HMS_WIND_RAJADA2 = r.gust2
        r1.flag_HMS_WIND_RAJADA2 = r.flag_gust2
        # r1.srad = r.srad
        # r1.flag_srad = r.flag_srad
        # r1.dewpt = r.dewpt
        # r1.flag_dewpt = r.flag_dewpt
        r1.ONDA_ALTURAMAX_SENSOR1 = r.mxwvht1
        r1.flag_ONDA_ALTURAMAX_SENSOR1 = r.flag_mxwvht1
        r1.ONDA_ESPALHAMENTO1 = r.wvspread1
        r1.flag_ONDA_ESPALHAMENTO1 = r.flag_wvspread1
        # r1.tm1 = r.tm1
        # r1.flag_tm1 = r.flag_tm1
        # r1.pkdir1 = r.pkdir1
        # r1.flag_pkdir1 = r.flag_pkdir1
        # r1.pkspread1 = r.pkspread1
        # r1.flag_pkspread1 = r.flag_pkspread1
        # r1.sensors_data_flagged = r.sensors_data_flagged
        # r1.cond = r.cond
        # r1.flag_cond = r.flag_cond
        # r1.sss = r.sss
        # r1.flag_sss = r.flag_sss

        result1.append(r1)

    return result1


@router.get("/qualified_data/last", status_code=200, response_model=List[QualifiedDataPetrobrasBase])
def qualified_data_last(
        token: str,
        db: Session = Depends(get_db),
        last: bool = True,
        open_data: bool = False,
        buoy_id:int = None,
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}

    if open_data:
        arguments['open_data='] = True

    result = crud.crud_qualified_data.qualified_data.last(db=db, arguments=arguments, last=last)

    return result



@router.get("/spotter", status_code=200, response_model=List[SpotterQualifiedSchema])
def qualified_data_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(datetime.utcnow().replace(microsecond=0) - timedelta(days=1)),
                    title="date_time format is yyyy-mm-ddTHH:MM:SS",
                    regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        end_date: Optional[str] = Query(default=(datetime.utcnow().replace(microsecond=0) + timedelta(days=2)),
                    title="date_time format is yyyy-mm-ddTHH:MM:SS",
                    regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        db: Session = Depends(get_db),
        flag: str = None,
        limit: int = None,
        order:Optional[bool]=True
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    # try:
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    except:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

    if end_date < start_date:
        raise HTTPException(
                status_code=400,
                detail="Provided start date is more recent then the end date.",
            )

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 100:
        start_date = (end_date - timedelta(days=100))


    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    buoy = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

    if "SPOTTER" not in buoy.name:
        raise HTTPException(
                status_code=400,
                detail=f"Please check in the PNBoia documentation if the correct endpoint is being used for the required buoy (Buoy ID = {buoy_id}).",
            )

    # if buoy.project_id == 2:
    #     if user.user_type not in ['admin', 'petrobras']:
    #         arguments['extract(hour from date_time)'] = ['in', [0, 3, 6, 9, 12, 15, 18, 21]]

    if not buoy.open_data and not user.user_type == 'admin':
        if not user.user_type == 'admin':
            raise HTTPException(
                status_code=400,
                detail="You do not have permission to do this action",
            )
    else:
        result = crud.crud_qualified_data.spotter_qualified_data.index(db=db, order=order, arguments=arguments, limit=limit)

    if flag:
        result_dict = []
        for r in result:
            result_dict.append(vars(r))
        result_df = pd.DataFrame(result_dict)
        column_flag = []
        for column in result_df.columns:
            if column[0:4] == "flag":
                column_flag.append(column.split("_")[1])
        for c in column_flag:
            if c not in ['latitude', 'longitude']:
                if flag == 'all':
                    result_df.loc[result_df[f"flag_{c}"]>0, f'{c}'] = np.nan
                elif flag == 'soft':
                    result_df.loc[(result_df[f"flag_{c}"]>0)&(result_df[f"flag_{c}"]<50), f'{c}'] = np.nan
        result_dict = result_df.to_dict(orient='records')
        for idx, r in enumerate(result):
            for key,value in result_dict[idx].items():
                if value == np.nan:
                    delattr(result[idx],key)
                    delattr(result[idx],f"flag_{key}")

    if not result:
        raise HTTPException(
                status_code=400,
                detail=f"No data for buoy {buoy_id} for the period.",
            )

    return result


@router.get("/triaxys", status_code=200, response_model=List[TriaxysQualifiedSchema])
def qualified_data_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(datetime.utcnow().replace(microsecond=0) - timedelta(days=1)),
                    title="date_time format is yyyy-mm-ddTHH:MM:SS",
                    regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        end_date: Optional[str] = Query(default=(datetime.utcnow().replace(microsecond=0) + timedelta(days=2)),
                    title="date_time format is yyyy-mm-ddTHH:MM:SS",
                    regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        db: Session = Depends(get_db),
        flag: str = None,
        limit: int = None,
        order:Optional[bool]=True
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    except:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

    if end_date < start_date:
        raise HTTPException(
                status_code=400,
                detail="Provided start date is more recent then the end date.",
            )

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 100:
        start_date = (end_date - timedelta(days=100))


    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    buoy = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

    if "TRIAXYS" not in buoy.name:
        raise HTTPException(
                status_code=400,
                detail=f"Please check in the PNBoia documentation if the correct endpoint is being used for the required buoy (Buoy ID = {buoy_id}).",
            )

    # if buoy.project_id == 2:
    #     if user.user_type not in ['admin', 'petrobras']:
    #         arguments['extract(hour from date_time)'] = ['in', [0, 3, 6, 9, 12, 15, 18, 21]]

    if not buoy.open_data and not user.user_type == 'admin':
        if not user.user_type == 'admin':
            raise HTTPException(
                status_code=400,
                detail="You do not have permission to do this action",
            )
    else:
        result = crud.crud_qualified_data.triaxys_qualified_data.index(db=db, order=order, arguments=arguments, limit=limit)

    if flag:
        result_dict = []
        for r in result:
            result_dict.append(vars(r))
        result_df = pd.DataFrame(result_dict)
        column_flag = []
        for column in result_df.columns:
            if column[0:4] == "flag":
                column_flag.append(column.split("_")[1])
        for c in column_flag:
            if c not in ['latitude', 'longitude']:
                if flag == 'all':
                    result_df.loc[result_df[f"flag_{c}"]>0, f'{c}'] = np.nan
                elif flag == 'soft':
                    result_df.loc[(result_df[f"flag_{c}"]>0)&(result_df[f"flag_{c}"]<50), f'{c}'] = np.nan
        result_dict = result_df.to_dict(orient='records')
        for idx, r in enumerate(result):
            for key,value in result_dict[idx].items():
                if value == np.nan:
                    delattr(result[idx],key)
                    delattr(result[idx],f"flag_{key}")

    if not result:
        raise HTTPException(
                status_code=400,
                detail=f"No data for buoy {buoy_id} for the period.",
            )

    return result


@router.get("/bmobr", status_code=200, response_model=List[BMOBrQualifiedSchema])
def qualified_data_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(datetime.utcnow().replace(microsecond=0) - timedelta(days=1)),
                    title="date_time format is yyyy-mm-ddTHH:MM:SS",
                    regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        end_date: Optional[str] = Query(default=(datetime.utcnow().replace(microsecond=0) + timedelta(days=2)),
                    title="date_time format is yyyy-mm-ddTHH:MM:SS",
                    regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
        db: Session = Depends(get_db),
        flag: str = None,
        limit: int = None,
        order:Optional[bool]=True
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
    except:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())

    if end_date < start_date:
        raise HTTPException(
                status_code=400,
                detail="Provided start date is more recent then the end date.",
            )

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 100:
        start_date = (end_date - timedelta(days=100))


    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    buoy = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

    if "METOCEAN" not in buoy.name:
        raise HTTPException(
                status_code=400,
                detail=f"Please check in the PNBoia documentation if the correct endpoint is being used for the required buoy (Buoy ID = {buoy_id}).",
            )

    if buoy.project_id == 2:
        if user.user_type not in ['admin', 'petrobras']:
            arguments['extract(hour from date_time)'] = ['in', [0, 3, 6, 9, 12, 15, 18, 21]]

    if not buoy.open_data and not user.user_type == 'admin':
        if not user.user_type == 'admin':
            raise HTTPException(
                status_code=400,
                detail="You do not have permission to do this action",
            )
    else:
        result = crud.crud_qualified_data.bmobr_qualified_data.index(db=db, order=order, arguments=arguments, limit=limit)

    if flag:
        result_dict = []
        for r in result:
            result_dict.append(vars(r))
        result_df = pd.DataFrame(result_dict)
        column_flag = []
        for column in result_df.columns:
            if column[0:4] == "flag":
                column_flag.append(column.split("_")[1])
        for c in column_flag:
            if c not in ['latitude', 'longitude']:
                if flag == 'all':
                    result_df.loc[result_df[f"flag_{c}"]>0, f'{c}'] = np.nan
                elif flag == 'soft':
                    result_df.loc[(result_df[f"flag_{c}"]>0)&(result_df[f"flag_{c}"]<50), f'{c}'] = np.nan
        result_dict = result_df.to_dict(orient='records')
        for idx, r in enumerate(result):
            for key,value in result_dict[idx].items():
                if value == np.nan:
                    delattr(result[idx],key)
                    delattr(result[idx],f"flag_{key}")

    if not result:
        raise HTTPException(
                status_code=400,
                detail=f"No data for buoy {buoy_id} for the period.",
            )

    return result
