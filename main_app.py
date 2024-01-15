### fastapi app
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn
from backend import dto
from backend.repository import document
from backend.db import models
from backend.db.database import engine, SessionLocal

import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/aichat")
def aichat():
    pass


@app.post("/document")
def upload_document(request: dto.UploadDocumentDto, db: Session = Depends(get_db)):
    print(request)
    document_instance = document.get_document_by_id(db, uuid.UUID(request.document_id).bytes )
    print(document_instance.link)
    return {"message": "success"}


if __name__ == "__main__":
    uvicorn.run("main_app:app", host="0.0.0.0", port=8000, reload=True)
