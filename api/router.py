from fastapi import APIRouter

from api.endpoints import auth_endpoints, task_endpoints, user_endpoints


api_router = APIRouter()
api_router.include_router(user_endpoints.router, prefix="/users", tags=["Users"])
api_router.include_router(task_endpoints.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(auth_endpoints.router, prefix="/auth", tags=["Auth"])