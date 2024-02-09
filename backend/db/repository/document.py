from sqlalchemy.orm import Session
from .. import models
import json
import uuid


def get_document_by_id(db: Session, uuid: str):
    return db.query(models.Document).filter(models.Document.id == uuid).first()

def set_save_done(db: Session, doc_uuid: str):
    db.query(models.Document).filter(models.Document.id == uuid.UUID(doc_uuid).bytes).update(
        {"save_done": 1}
    )
    db.commit()
    return True

def set_summary_done(db: Session, doc_uuid: str, summary: str):
    document_instance: models.Document = (
        db.query(models.Document).filter(models.Document.id == uuid.UUID(doc_uuid).bytes).first()
    )
    document_instance.summary_done = 1
    document_instance.summary = summary
    db.commit()
    return True


def set_embedding_done(db: Session, doc_uuid: str):
    db.query(models.Document).filter(models.Document.id == uuid.UUID(doc_uuid).bytes).update(
        {"embedding_done": 1}
    )
    db.commit()
    return True


def save_fail(db: Session, doc_uuid):
    db.query(models.Document).filter(models.Document.id == uuid.UUID(doc_uuid).bytes).update(
        {"save_done": 2}
    )
    db.commit()
    return True

def summary_fail(db: Session, doc_uuid):
    db.query(models.Document).filter(models.Document.id == uuid.UUID(doc_uuid).bytes).update(
        {"summary_done": 2}
    )
    db.commit()
    return True

def embedding_fail(db: Session, doc_uuid):
    db.query(models.Document).filter(models.Document.id == uuid.UUID(doc_uuid).bytes).update(
        {"embedding_done": 2}
    )
    db.commit()
    return True
