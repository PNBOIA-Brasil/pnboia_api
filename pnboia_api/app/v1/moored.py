import pandas as pd
import numpy as np

from typing import Optional, Any, List

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from pnboia_api.core.security import credentials_exception
from pnboia_api.schemas.moored import *
from pnboia_api.models.moored import *
import pnboia_api.crud as crud
from  pnboia_api.db.base import Base, SessionLocal, engine
from datetime import datetime, timedelta, date

from pnboia_api.app.deps import get_db

Base.metadata.create_all(bind=engine)

router = APIRouter()

#######################
# MOORED.BUOYS ENDPOINT
#######################

@router.get("/buoys/{buoy_id}", status_code=200, response_model=BuoyBase)
def buoy_show(
        *,
        buoy_id: int,
        token: str,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Fetch a single buoy by ID
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    result = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

    return result

@router.get("/buoys", status_code=200, response_model=List[BuoyBase])
def buoy_index(
        token: str,
        db: Session = Depends(get_db),
        status:Optional[bool]=None
    ) -> Any:   

    """
    Fetch a single buoy by ID
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    if status != None:
        arguments = {'status=': status}
    else:
        arguments = {}
    
    result = crud.crud_moored.buoy.index(db=db, arguments=arguments)

    return result

#######################
# MOORED.AXYSGENERAL ENDPOINT
#######################

@router.get("/axys_general", status_code=200, response_model=List[AxysGeneralBase])
def axys_general_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))
        
    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.axys_general.index(db=db, arguments=arguments)

    return result

#######################
# MOORED.BMOBRRAW ENDPOINT
#######################

@router.get("/bmobr_raw", status_code=200, response_model=List[BmobrRawBase])
def bmobr_raw_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))
        
    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.bmobr_raw.index(db=db, arguments=arguments)

    return result


#######################
# MOORED.BmobrTriaxysRaw ENDPOINT
#######################

@router.get("/bmobr_triaxys_raw", status_code=200, response_model=List[BmobrTriaxysRawBase])
def bmobr_triaxys_raw_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))
        
    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.bmobr_triaxys_raw.index(db=db, arguments=arguments)

    return result

#######################
# MOORED.SPOTTERALL ENDPOINT
#######################

@router.get("/spotter_all", status_code=200, response_model=List[SpotterAllBase])
def spotter_general_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))
        
    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.spotter_all.index(db=db, arguments=arguments)

    return result


#######################
# MOORED.SpotterSmartMooringConfig ENDPOINT
#######################

@router.get("/spotter_smart_mooring_config", status_code=200, response_model=List[SpotterSmartMooringConfigBase])
def spotter_smart_mooring_config_index(
        buoy_id: int,
        token: str,
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {'buoy_id=': buoy_id}

    print(arguments)

    result = crud.crud_moored.spotter_smart_mooring_config.index(db=db, arguments=arguments)

    return result

#######################
# MOORED.SpotterSystem ENDPOINT
#######################

@router.get("/spotter_system", status_code=200, response_model=List[SpotterSystemBase])
def spotter_system_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))
        
    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.spotter_system.index(db=db, arguments=arguments)

    return result


#######################
# MOORED.BmobrGeneral ENDPOINT
#######################

@router.get("/bmobr_general", status_code=200, response_model=List[BmobrGeneralBase])
def bmobr_general_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))
        
    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.bmobr_general.index(db=db, arguments=arguments)

    return result

