import pandas as pd
import numpy as np

from typing import Optional, Any, List

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from pnboia_api.schemas.qualified_data import *
from pnboia_api.models.qualified_data import *
import pnboia_api.crud as crud
from  pnboia_api.db.base import Base, engine
from datetime import datetime, timedelta, date

from pnboia_api.app.deps import get_db

Base.metadata.create_all(bind=engine)

router = APIRouter()


#######################
# QUALIFIED_DATA.QualifiedData ENDPOINT
#######################

@router.get("/v3/qualified_data/qualified_data", status_code=200, response_model=List[QualifiedDataBase])
def qualified_data_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db),
        petrobras: bool = False,
        limit: int = None,
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


    result = crud.crud_qualified_data.qualified_data.index(db=db, arguments=arguments)

    
    return result

