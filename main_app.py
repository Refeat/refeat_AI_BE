### fastapi app
import sys
sys.path.append("ai_module/src")

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import models
from backend.db.database import engine, get_db
from backend.configs.dependency.preset_class import AiModules
from backend.route.router import api_router
from backend.scheduler.tasks import db_check

models.Base.metadata.create_all(bind=engine)

main_modules = {}

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    AiModules() ## initialize ai modules(singleton)
    scheduler = BackgroundScheduler()
    db = next(get_db())
    scheduler.add_job(db_check, 'cron', minute='*/30', kwargs={"db": db})
    scheduler.start()

@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main_app:app", host="0.0.0.0", port=8000, reload=False)
