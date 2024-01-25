### fastapi app
import sys
import uuid

sys.path.append("ai_module/src")

from sqlalchemy.orm import Session
import uvicorn
from threading import Thread
import requests

from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader

from backend import dto
from backend.repository import document
from backend.db import models
from backend.db.database import engine, get_db
from backend.preset_class import required_classes

from ai_module.src.modules.file_to_db.file_processor import FileProcessor
from backend.threading_module.file_thread import trigger_file_thread
from backend.threading_module.chat_thread import get_chat_stream, get_dummy_stream
from ai_module.src.modules.chat.custom_chat_agent_module import ChatAgentModule

models.Base.metadata.create_all(bind=engine)

main_modules = {}

app = FastAPI()
auth_key_header = APIKeyHeader(name="Authorization")


@app.on_event("startup")
def startup_event():
    es = required_classes["CustomElasticSearch"]
    # es._create_index()  # delete index and create new index
    main_modules["file_processor"] = FileProcessor(
        es=es,
        summary_chain=required_classes["SummaryChain"],
        knowledge_graph_db=required_classes["KnowledgeGraphDatabase"],
        save_dir="s3_mount/json/",
        screenshot_dir="s3_mount/screenshot/",
    )
    main_modules["chat_agent"] = ChatAgentModule(
        verbose=True, es=es, knowledge_graph_db=required_classes["KnowledgeGraphDatabase"]
    )
    print("startup")


@app.post("/aichat")
def aichat(
    request: dto.AiChatModel, db: Session = Depends(get_db), token: str = Depends(auth_key_header)
):
    print(request.query)
    print(token)

    response = requests.post(
        "http://192.168.0.124:8080/chat/aichat",
        json={"projectId": request.project_id, "query": request.query},
        headers={"Authorization": token},
    )
    if response.status_code != 200:
        return response.json()
    # return response.json()
    return StreamingResponse(
        get_chat_stream(
            chat_agent=main_modules["chat_agent"],
            project_id=request.project_id,
            file_uuid=response.json()["data"]["reference"],
            chat_history=response.json()["data"]["history"],
            query=response.json()["data"]["query"],
        )
    )


@app.post("/aichat_dummy")
def aichat_dummy():
    return StreamingResponse(get_dummy_stream(), media_type="text/event-stream")


@app.get("/aichat_dummy")
async def aichat_dummys():
    return StreamingResponse(get_dummy_stream(), media_type="text/event-stream")


@app.post("/document")
def upload_document(request: dto.UploadDocumentDto, db: Session = Depends(get_db)):
    print(request)
    if request.file_type.lower() == "pdf":
        document_path = "s3_mount/files/" + request.path.split("files/")[-1]
    else:
        document_path = request.path

    file_processor = main_modules["file_processor"]
    processor_data = file_processor.load_file(
        request.document_id, request.project_id, document_path
    )
    title, favicon, screenshot_path = file_processor.get_title_favicon_screenshot_path(
        processor_data
    )

    file_thread = Thread(
        target=trigger_file_thread,
        args=(file_processor, processor_data, request.project_id, request.document_id, db), daemon=True,
    )
    file_thread.start()

    return {"title": title, "favicon": favicon}

@app.post("/document/delete")
def delete_document(request: dto.DeleteDocument):
    file_processor = main_modules["file_processor"]
    file_processor.delete(request.document_id, request.project_id)
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run("main_app:app", host="0.0.0.0", port=8000, reload=True)
