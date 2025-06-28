from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Query
from typing import Optional
import os
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

def verify_token(token: str = Query(..., description="API token for authentication")):
    """
    Verify the API token from query parameters.
    
    Args:
        token: The API token to verify
        
    Returns:
        bool: True if token is valid
        
    Raises:
        HTTPException: If token is invalid
    """
    # Get the valid token from environment variables
    valid_token = os.getenv("API_TOKEN")
    
    # If no token is set in environment, allow all requests (for development)
    if valid_token is None:
        return True
        
    # Verify the token
    if token != valid_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Token"
        )
    return True
