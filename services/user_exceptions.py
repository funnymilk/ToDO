from repository.user_exceptions import UserNotFoundRepo, NotUniqEmailRepo
from api.errors import NotFound, Conflict, ValidationError

class UserNotFound(NotFound):
    def __init__(self, details=None):
        super().__init__(resource="user", details=details)
        
class EmailExists(Conflict):
    def __init__(self, details=None):
        super().__init__(message="Пользователь с таким e-mail уже существует", details=details)

class IncorrectPassword(ValidationError):
    def __init__(self, message: str = "Пароль должен содержать минимум 8 символов, включая заглавную букву, цифру и специальный символ.", details=None):
        super().__init__(message=message, details=details)

class InputIncorrectPassword(ValidationError):
    def __init__(self, message: str = "Неверный пароль", details=None):
        super().__init__(message=message, details=details)

class IncorrectName(ValidationError):
    def __init__(self, message: str = "Имя не может быть одним из списка: admin, test, user", details=None):
        super().__init__(message=message, details=details)


def user_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotUniqEmailRepo:
            raise EmailExists()
        except UserNotFoundRepo:
            raise UserNotFound()
    return wrapper