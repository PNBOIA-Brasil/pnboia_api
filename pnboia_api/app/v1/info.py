import pandas as pd
import numpy as np

from typing import Optional, Any, List
from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse, FileResponse, Response
from fastapi.encoders import jsonable_encoder


from sqlalchemy.orm import Session

from pnboia_api.schemas.qualified_data import *
from pnboia_api.schemas.moored import *

from pnboia_api.models.qualified_data import *

import pnboia_api.crud as crud

from  pnboia_api.db.base import Base, engine
from datetime import datetime, timedelta, date

from pnboia_api.app.deps import get_db

from pnboia_api.app.utils import APIUtils, HTMLUtils, TXTUtils, JSONUtils

Base.metadata.create_all(bind=engine)

router = APIRouter()

#######################
# QUALIFIED_DATA.QualifiedData ENDPOINT
#######################

@router.get("/metadata", status_code=200) #response_model=List[SetupBuoySchema]) #response_class=PlainTextResponse)
def return_metadata(
            buoy_id: int,
            token: str,
            db: Session = Depends(get_db),
            response_type:str="html"
):

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    buoy = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

    if not buoy.open_data and not user.user_type == 'admin':
        if not user.user_type == 'admin':
            raise HTTPException(
                status_code=400,
                detail="You do not have permission to do this action",
            )

    register_buoys = crud.crud_moored.register_buoys.index_register(db=db, arguments={'buoy_id=': buoy_id}, order=True)

    buoy_type = buoy.name.split(" ")[0:2]
    setup_buoys = crud.crud_moored.setup_buoy.index(db=db)
    buoys_metadata = crud.crud_moored.buoys_metadata.index(db=db, arguments={'buoy_id=': buoy_id})
    parameters_moored = crud.crud_moored.parameters.index_parameters(db=db, order=True)

    if buoy_type[0] == "SPOTTER":
        buoy_params = list(SpotterQualifiedSchema.__fields__.keys())
    if buoy_type[0] == "TRIAXYS":
            buoy_params = list(TriaxysQualifiedSchema.__fields__.keys())
    if buoy_type[0] == "METOCEAN" and buoy_type[1] != "CRIOSFERA":
        buoy_params = list(BMOBrQualifiedSchema.__fields__.keys())
    if buoy_type[0] == "METOCEAN" and buoy_type[1] == "CRIOSFERA":
        buoy_params = list(CriosferaQualifiedSchema.__fields__.keys())



    if response_type == 'html':
        final_response = HTMLUtils().compose_final_response(buoy=buoy,
                                                     buoys_metadata=buoys_metadata,
                                                     register_buoys=register_buoys,
                                                     setup_buoys=setup_buoys,
                                                     buoy_parameters=buoy_params,
                                                     buoy_type=buoy_type,
                                                     parameters=parameters_moored)
        return HTMLResponse(final_response)

    elif response_type == "txt":

        final_response = TXTUtils().compose_final_response(buoy=buoy,
                                                     buoys_metadata=buoys_metadata,
                                                     setup_buoys=setup_buoys,
                                                     buoy_parameters=buoy_params,
                                                     buoy_type=buoy_type,
                                                     parameters=parameters_moored)

        txt_response = Response(content=final_response)
        file_name = TXTUtils().file_name_composition(buoy_name=buoy.name)
        txt_response.headers["Content-Disposition"] = f'attachment; filename="{file_name}.txt"'
        txt_response.headers["Content-Type"] = "text/csv"

        return txt_response

    elif response_type == "json":
        final_response = JSONUtils().compose_final_response(buoy=buoy,
                                                     buoys_metadata=buoys_metadata,
                                                     register_buoys=register_buoys,
                                                     setup_buoys=setup_buoys,
                                                     buoy_parameters=buoy_params,
                                                     buoy_type=buoy_type,
                                                     parameters=parameters_moored)
        return JSONResponse(jsonable_encoder(final_response))

    else:
        raise HTTPException(
                status_code=400,
                detail=f"Invalid response type. ['html', 'json' or 'txt'] available.",
            )


@router.get("/available_buoys", status_code=200, response_model=List[AvailableBuoysSchema])
def obj_index(
        token: str,
        db: Session = Depends(get_db),
        order:Optional[bool]=False,
        operative:Optional[bool]=False,
        response_type:Optional[str]='html'
    ) -> Any:

    """
    Fetch list of available buoys
    """

    user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

    arguments = {'open_data=': True}

    if operative:
        arguments.update({"status=": True})


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

    else:
        raise HTTPException(
                status_code=400,
                detail=f"Invalid response type. ['html', 'json' or 'txt'] available.",
            )


# @router.get("/pnboia", status_code=200, response_model=List[PNBoiaQualifiedSchema])
# def qualified_data_index(
#         buoy_id: int,
#         token: str,
#         start_date: Optional[str] = Query(default=(datetime.utcnow().replace(microsecond=0) - timedelta(days=1)),
#                     title="date_time format is yyyy-mm-ddTHH:MM:SS",
#                     regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
#         end_date: Optional[str] = Query(default=(datetime.utcnow().replace(microsecond=0) + timedelta(days=2)),
#                     title="date_time format is yyyy-mm-ddTHH:MM:SS",
#                     regex="\d{4}-\d?\d-\d?\dT(?:2[0-3]|[01]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]"),
#         db: Session = Depends(get_db),
#         limit: int = None,
#         response_type:str="json"
#     ) -> Any:

#     user = crud.crud_adm.user.verify(db=db, arguments={'token=': token})

#     arguments = {}
#     try:
#         start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
#         end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
#     except:
#         start_date = datetime.combine(start_date, datetime.min.time())
#         end_date = datetime.combine(end_date, datetime.min.time())

#     if end_date < start_date:
#         raise HTTPException(
#                 status_code=400,
#                 detail="Provided start date is more recent then the end date.",
#             )

#     if start_date > datetime.utcnow():
#         start_date = (datetime.utcnow() - timedelta(days=3))
#     if start_date >= end_date:
#         raise HTTPException(
#                 status_code=400,
#                 detail=f"Provided start date is more recent than the provided end date. Please review your requested period.",
#             )
#     if (end_date - start_date).days > 30:
#         end_date = (start_date + timedelta(days=30))


#     arguments = {'buoy_id=': buoy_id, 'date_time>=': start_date.strftime("%Y-%m-%d"), 'date_time<=': end_date.strftime("%Y-%m-%d")}

#     buoy = crud.crud_moored.buoy.show(db=db, id_pk = buoy_id)

#     if "METOCEAN" not in buoy.name:
#         raise HTTPException(
#                 status_code=400,
#                 detail=f"Please check in the PNBoia documentation if the correct endpoint is being used for the required buoy (Buoy ID = {buoy_id}).",
#             )

#     if not buoy.open_data and not user.user_type == 'admin':
#         if not user.user_type == 'admin':
#             raise HTTPException(
#                 status_code=400,
#                 detail="You do not have permission to do this action",
#             )
#     else:
#         result = crud.crud_qualified_data.pnboia_qualified_data.index(db=db, order=True, arguments=arguments, limit=limit)

#     if not result:
#         raise HTTPException(
#                 status_code=400,
#                 detail=f"No data for buoy {buoy_id} for the period.",
#             )

#     if response_type == "csv":
#         filename = APIUtils().file_name_composition(buoy_name=buoy.name, start_date=start_date, end_date=end_date)
#         return APIUtils().csv_response(result=result, filename=filename)
#     elif response_type == "json":
#         return result
