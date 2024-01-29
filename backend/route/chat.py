import requests

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from backend.route.custom_router import LoggingAPIRoute
from backend.configs.dependency.preset_class import AiModules, get_ai_module
from backend import dto
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.configs.authentication import auth_key_header

from backend.threading_module.chat_thread import (
    get_chat_stream,
    get_dummy_stream,
    get_dummy_stream_error,
)

router = APIRouter(route_class=LoggingAPIRoute)


@router.get("/injection_test")
def testtest(models: AiModules = Depends(AiModules)):
    return {"hi"}

@router.post("/aichat")
async def aichat(
    request: dto.AiChatModel, 
    db: Session = Depends(get_db), 
    token: str = Depends(auth_key_header),
    models: AiModules = Depends(AiModules)
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
    
    print(response.json())
    # return response.json()
    return StreamingResponse(
        get_chat_stream(
            chat_agent=models.chat_agent,
            project_id=request.project_id,
            references=response.json()["data"]["reference"],
            chat_history=response.json()["data"]["history"],
            query=response.json()["data"]["query"],
            db=db,
        )
    )
    
    

@router.post("/aichat_dummy")
def aichat_dummy():
    return StreamingResponse(get_dummy_stream(), media_type="text/event-stream")


@router.get("/aichat_dummy")
async def aichat_dummys():
    return StreamingResponse(get_dummy_stream(), media_type="text/event-stream")


@router.get("/aichat_error")
async def aichat_dummys():
    return StreamingResponse(get_dummy_stream_error(), media_type="text/event-stream")
