from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.drift import *

class CRUDBuoyDrift(CRUDBase[BuoyDrift]):
    ...
class CRUDSpotterGeneral(CRUDBase[SpotterGeneral]):
    ...
class CRUDSpotterSystem(CRUDBase[SpotterSystem]):
    ...
class CRUDSpotterWaves(CRUDBase[SpotterWaves]):
    ...
 
buoy_drift = CRUDBuoyDrift(BuoyDrift)
spotter_all = CRUDSpotterGeneral(SpotterGeneral)
spotter_system = CRUDSpotterSystem(SpotterSystem)
spotter_waves = CRUDSpotterWaves(SpotterWaves)
