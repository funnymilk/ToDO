from fastapi import APIRouter

from api.endpoints import task_endpoints, user_endpoints


api_router = APIRouter()
api_router.include_router(user_endpoints.router, prefix="/users", tags=["Auth"])
api_router.include_router(task_endpoints.router, prefix="/tasks", tags=["Tasks"])