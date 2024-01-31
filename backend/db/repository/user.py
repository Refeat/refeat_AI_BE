from sqlalchemy.orm import Session
from .. import models

def get_user(db: Session, user_id: int = 1):
    db_chat = db.query(models.UserInfo).filter(models.UserInfo.id == user_id).first()
    return db_chat