from sqlalchemy.orm import Session
from .. import models
from typing import Dict
import datetime
import base64
import uuid


def add_ai_chat(db: Session, project_id: str, chat: str, reference: Dict[str, Dict[str, int]]):
    document_list = list()
    chunk_list = list()
    index_list = list()
    print(reference)
    for key, value in reference.items():
        index_list.append(key)
        document_list.append(value["file_uuid"])
        chunk_list.append(value["text"])
        
    db_chat = models.Chat(
        content=chat,
        content_refined=chat,
        project=project_id,
        # reference=",".join(document_list),
        reference="",
        user=1,
        created_at=datetime.datetime.now(),
    )
    
    db.add(db_chat)
    db.commit()
    
    for i in range(len(index_list)):
        reference = models.Reference(
            index_number = index_list[i],
            document_id = uuid.UUID(document_list[i]).bytes,
            chunk=chunk_list[i],
            chat = db_chat.id
        )
        db.add(reference)
        db.commit()
    
    return db_chat
