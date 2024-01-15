### fastapi app
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn

from backend import dto
from backend.repository import document
from backend.db import models
from backend.db.database import engine, SessionLocal

from ai_module.src.modules.file_to_db.file_processor import FileProcessor

import uuid

models.Base.metadata.create_all(bind=engine)


main_modules = {}

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    main_modules['file_processor'] = FileProcessor(save_dir="s3_mount/json", screenshot_dir="s3_mount/screenshot")
    print("startup")
    


@app.post("/aichat")
def aichat():
    pass


@app.post("/document")
def upload_document(request: dto.UploadDocumentDto, db: Session = Depends(get_db)):
    print(request)
    document_instance = document.get_document_by_id(db, uuid.UUID(request.document_id).bytes )
    print(document_instance.link)
    document_path = "s3_mount/files/" + document_instance.link.split("files/")[-1]

    file_processor = main_modules['file_processor']
    processor_data = file_processor.load_file(request.document_id, request.project_id, document_path)
    title, favicon, screenshot_path = file_processor.get_title_favicon_screenshot_path(processor_data)
    print(title)
    print(favicon)
    print(screenshot_path)
    
    return {"message": "success"}


if __name__ == "__main__":
    uvicorn.run("main_app:app", host="0.0.0.0", port=8000, reload=True)
