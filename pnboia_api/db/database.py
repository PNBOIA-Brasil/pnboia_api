from sqlalchemy.orm import Session
from .base import SessionLocal

def get_db():
    """Dependency that provides a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
