# app/api/deps.py
from sqlalchemy.orm import Session

from app.db.session import SessionLocal  # Make sure your DB session is defined here


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
