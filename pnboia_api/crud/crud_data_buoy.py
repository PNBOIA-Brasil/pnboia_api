from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.data_buoy import DataBuoy

class CRUDDataBuoy(CRUDBase[DataBuoy]):
    ...

data_buoy = CRUDDataBuoy(DataBuoy)