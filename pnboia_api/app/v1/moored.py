from typing import Optional, Any, List
from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse, FileResponse, Response
from sqlalchemy.orm import Session

from pnboia_api.schemas.moored import *
from pnboia_api.models.moored import *
import pnboia_api.crud as crud
from  pnboia_api.db.base import Base, engine
from datetime import datetime, timedelta, date

from pnboia_api.app.deps import get_db

from pnboia_api.app.utils import APIUtils, HTMLUtils, TXTUtils, JSONUtils


Base.metadata.create_all(bind=engine)

router = APIRouter()

#######################
# MOORED.BUOYS ENDPOINT
#######################

@router.get("/buoys/{buoy_id}", status_code=200, response_model=BuoyBase)
def buoy_show(
        *,
        buoy_id: int,
        token: str,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Fetch a single buoy by ID
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    result = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

    return result

@router.get("/buoys_internal", status_code=200, response_model=List[BuoyBase])
def obj_index(
        token: str,
        db: Session = Depends(get_db),
        status:Optional[bool]=None,
        order:Optional[bool]=False,
    ) -> Any:

    """
    Fetch a single buoy by ID
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    if status != None:
        arguments = {'status=': status}
    else:
        arguments = {}

    result = crud.crud_moored.buoy.index(db=db, order=order, arguments=arguments)

    return result


@router.post("/buoys_internal", response_model=BuoyBase, status_code=201)
def buoy_create(
        token: str,
        obj_in: BuoyNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create new buoy
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})


    result = crud.crud_moored.buoy.index(db=db, arguments = {'name=': obj_in.name})

    if result:
        raise HTTPException(
            status_code=400,
            detail="There is already a buoy with this name",
        )

    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )


    result = crud.crud_moored.buoy.create(db=db, obj_in=obj_in)

    return result

@router.put("/buoys_internal/{buoy_id}", response_model=BuoyBase, status_code=201)
def buoy_update(
        *,
        buoy_id: int,
        token: str,
        obj_in: BuoyNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create new buoy
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    result = crud.crud_moored.buoy.index(db=db, arguments = {'buoy_id=': buoy_id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no buoy with this id",
        )

    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )

    result = crud.crud_moored.buoy.update(db=db, id_pk = buoy_id, obj_in=obj_in)

    return result

@router.delete("/buoys_internal/{buoy_id}", response_model=BuoyBase, status_code=201)
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

    result = crud.crud_moored.buoy.index(db=db, arguments = {'buoy_id=': buoy_id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no buoy with this id",
        )

    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )


    result = crud.crud_moored.buoy.delete(db=db, id_pk = buoy_id)

    return result


@router.get("/buoys", status_code=200, response_model=List[AvailableBuoysSchema])
def obj_index(
        token: str,
        db: Session = Depends(get_db),
        status:Optional[bool]=None,
        order:Optional[bool]=False,
        response_type:Optional[str]='html'
    ) -> Any:

    """
    Fetch list of available buoys
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    if status != None:
        arguments = {'status=': status}
    else:
        arguments = {}

    buoys = crud.crud_moored.buoy.index(db=db, order=order, arguments=arguments)

    if response_type == 'html':
        final_response = HTMLUtils().compose_base_available_buoys(buoys=buoys)
        return HTMLResponse(final_response)
    elif response_type == "json":
        return buoys
    elif response_type == "txt":
        final_response = TXTUtils().compose_base_available_buoys(buoys=buoys)
        txt_response = Response(content=final_response)
        txt_response.headers["Content-Disposition"] = f'attachment; filename="pnboia_available_buoys.txt"'
        txt_response.headers["Content-Type"] = "text/csv"

        return txt_response

#######################
# MOORED.AXYSGENERAL ENDPOINT
#######################

@router.get("/axys_general", status_code=200, response_model=List[AxysGeneralBase])
def axys_general_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))

    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.axys_general.index(db=db, arguments=arguments)

    return result

#######################
# MOORED.BMOBRRAW ENDPOINT
#######################

@router.get("/bmobr_raw", status_code=200, response_model=List[BmobrRawBase])
def bmobr_raw_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))

    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.bmobr_raw.index(db=db, arguments=arguments)

    return result


#######################
# MOORED.BmobrTriaxysRaw ENDPOINT
#######################

@router.get("/bmobr_triaxys_raw", status_code=200, response_model=List[BmobrTriaxysRawBase])
def bmobr_triaxys_raw_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))

    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.bmobr_triaxys_raw.index(db=db, arguments=arguments)

    return result

#######################
# MOORED.SPOTTERALL ENDPOINT
#######################

@router.get("/spotter_all", status_code=200, response_model=List[SpotterAllBase])
def spotter_general_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))

    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.spotter_all.index(db=db, arguments=arguments)

    return result


#######################
# MOORED.SpotterSmartMooringConfig ENDPOINT
#######################

@router.get("/spotter_smart_mooring_config", status_code=200, response_model=List[SpotterSmartMooringConfigBase])
def spotter_smart_mooring_config_index(
        buoy_id: int,
        token: str,
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {'buoy_id=': buoy_id}

    print(arguments)

    result = crud.crud_moored.spotter_smart_mooring_config.index(db=db, arguments=arguments)

    return result

@router.post("/spotter_smart_mooring_config", response_model=SpotterSmartMooringConfigBase, status_code=201)
def spotter_smart_mooring_config_create(
        token: str,
        obj_in: SpotterSmartMooringConfigNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create new buoy
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )

    result = crud.crud_moored.spotter_smart_mooring_config.create(db=db, obj_in=obj_in)

    return result

@router.put("/spotter_smart_mooring_config/{id}", response_model=SpotterSmartMooringConfigBase, status_code=201)
def spotter_smart_mooring_config_update(
        *,
        id: int,
        token: str,
        obj_in: SpotterSmartMooringConfigNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create new buoy
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )

    result = crud.crud_moored.spotter_smart_mooring_config.index(db=db, arguments = {'id=': id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no smart mooring config with this id",
        )

    result = crud.crud_moored.spotter_smart_mooring_config.update(db=db, id_pk = id, obj_in=obj_in)

    return result

@router.delete("/spotter_smart_mooring_config/{id}", response_model=SpotterSmartMooringConfigBase, status_code=201)
def spotter_smart_mooring_config_update(
        *,
        id: int,
        token: str,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create new buoy
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )

    result = crud.crud_moored.spotter_smart_mooring_config.index(db=db, arguments = {'id=': id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no smart mooring config with this id",
        )

    result = crud.crud_moored.spotter_smart_mooring_config.delete(db=db, id_pk = id)

    return result

#######################
# MOORED.SpotterSystem ENDPOINT
#######################

@router.get("/spotter_system", status_code=200, response_model=List[SpotterSystemBase])
def spotter_system_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))

    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.spotter_system.index(db=db, arguments=arguments)

    return result


#######################
# MOORED.BmobrGeneral ENDPOINT
#######################

@router.get("/bmobr_general", status_code=200, response_model=List[BmobrGeneralBase])
def bmobr_general_index(
        buoy_id: int,
        token: str,
        start_date: Optional[str] = Query(default=(date.today() - timedelta(days=1)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        end_date: Optional[str] = Query(default=(date.today() + timedelta(days=2)),
            title="date_time format is yyyy-mm-dd",
            regex="^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"),
        db: Session = Depends(get_db)
    ) -> Any:

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {}
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date > datetime.utcnow():
        start_date = (datetime.utcnow() - timedelta(days=3))
    if start_date >= end_date:
        start_date = (end_date - timedelta(days=1))
    if (end_date - start_date).days > 10:
        start_date = (end_date - timedelta(days=10))

    arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

    print(arguments)

    result = crud.crud_moored.bmobr_general.index(db=db, arguments=arguments)

    return result

#######################
# MOORED.ALERTS ENDPOINT
#######################

@router.get("/alerts", status_code=200, response_model=List[AlertBase])
def obj_index(
        token: str,
        db: Session = Depends(get_db),
        buoy_id:Optional[int] = None
    ) -> Any:

    """
    Fetch a single alert by buoy_id
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    if buoy_id != None:
        arguments = {'buoy_id=': buoy_id}
    else:
        arguments = {}

    result = crud.crud_moored.alert.index(db=db, arguments=arguments)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is not a alert for this buoy",
        )

    return result



@router.post("/alerts", response_model=AlertBase, status_code=201)
def buoy_create(
        token: str,
        obj_in: AlertNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Create a new alert
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )

    result = crud.crud_moored.alert.index(db=db, arguments = {'buoy_id=': obj_in.buoy_id})

    if result:
        raise HTTPException(
            status_code=400,
            detail="There is already a alert for this buoy",
        )


    result = crud.crud_moored.alert.create(db=db, obj_in=obj_in)

    return result

@router.put("/alerts/{buoy_id}", response_model=AlertBase, status_code=201)
def buoy_update(
        *,
        token: str,
        buoy_id: int,
        obj_in: AlertNewBase,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Update an alert
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})
    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )
    result = crud.crud_moored.alert.index(db=db, arguments = {'buoy_id=': buoy_id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no alert for this buoy",
        )

    result = crud.crud_moored.alert.update(db=db, id_pk = result[0].id, obj_in=obj_in)

    return result

@router.delete("/alerts/{buoy_id}", response_model=AlertBase, status_code=201)
def buoy_update(
        *,
        token: str,
        buoy_id: int,
        db: Session = Depends(get_db)
    ) -> Any:
    """
    Delete an alert
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})
    if not user.user_type == 'admin':
        raise HTTPException(
            status_code=400,
            detail="You do not have permission to do this action",
        )
    result = crud.crud_moored.alert.index(db=db, arguments = {'buoy_id=': buoy_id})

    if not result:
        raise HTTPException(
            status_code=400,
            detail="There is no alert for this buoy",
        )

    result = crud.crud_moored.alert.delete(db=db, id_pk = result[0].id)

    return result
