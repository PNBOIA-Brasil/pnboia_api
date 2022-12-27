import pandas as pd
import numpy as np

from typing import Optional, Any, List

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, APIRouter, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from pnboia_api.schemas.moored import *
from pnboia_api.schemas.quality_control import *
from pnboia_api.schemas.qualified_data import *
from pnboia_api.schemas.drift import *

from pnboia_api.models.moored import *
from pnboia_api.models.quality_control import *
from pnboia_api.models.qualified_data import *
from pnboia_api.models.drift import *

import pnboia_api.crud as crud

from  pnboia_api.db.base import Base, SessionLocal, engine

from datetime import datetime, timedelta, date
from mangum import Mangum


Base.metadata.create_all(bind=engine)

router = APIRouter(title="PNBOIA API", openapi_url="/openapi.json")

app = FastAPI(title="PNBOIA API", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

#API TESTS

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/v3")
def test():
    """
    Test API
    """

    return {"result": "API Working"}

#######################
# MOORED.BUOYS ENDPOINT
#######################

@app.get("/v3/moored/buoys/{buoy_id}", status_code=200, response_model=BuoyBase)
def buoy_show(
        *,
        buoy_id: int,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Fetch a single buoy by ID
    """
    result = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

    return result

@app.get("/v3/moored/buoys", status_code=200, response_model=List[BuoyBase])
def buoy_index(
        db: Session = Depends(get_db),
        status:Optional[bool]=None,
    ) -> Any:   

    """
    Fetch a single buoy by ID
    """
    if status != None:
        arguments = {'status=': status}
    else:
        arguments = {}
    
    result = crud.crud_moored.buoy.index(db=db, arguments=arguments)

    return result

# @app.post("/v3/moored/buoys", status_code=201, response_model=BuoyBase)
# def buoys_create(
#         *,
#         buoy: BuoyBase,
#         db: Session = Depends(get_db)
#     ) -> Any:
#     """
#     Create a new buoy in the database.
#     """

#     buoy = crud.crud_moored.buoy.create(db=db, obj_in=buoy)

#     return buoy

# @app.put("/v3/buoys/{buoy_id}", status_code=201, response_model=BuoyBase)
# def buoy_update(
#         *,
#         buoy_id: int,
#         buoy: BuoyBase,
#         db: Session = Depends(get_db)
#     ) -> Any:

#     buoy = crud.buoy.update(db=db, id_pk=buoy_id, obj_in=buoy)

#     return buoy

# @app.delete("/buoys/{buoy_id}")
# def buoys_delete(
#         *,
#         buoy_id: int,
#         db: Session = Depends(get_db)
#     ) -> Any:

#     buoy = crud.buoy.delete(db=db, id_pk=buoy_id)

#     return buoy

#######################
# MOORED.AXYSGENERAL ENDPOINT
#######################

@app.get("/v3/moored/axys_general", status_code=200, response_model=List[AxysGeneralBase])
def axys_general_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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

@app.get("/v3/moored/bmobr_raw", status_code=200, response_model=List[BmobrRawBase])
def bmobr_raw_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(datetime.utcnow() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(datetime.utcnow() + timedelta(days=3)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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

@app.get("/v3/moored/bmobr_triaxys_raw", status_code=200, response_model=List[BmobrTriaxysRawBase])
def bmobr_triaxys_raw_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(datetime.utcnow() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(datetime.utcnow() + timedelta(days=3)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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

@app.get("/v3/moored/spotter_all", status_code=200, response_model=List[SpotterAllBase])
def spotter_general_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(datetime.utcnow() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(datetime.utcnow() + timedelta(days=3)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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

@app.get("/v3/moored/spotter_smart_mooring_config", status_code=200, response_model=List[SpotterSmartMooringConfigBase])
def spotter_smart_mooring_config_index(
        buoy_id: int,
        db: Session = Depends(get_db)
    ) -> Any:

    arguments = {'buoy_id=': buoy_id}

    print(arguments)

    result = crud.crud_moored.spotter_smart_mooring_config.index(db=db, arguments=arguments)

    return result

#######################
# MOORED.SpotterSystem ENDPOINT
#######################

@app.get("/v3/moored/spotter_system", status_code=200, response_model=List[SpotterSystemBase])
def spotter_system_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(datetime.utcnow() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(datetime.utcnow() + timedelta(days=3)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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

@app.get("/v3/moored/bmobr_general", status_code=200, response_model=List[BmobrGeneralBase])
def bmobr_general_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(datetime.utcnow() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(datetime.utcnow() + timedelta(days=3)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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



#######################
# QUALIFIED_DATA.QualifiedData ENDPOINT
#######################

@app.get("/v3/qualified_data/qualified_data", status_code=200, response_model=List[QualifiedDataBase])
def qualified_data_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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

    result = crud.crud_qualified_data.qualified_data.index(db=db, arguments=arguments)

    return result




#######################
# DRIFT.BUOYS ENDPOINT
#######################

@app.get("/v3/drift/buoys/{buoy_id}", status_code=200, response_model=BuoyDriftBase)
def buoy_show(
        *,
        buoy_id: int,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Fetch a single buoy by ID
    """
    result = crud.crud_drift.buoy_drift.show(db=db, id_pk = buoy_id)

    return result

@app.get("/v3/drift/buoys", status_code=200, response_model=List[BuoyBase])
def buoy_index(
        db: Session = Depends(get_db),
    ) -> Any:   

    """
    Fetch a single buoy by ID
    """    
    result = crud.crud_drift.buoy_drift.index(db=db, arguments=arguments)

    return result



#######################
# DRIFT.spotter_general ENDPOINT
#######################


@app.get("/v3/drift/spotter_general", status_code=200, response_model=List[SpotterGeneralDriftBase])
def spootter_general_drift_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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

@app.get("/v3/drift/spotter_system", status_code=200, response_model=List[SpotterSystemDriftBase])
def spotter_system_drift_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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

@app.get("/v3/drift/spotter_waves", status_code=200, response_model=List[SpotterWavesDriftBase])
def spotter_system_drift_index(
        buoy_id: int,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

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