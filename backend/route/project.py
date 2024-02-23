from threading import Thread

from fastapi import APIRouter, Depends, HTTPException

from backend.route.custom_router import LoggingAPIRoute
from backend.configs.dependency.preset_class import AiModules
from backend import dto
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.repository import document

from backend.threading_module.file_thread import trigger_file_thread



router = APIRouter(route_class=LoggingAPIRoute)



@router.post("/ai/add_column")
def add_column(request: dto.AddColumn,
               models: AiModules = Depends(AiModules)):
    is_general = models.column_module.get_is_general_query(request.title)
    return {"isGeneral": is_general}


@router.post("/ai/get_column")
def get_column(request: dto.GetColumn,
               models: AiModules = Depends(AiModules)):

    file_uuid, column_value = models.column_module.get_column_value_by_file(
        column=request.title, file_uuid=request.document_id, is_general_query=request.is_general
    )
    return {"documentId": file_uuid, "value": column_value}

import cProfile

@router.post("/ai/document")
def upload_document(request: dto.UploadDocumentDto, 
                    db: Session = Depends(get_db),
                    models: AiModules = Depends(AiModules)):
    print(request)
    # pr = cProfile.Profile()
    # pr.enable()
    if request.file_type.lower() == "pdf":
        document_path = "s3_mount/files/" + request.path.split("files/")[-1]
    else:
        document_path = request.path

    file_processor = models.file_processor
    
    try:
        processor_data = file_processor.load_file(
            request.document_id, request.project_id, document_path
        )
        title, favicon, screenshot_path = file_processor.get_title_favicon_screenshot_path(
            processor_data
        )
    except Exception as e:
        print(e)
        document.save_fail(db, request.document_id)
        print("save fail")
        raise HTTPException(status_code=500, detail="save error")

    file_thread = Thread(
        target=trigger_file_thread,
        args=(file_processor, processor_data, request.project_id, request.document_id, request.lang, db),
        daemon=True,
    )
    file_thread.start()
    # pr.disable()
    # pr.dump_stats('profile_results.prof')

    return {"title": title, "favicon": favicon}


@router.post("/ai/document/delete")
def delete_document(request: dto.DeleteDocument, models: AiModules = Depends(AiModules)):
    models.file_processor.delete(request.document_id, request.project_id)
    return {"status": "success"}