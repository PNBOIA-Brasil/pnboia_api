from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.quality_control import *

class CRUDGeneral(CRUDBase[General]):
    ...
 
general = CRUDGeneral(General)
