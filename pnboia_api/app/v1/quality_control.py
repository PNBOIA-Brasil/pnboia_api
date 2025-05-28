import pandas as pd
import numpy as np

from typing import Optional, Any, List
from fastapi import APIRouter, Depends, HTTPException
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

@router.post("/quality_control", response_model=GeneralNewBase, status_code=201)
def general_create(
        token: str,
        obj_in: GeneralNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create new quality control value
    """
    
    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})
    
    result = crud.crud_quality_control.general.index(db=db, arguments = {'buoy_id=': obj_in.buoy_id})

    if result:
        raise HTTPException(
            status_code=400,
            detail="There is already a qc_config for this buoy",
        )

    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )

    result = crud.crud_quality_control.general.create(db=db, obj_in=obj_in)

    return result

@router.put("/quality_control/{buoy_id}", response_model=GeneralNewBase, status_code=201)
def general_update(
        *,
        buoy_id: int,
        token: str,
        obj_in: GeneralNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Update qc_config
    """
    
    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    result = crud.crud_quality_control.general.index(db=db, arguments = {'buoy_id=': buoy_id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no qc_config for this buoy",
        )
    
    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )

    result = crud.crud_quality_control.general.update(db=db, id_pk = result[0].id, obj_in=obj_in)

    return result

@router.delete("/quality_control/{buoy_id}", response_model=GeneralNewBase, status_code=201)
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

    result = crud.crud_quality_control.general.index(db=db, arguments = {'buoy_id=': buoy_id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no qc_config for this buoy",
        )

    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )


    result = crud.crud_quality_control.general.delete(db=db, id_pk = result[0].id)

    return result
