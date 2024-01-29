from fastapi import APIRouter
from backend.route.custom_router import LoggingAPIRoute


router = APIRouter(route_class=LoggingAPIRoute)