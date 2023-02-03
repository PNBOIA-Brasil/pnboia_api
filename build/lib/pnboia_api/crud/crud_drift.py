from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.drift import *

class CRUDBuoyDrift(CRUDBase[BuoyDrift]):
    ...
class CRUDSpotterGeneral(CRUDBase[SpotterGeneralDrift]):
    ...
class CRUDSpotterSystem(CRUDBase[SpotterSystemDrift]):
    ...
class CRUDSpotterWaves(CRUDBase[SpotterWavesDrift]):
    ...
 
buoy_drift = CRUDBuoyDrift(BuoyDrift)
spotter_general = CRUDSpotterGeneral(SpotterGeneralDrift)
spotter_system = CRUDSpotterSystem(SpotterSystemDrift)
spotter_waves = CRUDSpotterWaves(SpotterWavesDrift)
