from sqlalchemy.orm import Session
from ..db import models

def get_document_by_id(db: Session, uuid: str):
    return db.query(models.Document).filter(models.Document.id == uuid).first()