from typing import List, Optional, Any
from datetime import datetime, timedelta, date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from pnboia_api.app.deps import get_db
from pnboia_api.schemas.sailbuoy import (
    SailbuoyMetadataResponse, SailbuoyMetadataCreate, SailbuoyMetadataUpdate,
    AutopilotDataResponse, AutopilotDataCreate, AutopilotDataUpdate,
    DataloggerDataResponse, DataloggerDataCreate, DataloggerDataUpdate,
    PaginatedResponse
)
from pnboia_api import crud

router = APIRouter()

#######################
# SAILBUOY METADATA ENDPOINTS
#######################

@router.get("/metadata", response_model=List[SailbuoyMetadataResponse])
def list_metadata(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
):
    """
    Retrieve sailbuoy metadata entries.
    """
    if active_only:
        return crud.sailbuoy_metadata.get_active(db, skip=skip, limit=limit)
    return crud.sailbuoy_metadata.index(db, skip=skip, limit=limit)

@router.get("/metadata/{sailbuoy_id}/{name}", response_model=SailbuoyMetadataResponse)
def get_metadata(
    sailbuoy_id: str,
    name: str,
    db: Session = Depends(get_db),
):
    """
    Get a specific sailbuoy metadata entry by sailbuoy_id and name.
    """
    db_metadata = db.query(crud.sailbuoy_metadata.model).filter(
        (crud.sailbuoy_metadata.model.sailbuoy_id == sailbuoy_id) &
        (crud.sailbuoy_metadata.model.name == name)
    ).first()
    if not db_metadata:
        raise HTTPException(status_code=404, detail="Sailbuoy metadata not found")
    return db_metadata

@router.post("/metadata/", response_model=SailbuoyMetadataResponse)
def create_metadata(
    metadata: SailbuoyMetadataCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new sailbuoy metadata entry.
    """
    return crud.sailbuoy_metadata.create(db=db, obj_in=metadata)

@router.put("/metadata/{sailbuoy_id}/{name}", response_model=SailbuoyMetadataResponse)
def update_metadata(
    sailbuoy_id: str,
    name: str,
    metadata: SailbuoyMetadataUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a sailbuoy metadata entry.
    """
    db_metadata = db.query(crud.sailbuoy_metadata.model).filter(
        (crud.sailbuoy_metadata.model.sailbuoy_id == sailbuoy_id) &
        (crud.sailbuoy_metadata.model.name == name)
    ).first()
    if not db_metadata:
        raise HTTPException(status_code=404, detail="Sailbuoy metadata not found")
    
    return crud.sailbuoy_metadata.update(db=db, id_pk=(sailbuoy_id, name), obj_in=metadata)

@router.delete("/metadata/{sailbuoy_id}/{name}")
def delete_metadata(
    sailbuoy_id: str,
    name: str,
    db: Session = Depends(get_db),
):
    """
    Delete a sailbuoy metadata entry.
    """
    db_metadata = db.query(crud.sailbuoy_metadata.model).filter(
        (crud.sailbuoy_metadata.model.sailbuoy_id == sailbuoy_id) &
        (crud.sailbuoy_metadata.model.name == name)
    ).first()
    if not db_metadata:
        raise HTTPException(status_code=404, detail="Sailbuoy metadata not found")
    
    db.delete(db_metadata)
    db.commit()
    return {"ok": True}

#######################
# AUTOPILOT DATA ENDPOINTS
#######################

@router.get("/autopilot/", response_model=List[AutopilotDataResponse])
def list_autopilot_data(
    db: Session = Depends(get_db),
    sailbuoy_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
):
    """
    Retrieve autopilot data with optional filtering.
    """
    if sailbuoy_id and start_date and end_date:
        return crud.autopilot_data.get_by_time_range(
            db, 
            sailbuoy_id=sailbuoy_id,
            start_time=start_date,
            end_time=end_date,
            limit=limit
        )
    elif sailbuoy_id:
        return crud.autopilot_data.get_latest(
            db, 
            sailbuoy_id=sailbuoy_id,
            limit=limit
        )
    return crud.autopilot_data.index(db, limit=limit)

@router.post("/autopilot/", response_model=AutopilotDataResponse)
def create_autopilot_data(
    data: AutopilotDataCreate,
    db: Session = Depends(get_db),
):
    """
    Create new autopilot data.
    """
    return crud.autopilot_data.create(db=db, obj_in=data)

@router.get("/autopilot/latest", response_model=List[AutopilotDataResponse])
def get_latest_autopilot_data(
    sailbuoy_id: str,
    limit: int = Query(1, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Get the latest autopilot data for a specific sailbuoy.
    """
    return crud.autopilot_data.get_latest(db, sailbuoy_id=sailbuoy_id, limit=limit)

#######################
# DATALOGGER DATA ENDPOINTS
#######################

@router.get("/datalogger/", response_model=List[DataloggerDataResponse])
def list_datalogger_data(
    db: Session = Depends(get_db),
    sailbuoy_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
):
    """
    Retrieve datalogger data with optional filtering.
    """
    if sailbuoy_id and start_date and end_date:
        return crud.datalogger_data.get_by_time_range(
            db, 
            sailbuoy_id=sailbuoy_id,
            start_time=start_date,
            end_time=end_date,
            limit=limit
        )
    elif sailbuoy_id:
        return crud.datalogger_data.get_latest(
            db, 
            sailbuoy_id=sailbuoy_id,
            limit=limit
        )
    return crud.datalogger_data.index(db, limit=limit)

@router.post("/datalogger/", response_model=DataloggerDataResponse)
def create_datalogger_data(
    data: DataloggerDataCreate,
    db: Session = Depends(get_db),
):
    """
    Create new datalogger data.
    """
    return crud.datalogger_data.create(db=db, obj_in=data)

@router.get("/datalogger/latest", response_model=List[DataloggerDataResponse])
def get_latest_datalogger_data(
    sailbuoy_id: str,
    limit: int = Query(1, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Get the latest datalogger data for a specific sailbuoy.
    """
    return crud.datalogger_data.get_latest(db, sailbuoy_id=sailbuoy_id, limit=limit)
