from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import func

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
                status_code=404, detail=f"buoy with status {status} not found"
            )
        return result

    def index(
        self, db: Session, *, skip: int = 0, limit: int = 100, arguments: dict = None
    ) -> List[ModelType]:

        if arguments:
            query = self.create_query(arguments)
        else:
            query = "true"

        result = db.query(self.model).filter(text(query)).all()
        if not result:
            raise HTTPException(
                status_code=404, detail=f"{self.model} with {arguments} not found"
            )

        return result

    def create(self, db: Session, *, obj_in: ModelType) -> ModelType:

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)

        max_id = db.query(func.max(self.model.id)).first()

        db_obj.id = max_id[0] + 1

        db.add(db_obj)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, id_pk: int, obj_in: Union[ModelType, Dict[str, Any]]
    ) -> ModelType:
    
        obj_old = db.query(self.model).filter(self.model.id == id_pk).first()

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in vars(obj_old).keys():
            if field in update_data:
                setattr(obj_old, field, update_data[field])
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