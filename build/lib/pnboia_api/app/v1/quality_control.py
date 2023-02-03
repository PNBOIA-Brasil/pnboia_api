import pandas as pd
import numpy as np

from typing import Optional, Any, List

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from pnboia_api.schemas.quality_control import *
from pnboia_api.models.quality_control import *
import pnboia_api.crud as crud
from  pnboia_api.db.base import Base, engine
from datetime import datetime, timedelta, date

from pnboia_api.app.deps import get_db

Base.metadata.create_all(bind=engine)

router = APIRouter()


#######################
# QUALIFIED_DATA.QualifiedData ENDPOINT
#######################

@router.get("/quality_control", status_code=200, response_model=List[GeneralBase])
def quality_control_index(
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

    result = crud.crud_quality_control.general.index(db=db, arguments=arguments)

    return result
