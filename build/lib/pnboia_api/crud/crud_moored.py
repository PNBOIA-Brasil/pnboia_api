from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.moored import *

class CRUDBuoy(CRUDBase[Buoy]):
    ...
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
