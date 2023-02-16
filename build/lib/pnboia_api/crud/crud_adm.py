from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from pnboia_api.crud.base import CRUDBase
from pnboia_api.schemas.adm import *

from pnboia_api.models.adm import *
from pnboia_api.core.security import get_password_hash, create_token, credentials_exception

class CRUDUser(CRUDBase[User]):

    def create(self, db: Session, *, obj_in: User) -> User:
        create_data = obj_in.dict()
        db_obj = User(**create_data)
        db_obj.password = get_password_hash(obj_in.password)

        db.add(db_obj)
        db.commit()

        return db_obj

    def get_current_user(
            self,
            db: Session,
            token: str
        ) -> User:


        arguments = {'token=': token}
        
        user = crud.crud_adm.user.index(db=db, arguments=arguments)

        if user == []:
            raise credentials_exception
        return user

    def verify(
        self, db: Session, *, skip: int = 0, limit: int = 100, raise_error = True,
        arguments: dict = None
    ) -> User:

        if arguments:
            query = self.create_query(arguments)
        else:
            query = "true"

        result = db.query(self.model).filter(text(query)).first()

        if raise_error:
            if not result:
                raise credentials_exception

        return result

user = CRUDUser(User)
