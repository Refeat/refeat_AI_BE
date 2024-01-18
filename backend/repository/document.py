from sqlalchemy.orm import Session
from ..db import models
import json
import uuid

def get_document_by_id(db: Session, uuid: str):
    return db.query(models.Document).filter(models.Document.id == uuid).first()

def set_summary_done(db: Session, doc_uuid: str, summary: str):
    document_instance = db.query(models.Document).filter(models.Document.id == uuid.UUID(doc_uuid).bytes).first()
    document_instance.summary_done = True
    document_instance.summary = summary
    db.commit()
    return True

def set_embedding_done(db: Session, doc_uuid: str):
    db.query(models.Document).filter(models.Document.id == uuid.UUID(doc_uuid).bytes).update({"embedding_done": True})
    db.commit()
    return True