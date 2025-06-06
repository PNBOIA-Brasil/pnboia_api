from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.moored import *
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List, TypeVar
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBuoy(CRUDBase[Buoy]):
    def index(
        self, db: Session, *, skip: int = 0, limit: int = 100, order: bool = False, arguments: dict = None
    ) -> List[Buoy]:

        if arguments:
            query = self.create_query(arguments)
        else:
            query = "true"
        if order:
            result = db.query(self.model).filter(text(query)).order_by(desc(self.model.status)).order_by(self.model.name).all()
        else:
            result = db.query(self.model).filter(text(query)).all()

        return result

class CRUDAxysAdcp(CRUDBase[AxysAdcp]):
    ...
class CRUDAxysGeneral(CRUDBase[AxysGeneral]):
    ...
class CRUDBmobrGeneral(CRUDBase[BmobrGeneral]):
    ...
class CRUDBmobrRaw(CRUDBase[BmobrRaw]):
    ...
class CRUDBmobrTriaxysRaw(CRUDBase[BmobrTriaxysRaw]):
    ...
class CRUDCriosferaGeneral(CRUDBase[CriosferaGeneral]):
    ...
class CRUDSpotterAll(CRUDBase[SpotterAll]):
    ...
class CRUDSpotterSmartMooringConfig(CRUDBase[SpotterSmartMooringConfig]):
    ...
class CRUDSpotterSystem(CRUDBase[SpotterSystem]):
    ...
class CRUDTriaxysGeneral(CRUDBase[TriaxysGeneral]):
    ...
class CRUDTriaxysRaw(CRUDBase[TriaxysRaw]):
    ...
class CRUDTriaxysStatus(CRUDBase[TriaxysStatus]):
    ...

class CRUDAlert(CRUDBase[Alert]):
    ...

class CRUDSetupBuoy(CRUDBase[SetupBuoy]):
    ...
class CRUDBuoysMetadata(CRUDBase[BuoysMetadata]):
    ...
class CRUDParameters(CRUDBase[Parameters]):
    def index_parameters(
        self,
        db: Session,
        *,
        skip: int = 0,
        order:bool = False,
        limit: int = None,
        arguments: dict = None,
    ) -> List[ModelType]:

        if arguments:
            query = self.create_query(arguments)
        else:
            query = "true"

        if limit:
            if order:
                result = db.query(self.model).filter(text(query)).order_by(self.model.id).limit(limit).all()
            else:
                result = db.query(self.model).filter(text(query)).limit(limit).all()

        elif order:
            result = db.query(self.model).filter(text(query)).order_by(self.model.id).all()
        else:
            result = db.query(self.model).filter(text(query)).all()

        return result

class CRUDRegisterBuoys(CRUDBase[RegisterBuoys]):
    def index_register(
        self,
        db: Session,
        *,
        skip: int = 0,
        order:bool = False,
        limit: int = None,
        arguments: dict = None,
    ) -> List[ModelType]:

        if arguments:
            query = self.create_query(arguments)
        else:
            query = "true"

        if limit:
            if order:
                result = db.query(self.model).filter(text(query)).order_by(self.model.start_date).limit(limit).all()
            else:
                result = db.query(self.model).filter(text(query)).limit(limit).all()

        elif order:
            result = db.query(self.model).filter(text(query)).order_by(self.model.start_date).all()
        else:
            result = db.query(self.model).filter(text(query)).all()

        return result


buoy = CRUDBuoy(Buoy)
axys_adcp = CRUDAxysAdcp(AxysAdcp)
axys_general = CRUDAxysGeneral(AxysGeneral)
bmobr_general = CRUDBmobrGeneral(BmobrGeneral)
bmobr_raw = CRUDBmobrRaw(BmobrRaw)
bmobr_triaxys_raw = CRUDBmobrTriaxysRaw(BmobrTriaxysRaw)
criosfera_general = CRUDCriosferaGeneral(CriosferaGeneral)
spotter_all = CRUDSpotterAll(SpotterAll)
spotter_smart_mooring_config = CRUDSpotterSmartMooringConfig(SpotterSmartMooringConfig)
spotter_system = CRUDSpotterSystem(SpotterSystem)
triaxys_general = CRUDTriaxysGeneral(TriaxysGeneral)
triaxys_raw = CRUDTriaxysRaw(TriaxysRaw)
triaxys_status = CRUDTriaxysStatus(TriaxysStatus)
alert = CRUDAlert(Alert)
setup_buoy = CRUDSetupBuoy(SetupBuoy)
buoys_metadata = CRUDBuoysMetadata(BuoysMetadata)
parameters = CRUDParameters(Parameters)
register_buoys = CRUDRegisterBuoys(RegisterBuoys)
