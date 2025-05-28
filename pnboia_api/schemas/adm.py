# coding: utf-8
from pydantic import BaseModel, EmailStr
from typing import Optional, Any, List


class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    user_type: Optional[str] = 'normal'
    password: Optional[str]
    token: Optional[str]

    class Config:
        orm_mode = True

class UserCreateBase(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    user_type: Optional[str]
    token: Optional[str]

    class Config:
        orm_mode = True

class UserUpdateBase(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    token: Optional[str]

    class Config:
        orm_mode = True

class UserShowBase(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    user_type: Optional[str]
    token: Optional[str]

    class Config:
        orm_mode = True
