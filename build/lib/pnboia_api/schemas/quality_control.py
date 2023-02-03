# coding: utf-8
from pydantic import BaseModel, HttpUrl, validator, Json
from typing import Optional, Any, List

class GeneralBase(BaseModel):

    id: Optional[int]
    buoy_id: Optional[int]
    qc_config: Optional[dict]

    class Config:
        orm_mode = True