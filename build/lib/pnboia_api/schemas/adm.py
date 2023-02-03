# coding: utf-8
from pydantic import BaseModel, EmailStr
from typing import Optional, Any, List


class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr] = None
    user_type: Optional[str]
    password: Optional[str]
    token: Optional[str]

    class Config:
        orm_mode = True
