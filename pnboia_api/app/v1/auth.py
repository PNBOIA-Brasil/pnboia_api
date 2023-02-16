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

@router.get("/me", response_model=UserShowBase)
def show_user(
        db: Session = Depends(get_db),
        token: str = None,
    ) -> Any:   

    """
    Fetch a single buoy by ID
    """
    if token == None:
        raise credentials_exception

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    return user


@router.post("/", response_model=UserShowBase, status_code=201)
def create_user(
        *,
        token: str,
        db: Session = Depends(get_db),
        user_in: UserCreateBase
    ) -> Any:
    """
    Create new user without the need to be logged in.
    """

    if token == None:
        raise credentials_exception

    user = crud.crud_adm.user.verify(db=db, raise_error=False, arguments={'token=': token})

    if user.user_type != 'admin':
        raise credentials_exception
    
    user = crud.crud_adm.user.verify(db=db, raise_error=False, arguments = {'email=': user_in.email})

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )

    user_in.user_type = 'normal'

    user = crud.crud_adm.user.create(db=db, obj_in=user_in)

    return user

@router.put("/", response_model=UserShowBase, status_code=201)
def update_user(
        *,
        token: str,
        db: Session = Depends(get_db),
        user_in: UserUpdateBase
    ) -> Any:
    """
    Create new user without the need to be logged in.
    """

    if token == None:
        raise credentials_exception

    user = crud.crud_adm.user.verify(db=db, raise_error=False, arguments={'token=': token})

    if user.user_type != 'admin':
        raise credentials_exception

    arguments = {'email=': user_in.email}

    user = crud.crud_adm.user.verify(db=db, raise_error=False, arguments=arguments)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="There is no user with token",
        )

    user = crud.crud_adm.user.update(db=db, id_pk = user.id, obj_in=user_in)

    return user

@router.delete("/", response_model=UserShowBase, status_code=201)
def delete_user(
        *,
        token: str,
        db: Session = Depends(get_db),
        user_in: UserUpdateBase
    ) -> Any:
    """
    Create new user without the need to be logged in.
    """

    if token == None:
        raise credentials_exception

    user = crud.crud_adm.user.verify(db=db, raise_error=False, arguments={'token=': token})

    if user.user_type != 'admin':
        raise credentials_exception

    arguments = {'email=': user_in.email}

    user = crud.crud_adm.user.verify(db=db, raise_error=False, arguments=arguments)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="There is no user with token",
        )

    user = crud.crud_adm.user.delete(db=db, id_pk = user.id)

    return user