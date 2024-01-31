from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.repository.user import get_user
from fastapi import Depends


def db_check(db: Session):
    user = get_user(db)
    return user