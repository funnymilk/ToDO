class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str, details: dict | str = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


_RESOURCE_DISPLAY = {
    "user": "Пользователь",
    "task": "Задача",
    "session": "Сессия",
}

# some resources require a gendered verb form or separate phrasing
_RESOURCE_NOT_FOUND = {
    "user": "Пользователь не найден",
    "task": "Задача не найдена",
    "session": "Сессия не найдена",
}


class NotFound(AppError):
    def __init__(self, resource: str | None = None, message: str | None = None, details: dict | str = None):
        if message:
            msg = message
        elif resource in _RESOURCE_NOT_FOUND:
            msg = _RESOURCE_NOT_FOUND[resource]
        elif resource in _RESOURCE_DISPLAY:
            msg = f"{_RESOURCE_DISPLAY[resource]} не найден"
        elif resource:
            msg = f"{resource} не найден"
        else:
            msg = "Ресурс не найден"
        super().__init__(404, "not_found", msg, details)


class Forbidden(AppError):
    def __init__(self, message: str = "Доступ запрещен", details: dict | str = None):
        super().__init__(403, "forbidden", message, details)


class Conflict(AppError):
    def __init__(self, message: str = "Конфликт", details: dict | str = None):
        super().__init__(409, "conflict", message, details)


class ValidationError(AppError):
    def __init__(self, message: str = "Validation error", details: dict | list | str = None):
        super().__init__(422, "validation_error", message, details)


class Unauthorized(AppError):
    def __init__(self, message: str = "Неавторизованный доступ", details: dict | str = None):
        super().__init__(401, "unauthorized", message, details)
