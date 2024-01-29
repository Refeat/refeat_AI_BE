from fastapi import APIRouter, Depends
from backend.route.custom_router import LoggingAPIRoute
from backend.dependency.preset_class import AiModules, get_ai_module


test_router = APIRouter(route_class=LoggingAPIRoute)


@test_router.get("/injection_test")
def testtest(models: AiModules = Depends(AiModules)):
    return {"hi"}