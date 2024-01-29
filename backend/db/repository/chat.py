from sqlalchemy.orm import Session
from .. import models
from typing import List, Dict
import json
import uuid


def add_ai_chat(db: Session, project_id: str, chat: str, reference:Dict[str, Dict[str, int]]):
    document_list = list()
    position_list = list()
    print(reference)
    for key, value in reference.items():
        document_list.append(key)
        position_list.append(",".join(list(map(str,value.values()))))
    db_chat = models.Chat(content=chat, project=project_id, reference=",".join(document_list), position = "|".join(position_list), user=1)
    db.add(db_chat)
    db.commit()
    return db_chat