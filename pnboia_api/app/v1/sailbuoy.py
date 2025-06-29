from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from dateutil.parser import parse as parse_date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import desc

from pnboia_api.db.database import get_db
from pnboia_api.schemas.sailbuoy import (
    SailbuoyMetadataResponse,
    AutopilotDataResponse,
    DataloggerDataResponse,
    SailbuoyMetadataCreate,
    SailbuoyMetadataUpdate,
    AutopilotDataCreate,
    DataloggerDataCreate,
    AutopilotDataUpdate,
    DataloggerDataUpdate,
    AutopilotDataSynopticResponse,
    DataloggerDataSynopticResponse,
    PaginatedResponse
)
from pnboia_api.crud.crud_sailbuoy import (
    sailbuoy_metadata,
    autopilot_data,
    datalogger_data,
    autopilot_data_synoptic,
    datalogger_data_synoptic,
)
from pnboia_api.models.sailbuoy import (
    SailbuoyMetadata, 
    AutopilotData, 
    DataloggerData,
    AutopilotDataSynoptic,
    DataloggerDataSynoptic
)
from pnboia_api.core import verify_token

# Security
security = HTTPBearer()

# Valid tokens (you can move this to a database query if needed)
VALID_TOKENS = ["HSSl1OJ-mo4vOX6eVXLG"]  # Add other valid tokens here

# Token verification
def verify_token(token: str = Query(..., description="API token for authentication")):
    """Verify the token from query parameters"""
    if token not in VALID_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
        )
    return True

router = APIRouter()

#######################
# SAILBUOY METADATA ENDPOINTS
#######################

@router.get("/metadata", response_model=List[SailbuoyMetadataResponse], dependencies=[Depends(verify_token)])
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
        return sailbuoy_metadata.get_active(db, skip=skip, limit=limit)
    return sailbuoy_metadata.index(db, skip=skip, limit=limit)

@router.get("/metadata/{sailbuoy_id}/{name}", response_model=SailbuoyMetadataResponse, dependencies=[Depends(verify_token)])
def get_metadata(
    sailbuoy_id: str,
    name: str,
    db: Session = Depends(get_db),
):
    """
    Get a specific sailbuoy metadata entry by sailbuoy_id and name.
    """
    db_metadata = db.query(SailbuoyMetadata).filter(
        SailbuoyMetadata.sailbuoy_id == sailbuoy_id,
        SailbuoyMetadata.name == name
    ).first()
    if not db_metadata:
        raise HTTPException(status_code=404, detail="Sailbuoy metadata not found")
    return db_metadata

@router.post("/metadata/", response_model=SailbuoyMetadataResponse, dependencies=[Depends(verify_token)])
def create_metadata(
    metadata: SailbuoyMetadataCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new sailbuoy metadata entry.
    """
    return sailbuoy_metadata.create(db=db, obj_in=metadata)

@router.put("/metadata/{sailbuoy_id}/{name}", response_model=SailbuoyMetadataResponse, dependencies=[Depends(verify_token)])
def update_metadata(
    sailbuoy_id: str,
    name: str,
    metadata: SailbuoyMetadataUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a sailbuoy metadata entry.
    """
    db_metadata = db.query(SailbuoyMetadata).filter(
        SailbuoyMetadata.sailbuoy_id == sailbuoy_id,
        SailbuoyMetadata.name == name
    ).first()
    if not db_metadata:
        raise HTTPException(status_code=404, detail="Sailbuoy metadata not found")
    
    return sailbuoy_metadata.update(db=db, id_pk=db_metadata.id, obj_in=metadata)

@router.delete("/metadata/{sailbuoy_id}/{name}", response_model=SailbuoyMetadataResponse, dependencies=[Depends(verify_token)])
def delete_metadata(
    sailbuoy_id: str,
    name: str,
    db: Session = Depends(get_db),
):
    """
    Delete a sailbuoy metadata entry.
    """
    db_metadata = db.query(SailbuoyMetadata).filter(
        SailbuoyMetadata.sailbuoy_id == sailbuoy_id,
        SailbuoyMetadata.name == name
    ).first()
    if not db_metadata:
        raise HTTPException(status_code=404, detail="Sailbuoy metadata not found")
    
    db.delete(db_metadata)
    db.commit()
    return db_metadata

#######################
# AUTOPILOT DATA ENDPOINTS
#######################

@router.get("/autopilot/", response_model=List[AutopilotDataResponse], dependencies=[Depends(verify_token)])
def list_autopilot_data(
    db: Session = Depends(get_db),
    sailbuoy_id: Optional[str] = None,
    start_date: Optional[Union[datetime, str]] = None,
    end_date: Optional[Union[datetime, str]] = None,
    limit: int = 100,
):
    """
    Retrieve autopilot data with optional filtering.
    """
    # Convert string dates to datetime objects if needed
    if isinstance(start_date, str):
        start_date = parse_date(start_date)
    if isinstance(end_date, str):
        end_date = parse_date(end_date)
    
    if sailbuoy_id and start_date and end_date:
        return autopilot_data.get_by_time_range(
            db, 
            sailbuoy_id=sailbuoy_id,
            start_time=start_date,
            end_time=end_date,
            limit=limit
        )
    elif sailbuoy_id:
        return autopilot_data.get_latest(
            db, 
            sailbuoy_id=sailbuoy_id,
            limit=limit
        )
    return autopilot_data.index(db, limit=limit)

@router.post("/autopilot/", response_model=AutopilotDataResponse, dependencies=[Depends(verify_token)])
def create_autopilot_data(
    data: AutopilotDataCreate,
    db: Session = Depends(get_db),
):
    """
    Create new autopilot data.
    """
    return autopilot_data.create(db=db, obj_in=data)

@router.get("/autopilot/latest/{sailbuoy_id}", response_model=List[AutopilotDataResponse], dependencies=[Depends(verify_token)])
def get_latest_autopilot_data(
    sailbuoy_id: str,
    limit: int = Query(1, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Get the latest autopilot data for a specific sailbuoy.
    """
    return autopilot_data.get_latest(db, sailbuoy_id=sailbuoy_id, limit=limit)

#######################
# DATALOGGER DATA ENDPOINTS
#######################

@router.get("/datalogger/", response_model=List[DataloggerDataResponse], dependencies=[Depends(verify_token)])
def list_datalogger_data(
    db: Session = Depends(get_db),
    sailbuoy_id: Optional[str] = None,
    start_date: Optional[Union[datetime, str]] = None,
    end_date: Optional[Union[datetime, str]] = None,
    limit: int = 100,
):
    """
    Retrieve datalogger data with optional filtering.
    """
    # Convert string dates to datetime objects if needed
    if isinstance(start_date, str):
        start_date = parse_date(start_date)
    if isinstance(end_date, str):
        end_date = parse_date(end_date)
    
    if sailbuoy_id and start_date and end_date:
        return datalogger_data.get_by_time_range(
            db, 
            sailbuoy_id=sailbuoy_id,
            start_time=start_date,
            end_time=end_date,
            limit=limit
        )
    elif sailbuoy_id:
        return datalogger_data.get_latest(
            db, 
            sailbuoy_id=sailbuoy_id,
            limit=limit
        )
    return datalogger_data.index(db, limit=limit)

@router.post("/datalogger/", response_model=DataloggerDataResponse, dependencies=[Depends(verify_token)])
def create_datalogger_data(
    data: DataloggerDataCreate,
    db: Session = Depends(get_db),
):
    """
    Create new datalogger data.
    """
    return datalogger_data.create(db=db, obj_in=data)

@router.get("/datalogger/latest/{sailbuoy_id}", response_model=List[DataloggerDataResponse], dependencies=[Depends(verify_token)])
def get_latest_datalogger_data(
    sailbuoy_id: str,
    limit: int = Query(1, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Get the latest datalogger data for a specific sailbuoy.
    """
    return datalogger_data.get_latest(db, sailbuoy_id=sailbuoy_id, limit=limit)


#######################
# SYNOPTIC DATA ENDPOINTS (00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00)
#######################

@router.get("/autopilot/synoptic", response_model=List[AutopilotDataSynopticResponse], dependencies=[Depends(verify_token)])
def list_autopilot_synoptic_data(
    db: Session = Depends(get_db),
    sailbuoy_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
):
    """
    Retrieve synoptic autopilot data (00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00)
    
    This endpoint returns the same fields as the regular autopilot data endpoint, but only includes
    data points at synoptic hours (every 3 hours).
    """
    query = db.query(AutopilotDataSynoptic)
    
    if sailbuoy_id:
        query = query.filter(AutopilotDataSynoptic.sailbuoy_id == sailbuoy_id)
    if start_date:
        query = query.filter(AutopilotDataSynoptic.sailbuoy_time >= start_date)
    if end_date:
        query = query.filter(AutopilotDataSynoptic.sailbuoy_time <= end_date)
    
    results = query.order_by(desc(AutopilotDataSynoptic.sailbuoy_time)).limit(limit).all()
    
    # Convert to response model - include all fields that exist in the response model
    return [
        AutopilotDataSynopticResponse(
            **{
                k: getattr(row, k, None)  # Use None as default if attribute doesn't exist
                for k in AutopilotDataSynopticResponse.__annotations__.keys()
            }
        )
        for row in results
    ]

@router.get("/datalogger/synoptic", response_model=List[DataloggerDataSynopticResponse], dependencies=[Depends(verify_token)])
def list_datalogger_synoptic_data(
    db: Session = Depends(get_db),
    sailbuoy_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
):
    """
    Retrieve synoptic datalogger data (00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00)
    
    This endpoint returns the same fields as the regular datalogger data endpoint, but only includes
    data points at synoptic hours (every 3 hours).
    """
    query = db.query(DataloggerDataSynoptic)
    
    if sailbuoy_id:
        query = query.filter(DataloggerDataSynoptic.sailbuoy_id == sailbuoy_id)
    if start_date:
        query = query.filter(DataloggerDataSynoptic.sailbuoy_time >= start_date)
    if end_date:
        query = query.filter(DataloggerDataSynoptic.sailbuoy_time <= end_date)
    
    results = query.order_by(desc(DataloggerDataSynoptic.sailbuoy_time)).limit(limit).all()
    
    # Convert to response model - include all fields that exist in the response model
    return [
        DataloggerDataSynopticResponse(
            **{
                k: getattr(row, k, None)  # Use None as default if attribute doesn't exist
                for k in DataloggerDataSynopticResponse.__annotations__.keys()
            }
        )
        for row in results
    ]

@router.get("/autopilot/synoptic/latest", response_model=List[AutopilotDataSynopticResponse], dependencies=[Depends(verify_token)])
def get_latest_autopilot_synoptic_data(
    sailbuoy_id: str,
    limit: int = Query(1, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Get the latest synoptic autopilot data for a specific sailbuoy.
    
    Returns the most recent synoptic data points (every 3 hours) with all fields
    matching the regular autopilot data endpoint.
    """
    results = autopilot_data_synoptic.get_latest(db, sailbuoy_id=sailbuoy_id, limit=limit)
    
    # Convert to response model - include all fields that exist in the response model
    return [
        AutopilotDataSynopticResponse(
            **{
                k: getattr(row, k, None)  # Use None as default if attribute doesn't exist
                for k in AutopilotDataSynopticResponse.__annotations__.keys()
            }
        )
        for row in (results if results else [])
    ]

@router.get("/datalogger/synoptic/latest", response_model=List[DataloggerDataResponse], dependencies=[Depends(verify_token)])
def get_latest_datalogger_synoptic_data(
    sailbuoy_id: str,
    limit: int = Query(1, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """
    Get the latest synoptic datalogger data for a specific sailbuoy.
    """
    results = datalogger_data_synoptic.get_latest(db, sailbuoy_id=sailbuoy_id, limit=limit)
    # Convert to response model
    return [
        DataloggerDataResponse(
            **{
                k: getattr(row, k)
                for k in DataloggerDataResponse.__annotations__.keys()
                if hasattr(row, k)
            }
        )
        for row in (results if results else [])
    ]
