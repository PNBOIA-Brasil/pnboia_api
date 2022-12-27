from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status

import random
import string


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)

def create_token(length):
    letters = string.ascii_letters + string.digits + "_" + "-"
    return ''.join(random.choice(letters) for i in range(length))

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials"
)
