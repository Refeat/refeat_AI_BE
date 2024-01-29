### fastapi app
import sys
sys.path.append("ai_module/src")

import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from backend.db import models
from backend.db.database import engine
from backend.configs.dependency.preset_class import AiModules
from backend.route.router import api_router

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
    AiModules()


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main_app:app", host="0.0.0.0", port=8000, reload=True)
