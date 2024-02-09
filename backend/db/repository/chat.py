from sqlalchemy.orm import Session
from .. import models
from typing import Dict
import datetime


def add_ai_chat(db: Session, project_id: str, chat: str, reference: Dict[str, Dict[str, int]]):
    document_list = list()
    chunk_list = list()
    print(reference)
    for key, value in reference.items():
        document_list.append(key)
        chunk_list.append(value["text"])
    db_chat = models.Chat(
        content=chat,
        content_refined=chat,
        project=project_id,
        reference=",".join(document_list),
        chunk_text="|".join(chunk_list),
        user=1,
        created_at=datetime.datetime.now(),
    )
    db.add(db_chat)
    db.commit()
    return db_chat
