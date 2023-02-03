from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from pnboia_api.schemas.adm import *
from pnboia_api.models.adm import *
import pnboia_api.crud as crud
from pnboia_api.app.deps import get_db

from pnboia_api.core.security import credentials_exception

router = APIRouter()

@router.get("/me", response_model=UserBase)
def read_users_me(
        db: Session = Depends(get_db),
        token: str = None,
    ) -> Any:   

    """
    Fetch a single buoy by ID
    """
    if token == None:
        raise credentials_exception

    arguments = {'token=': token}

    result = crud.crud_adm.user.index(db=db, arguments=arguments)

    return result


@router.post("/signup", response_model=UserBase, status_code=201)
def create_user_signup(
        *,
        db: Session = Depends(get_db),
        user_in: UserBase
    ) -> Any:
    """
    Create new user without the need to be logged in.
    """

    arguments = {'email=': user_in.email}
    
    user = crud.crud_adm.user.verify(db=db, raise_error=False, arguments=arguments)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )

    user = crud.crud_adm.user.create(db=db, obj_in=user_in)

    return user
