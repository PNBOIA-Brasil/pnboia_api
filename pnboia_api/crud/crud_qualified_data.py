from pnboia_api.crud.base import CRUDBase
from pnboia_api.models.qualified_data import *
from sqlalchemy.orm import Session

from typing import List
from sqlalchemy import desc
from sqlalchemy.orm import Session

class CRUDQualifiedData(CRUDBase[QualifiedData]):

    def last(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        last:bool = True,
        buoy_sel:bool = False,
        arguments: dict = None
    ) -> List[QualifiedData]:

        if arguments:
            query = self.create_query(arguments)
        else:
            query = "true"

        if last:
            if buoy_sel:
                # result = db.query(self.model).filter(text(query)).order_by(desc(self.model.date_time)).all()
                result = db.query(self.model).filter(text(query)).distinct(self.model.buoy_id).order_by(desc(self.model.buoy_id)).order_by(desc(self.model.date_time)).all()

            else:
                result = db.query(self.model).distinct(self.model.buoy_id).order_by(desc(self.model.buoy_id)).order_by(desc(self.model.date_time)).all()


        else:
            result = db.query(self.model).distinct(self.model.buoy_id).order_by(desc(self.model.buoy_id)).order_by(self.model.date_time).all()

        if not result:
            raise HTTPException(
                status_code=404, detail=f"{self.model} with {arguments} not found"
            )

        return result

qualified_data = CRUDQualifiedData(QualifiedData)

spotter_qualified_data = CRUDQualifiedData(SpotterQualified)
triaxys_qualified_data = CRUDQualifiedData(TriaxysQualified)
bmobr_qualified_data = CRUDQualifiedData(BMOBrQualified)
pnboia_qualified_data = CRUDQualifiedData(PNBoiaQualified)
criosfera_qualified_data = CRUDQualifiedData(CriosferaQualified)
