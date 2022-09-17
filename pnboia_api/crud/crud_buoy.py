from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.buoy import Buoy

class CRUDBuoy(CRUDBase[Buoy]):
    ...

buoy = CRUDBuoy(Buoy)