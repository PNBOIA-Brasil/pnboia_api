import pandas as pd
import numpy as np

from typing import Optional, Any, List

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, APIRouter, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from pnboia_api.schemas import *
import pnboia_api.crud as crud
from pnboia_api.models import *

from  pnboia_api.db.base import Base, SessionLocal, engine

from datetime import datetime, timedelta, date
from mangum import Mangum


Base.metadata.create_all(bind=engine)

app = FastAPI(title="PNBOIA API", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/v2")
def test():
    """
    Test API
    """

    return {"result": "API Working"}


@app.get("/v2/buoys/{buoy_id}", status_code=200, response_model=BuoyBase)
def buoy_show(
        *,
        buoy_id: int,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Fetch a single buoy by ID
    """
    result = crud.buoy.show(db=db, id_pk = buoy_id)

    return result

@app.get("/v2/buoys", status_code=200, response_model=List[BuoyBase])
def buoy_index(
        db: Session = Depends(get_db),
        status:Optional[str] = Query(None, min_length=5, example="ativa"),
    ) -> Any:
    """
    Fetch a single buoy by ID
    """
    if status:
        status = status.capitalize()

    result = crud.buoy.index(db=db, arguments = {'status=': status})

    return result


@app.post("/v2/buoys", status_code=201, response_model=BuoyBase)
def buoys_create(
        *,
        buoy: BuoyBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create a new buoy in the database.
    """

    buoy = crud.buoy.create(db=db, obj_in=buoy)

    return buoy

@app.put("/v2/buoys/{buoy_id}", status_code=201, response_model=BuoyBase)
def buoy_update(
        *,
        buoy_id: int,
        buoy: BuoyBase,
        db: Session = Depends(get_db)
    ) -> Any:

    buoy = crud.buoy.update(db=db, id_pk=buoy_id, obj_in=buoy)

    return buoy

@app.delete("/buoys/{buoy_id}")
def buoys_delete(
        *,
        buoy_id: int,
        db: Session = Depends(get_db)
    ) -> Any:

    buoy = crud.buoy.delete(db=db, id_pk=buoy_id)

    return buoy


@app.get("/v2/data_buoys/{buoy_id}")
def data_buoy_index(
        *,
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
    
    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))
        
    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)
    result = crud.data_buoy.index(db=db, arguments=arguments)

    return result


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")