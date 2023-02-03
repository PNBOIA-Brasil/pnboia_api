from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.qualified_data import *

class CRUDQualifiedData(CRUDBase[QualifiedData]):
    ...

qualified_data = CRUDQualifiedData(QualifiedData)
