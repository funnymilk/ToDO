from fastapi import Request
from fastapi.responses import JSONResponse

from services.auth_exceptions import RefreshSessionNotFound
from services.user_exceptions import EmailExists, IncorrectName, IncorrectPassword, InputIncorrectPassword, UserNotFound
from services.task_exceptions import NotFoundUserForTask, TaskNotFound
from logger.logger import get_logger

logger = get_logger(__name__)

def register_exception_handlers(app):
    @app.exception_handler(TaskNotFound)
    def task_not_found_handler(request: Request, exc: TaskNotFound):
        return JSONResponse(status_code=404, content={"detail": "Таких задач нет"})
    
    @app.exception_handler(EmailExists)
    def task_not_found_handler(request: Request, exc: EmailExists):
        return JSONResponse(status_code=404, content={"detail": "Пользователь с таким e-mail уже существует"})
    
    @app.exception_handler(IncorrectName)
    def task_not_found_handler(request: Request, exc: IncorrectName):
        return JSONResponse(status_code=404, content={"detail": "Имя не может быть одним из списка: admin, test, user"})

    @app.exception_handler(IncorrectPassword)
    def task_not_found_handler(request: Request, exc: IncorrectPassword):
        return JSONResponse(status_code=404, content={"detail": "Пароль должен содержать минимум 8 символов, включая заглавную букву, цифру и специальный символ."})
    
    @app.exception_handler(UserNotFound)
    def task_not_found_handler(request: Request, exc: UserNotFound): 
        return JSONResponse(status_code=404, content={"detail": "Пользователь не найден"})

    @app.exception_handler(InputIncorrectPassword)
    def task_not_found_handler(request: Request, exc: InputIncorrectPassword): 
        return JSONResponse(status_code=404, content={"detail": "Неверный пароль"})
        
    @app.exception_handler(NotFoundUserForTask)
    def task_not_found_handler(request: Request, exc: NotFoundUserForTask): 
        return JSONResponse(status_code=404, content={"detail": "нет такого пользователя"})
    
    @app.exception_handler(RefreshSessionNotFound)
    def refresh_session_not_found_handler(request: Request, exc: RefreshSessionNotFound):
        logger.error("msg", exc_info=exc)
        return JSONResponse(status_code=404, content={"detail": "Сессия не найдена"})