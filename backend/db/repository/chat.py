from sqlalchemy.orm import Session
from .. import models
from typing import Dict
import datetime


def add_ai_chat(db: Session, project_id: str, chat: str, reference: Dict[str, Dict[str, int]]):
    document_list = list()
    position_list = list()
    print(reference)
    for key, value in reference.items():
        document_list.append(key)
        position_list.append(",".join(list(map(str, value.values()))[:-1]))
    db_chat = models.Chat(
        content=chat,
        content_refined=chat,
        project=project_id,
        reference=",".join(document_list),
        position="|".join(position_list),
        user=1,
        created_at=datetime.datetime.now(),
    )
    db.add(db_chat)
    db.commit()
    return db_chat
