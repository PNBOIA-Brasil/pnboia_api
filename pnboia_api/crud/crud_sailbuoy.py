from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.sailbuoy import (
    SailbuoyMetadata, AutopilotData, DataloggerData,
    AutopilotDataSynoptic, DataloggerDataSynoptic
)
from pnboia_api.schemas.sailbuoy import (
    SailbuoyMetadataCreate, SailbuoyMetadataUpdate,
    AutopilotDataCreate, AutopilotDataUpdate,
    DataloggerDataCreate, DataloggerDataUpdate
)

class CRUDSailbuoyMetadata(CRUDBase[SailbuoyMetadata]):
    """
    CRUD operations for SailbuoyMetadata
    """
    def get_by_imei(self, db: Session, *, imei: str) -> Optional[SailbuoyMetadata]:
        """Get a sailbuoy metadata entry by IMEI"""
        return db.query(self.model).filter(self.model.imei == imei).first()

    def get_by_name(self, db: Session, *, name: str) -> Optional[SailbuoyMetadata]:
        """Get a sailbuoy metadata entry by name"""
        return db.query(self.model).filter(self.model.name == name).first()

    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[SailbuoyMetadata]:
        """Get all active sailbuoys"""
        return db.query(self.model).filter(self.model.is_active == True).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: SailbuoyMetadataCreate) -> SailbuoyMetadata:
        """Create a new sailbuoy metadata entry"""
        # Check if sailbuoy with this name already exists
        existing = db.query(self.model).filter(
            (self.model.sailbuoy_id == obj_in.sailbuoy_id) & 
            (self.model.name == obj_in.name)
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Sailbuoy with ID {obj_in.sailbuoy_id} and name {obj_in.name} already exists"
            )
        
        # Create new entry
        db_obj = SailbuoyMetadata(
            sailbuoy_id=obj_in.sailbuoy_id,
            name=obj_in.name,
            imei=obj_in.imei,
            model=obj_in.model,
            deploy_date=obj_in.deploy_date,
            last_date_time=obj_in.last_date_time,
            is_active=obj_in.is_active
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


class CRUDAutopilotData(CRUDBase[AutopilotData]):
    """
    CRUD operations for AutopilotData
    """
    def get_latest(self, db: Session, *, sailbuoy_id: str, limit: int = 1) -> List[AutopilotData]:
        """Get the latest autopilot data for a sailbuoy"""
        return (
            db.query(self.model)
            .filter(self.model.sailbuoy_id == sailbuoy_id)
            .order_by(desc(self.model.sailbuoy_time))
            .limit(limit)
            .all()
        )
    
    def get_by_time_range(
        self, 
        db: Session, 
        *, 
        sailbuoy_id: str, 
        start_time: datetime, 
        end_time: datetime,
        limit: int = 1000
    ) -> List[AutopilotData]:
        """Get autopilot data for a sailbuoy within a time range"""
        # Log the input parameters for debugging
        print(f"Querying autopilot data for {sailbuoy_id} between {start_time} and {end_time}")
        
        # Execute the query
        result = (
            db.query(self.model)
            .filter(
                (self.model.sailbuoy_id == sailbuoy_id) &
                (self.model.sailbuoy_time >= start_time) &
                (self.model.sailbuoy_time <= end_time)
            )
            .order_by(self.model.sailbuoy_time)
            .limit(limit)
            .all()
        )
        
        # Log the number of results
        print(f"Found {len(result)} records")
        return result
    
    def create(self, db: Session, *, obj_in: AutopilotDataCreate) -> AutopilotData:
        """Create a new autopilot data entry"""
        # Get the sailbuoy metadata
        sailbuoy_metadata = sailbuoy_metadata.get_by_name(db, name=obj_in.name)
        if not sailbuoy_metadata:
            raise HTTPException(
                status_code=404,
                detail=f"Sailbuoy with name {obj_in.name} not found"
            )
        
        # Create data dictionary, excluding name since it's not a column in AutopilotData
        data = obj_in.dict(exclude={"name"})
        data["sailbuoy_id"] = sailbuoy_metadata.sailbuoy_id
        
        # Create new entry
        db_obj = AutopilotData(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Update last_date_time in metadata if this is the most recent data
        if not sailbuoy_metadata.last_date_time or obj_in.sailbuoy_time > sailbuoy_metadata.last_date_time:
            sailbuoy_metadata.last_date_time = obj_in.sailbuoy_time
            db.add(sailbuoy_metadata)
            db.commit()
            db.refresh(sailbuoy_metadata)
        
        return db_obj


class CRUDDataloggerData(CRUDBase[DataloggerData]):
    """
    CRUD operations for DataloggerData
    """
    def get_latest(self, db: Session, *, sailbuoy_id: str, limit: int = 1) -> List[DataloggerData]:
        """Get the latest datalogger data for a sailbuoy"""
        return (
            db.query(self.model)
            .filter(self.model.sailbuoy_id == sailbuoy_id)
            .order_by(desc(self.model.sailbuoy_time))
            .limit(limit)
            .all()
        )
    
    def get_by_time_range(
        self, 
        db: Session, 
        *, 
        sailbuoy_id: str, 
        start_time: datetime, 
        end_time: datetime,
        limit: int = 1000
    ) -> List[DataloggerData]:
        """Get datalogger data for a sailbuoy within a time range"""
        # Log the input parameters for debugging
        print(f"Querying datalogger data for {sailbuoy_id} between {start_time} and {end_time}")
        
        # Execute the query
        result = (
            db.query(self.model)
            .filter(
                (self.model.sailbuoy_id == sailbuoy_id) &
                (self.model.sailbuoy_time >= start_time) &
                (self.model.sailbuoy_time <= end_time)
            )
            .order_by(self.model.sailbuoy_time)
            .limit(limit)
            .all()
        )
        
        # Log the number of results
        print(f"Found {len(result)} records")
        return result
    
    def create(self, db: Session, *, obj_in: DataloggerDataCreate) -> DataloggerData:
        """Create a new datalogger data entry"""
        # Get the sailbuoy metadata
        sailbuoy_metadata = sailbuoy_metadata.get_by_name(db, name=obj_in.name)
        if not sailbuoy_metadata:
            raise HTTPException(
                status_code=404,
                detail=f"Sailbuoy with name {obj_in.name} not found"
            )
        
        # Create data dictionary, excluding name since it's not a column in DataloggerData
        data = obj_in.dict(exclude={"name"})
        data["sailbuoy_id"] = sailbuoy_metadata.sailbuoy_id
        
        # Create new entry
        db_obj = DataloggerData(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Update last_date_time in metadata if this is the most recent data
        if not sailbuoy_metadata.last_date_time or obj_in.sailbuoy_time > sailbuoy_metadata.last_date_time:
            sailbuoy_metadata.last_date_time = obj_in.sailbuoy_time
            db.add(sailbuoy_metadata)
            db.commit()
            db.refresh(sailbuoy_metadata)
        
        return db_obj


# Create instances of the CRUD classes
sailbuoy_metadata = CRUDSailbuoyMetadata(SailbuoyMetadata)
autopilot_data = CRUDAutopilotData(AutopilotData)
datalogger_data = CRUDDataloggerData(DataloggerData)

# Synoptic data CRUD operations
class CRUDAutopilotDataSynoptic(CRUDAutopilotData):
    """CRUD operations for autopilot synoptic data"""
    pass

class CRUDDataloggerDataSynoptic(CRUDDataloggerData):
    """CRUD operations for datalogger synoptic data"""
    pass

# Initialize the CRUD instances for synoptic data
autopilot_data_synoptic = CRUDAutopilotDataSynoptic(AutopilotDataSynoptic)
datalogger_data_synoptic = CRUDDataloggerDataSynoptic(DataloggerDataSynoptic)
