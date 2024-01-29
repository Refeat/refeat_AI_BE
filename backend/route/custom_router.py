from fastapi.routing import APIRoute, APIRouter
from typing import Any, Callable, Dict
from starlette.requests import Request
from starlette.responses import Response
from backend.log.logger import logger

class LoggingAPIRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            await self._request_log(request)
            response: Response = await original_route_handler(request)
            # self._response_log(request, response)
            return response

        return custom_route_handler

    @staticmethod
    def _has_json_body(request: Request) -> bool:
        if (
					request.method in ("POST", "PUT", "PATCH") 
	        and request.headers.get("content-type") == "application/json"
				):
            return True
        return False

    async def _request_log(self, request: Request) -> None:
        extra: Dict[str, Any] = {
				  "httpMethod": request.method,
          "url": request.url.path,
          "headers": request.headers,
          "queryParams": request.query_params,
        }

        if self._has_json_body(request):
            request_body = await request.body()
            extra["body"] = request_body.decode("UTF-8")
        logger.info(f"request{extra}")