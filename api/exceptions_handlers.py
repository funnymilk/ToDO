from fastapi import Request
from fastapi.responses import JSONResponse

from services.exceptions import TaskNotFound

def register_exception_handlers(app):
    @app.exception_handler(TaskNotFound)
    def task_not_found_handler(request: Request, exc: TaskNotFound):
        return JSONResponse(status_code=404, content={"detail": "Таких задач нет"})
