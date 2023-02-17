from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import func
from sqlalchemy import desc
from pnboia_api.core.security import create_token
from pnboia_api.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def show(self, db: Session, id_pk: Any) -> Optional[ModelType]:
        result = db.query(self.model).filter(self.model.buoy_id == id_pk).first()
        if not result:
            raise HTTPException(
                status_code=404, detail=f"buoy with buoy_id = {id_pk} not found"
            )
        return result

    def index(
        self, db: Session, *, skip: int = 0, order:bool = False,limit: int = None, arguments: dict = None
    ) -> List[ModelType]:

        if arguments:
            query = self.create_query(arguments)
        else:
            query = "true"
        
        if limit:
            if order:
                result = db.query(self.model).filter(text(query)).order_by(desc(self.model.date_time)).limit(limit).all()          
            else:
                result = db.query(self.model).filter(text(query)).limit(limit).all()
        elif order:
            result = db.query(self.model).filter(text(query)).order_by(desc(self.model.date_time)).all()          
        else:
            result = db.query(self.model).filter(text(query)).all()

        return result

    def create(self, db: Session, *, obj_in: ModelType) -> ModelType:

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)


        if str(self.model) == "<class 'pnboia_api.models.moored.Buoy'>":
            max_id = db.query(func.max(self.model.buoy_id)).first()
            db_obj.buoy_id = max_id[0] + 1
        elif str(self.model) == "<class 'pnboia_api.models.drift.BuoyDrift'>":
            max_id = db.query(func.max(self.model.buoy_id)).first()
            db_obj.buoy_id = max_id[0] + 1
        else:
            max_id = db.query(func.max(self.model.id)).first()
            db_obj.id = max_id[0] + 1

        db.add(db_obj)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, id_pk: int, update_token=False, obj_in: Union[ModelType, Dict[str, Any]]
    ) -> ModelType:
    
        if str(self.model) == "<class 'pnboia_api.models.moored.Buoy'>":
            obj_old = db.query(self.model).filter(self.model.buoy_id == id_pk).first()
        elif str(self.model) == "<class 'pnboia_api.models.drift.BuoyDrift'>":
            obj_old = db.query(self.model).filter(self.model.buoy_id == id_pk).first()
        else:
            obj_old = db.query(self.model).filter(self.model.id == id_pk).first()

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in vars(obj_old).keys():
            if field in update_data:
                setattr(obj_old, field, update_data[field])

        if update_token:
            obj_old.token = create_token(20)

        db.add(obj_old)
        db.commit()
        db.refresh(obj_old)
        return obj_old

    def delete(self, db: Session, *, id_pk: int) -> ModelType:
        obj = db.query(self.model).get(id_pk)
        db.delete(obj)
        db.commit()
        return obj

    def create_query(self, kwargs):
        x = 0
        query = ""
        for key, value in kwargs.items():
            if x == 0:
                beginning = ""
            else:
                beginning = " AND"
            if type(value) == list:
                if len(value[1]) == 1:
                    query += f"{beginning} {key} {value[0]} ('{value[1][0]}')"
                else:
                    query += f"{beginning} {key} {value[0]} {tuple(value[1])}"
            else:
                query += f"{beginning} {key} '{value}'"
            x = 1

        return query