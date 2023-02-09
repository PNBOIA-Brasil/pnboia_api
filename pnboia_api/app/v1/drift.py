import pandas as pd
import numpy as np

from typing import Optional, Any, List

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from pnboia_api.core.security import credentials_exception
from pnboia_api.schemas.drift import *
from pnboia_api.models.drift import *
import pnboia_api.crud as crud
from  pnboia_api.db.base import Base, engine
from datetime import datetime, timedelta, date

from pnboia_api.app.deps import get_db



Base.metadata.create_all(bind=engine)

router = APIRouter()



#######################
# DRIFT.BUOYS ENDPOINT
#######################

@router.get("/buoys/{buoy_id}", status_code=200, response_model=BuoyDriftBase)
def buoy_show(
        *,
        buoy_id: int,
        token: str,
        db: Session = Depends(get_db),
    ) -> Any:
    """
    Fetch a single buoy by ID
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})
    
    result = crud.crud_drift.buoy_drift.show(db=db, id_pk = buoy_id)

    return result

@router.get("/buoys", status_code=200, response_model=List[BuoyDriftBase])
def buoy_index(
        token: str,
        db: Session = Depends(get_db)
    ) -> Any:   

    """
    Fetch a single buoy by ID
    """    

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    result = crud.crud_drift.buoy_drift.index(db=db)

    return result



@router.post("/buoys", response_model=BuoyDriftBase, status_code=201)
def buoy_create(
        token: str,
        buoy_in: BuoyDriftNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create new buoy
    """
    
    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    
    result = crud.crud_drift.buoy_drift.index(db=db, arguments = {'antenna_id=': buoy_in.antenna_id})

    if result:
        raise HTTPException(
            status_code=400,
            detail="There is already a buoy with this name",
        )

    result = crud.crud_drift.buoy_drift.create(db=db, obj_in=buoy_in)

    return result

@router.put("/buoys/{buoy_id}", response_model=BuoyDriftBase, status_code=201)
def buoy_update(
        *,
        buoy_id: int,
        token: str,
        buoy_in: BuoyDriftNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create new buoy
    """
    
    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    result = crud.crud_drift.buoy_drift.index(db=db, arguments = {'buoy_id=': buoy_id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no buoy with this id",
        )

    result = crud.crud_drift.buoy_drift.update(db=db, id_pk = buoy_id, obj_in=buoy_in)

    return result

@router.delete("/buoys/{buoy_id}", response_model=BuoyDriftBase, status_code=201)
def buoy_update(
        *,
        buoy_id: int,
        token: str,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create new buoy
    """
    
    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    result = crud.crud_drift.buoy_drift.index(db=db, arguments = {'buoy_id=': buoy_id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no buoy with this id",
        )

    result = crud.crud_drift.buoy_drift.delete(db=db, id_pk = buoy_id)

    return result



#######################
# DRIFT.spotter_general ENDPOINT
#######################


@router.get("/spotter_general", status_code=200, response_model=List[SpotterGeneralDriftBase])
def spootter_general_drift_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date format is yyyy-mm-dd",
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

    result = crud.crud_drift.spotter_general.index(db=db, arguments=arguments)

    return result


#######################
# DRIFT.spotter_system ENDPOINT
#######################

@router.get("/spotter_system", status_code=200, response_model=List[SpotterSystemDriftBase])
def spotter_system_drift_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date format is yyyy-mm-dd",
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

    result = crud.crud_drift.spotter_system.index(db=db, arguments=arguments)

    return result



#######################
# DRIFT.spotter_waves ENDPOINT
#######################

@router.get("/spotter_waves", status_code=200, response_model=List[SpotterWavesDriftBase])
def spotter_system_drift_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date format is yyyy-mm-dd",
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

    result = crud.crud_drift.spotter_waves.index(db=db, arguments=arguments)

    return result



if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")