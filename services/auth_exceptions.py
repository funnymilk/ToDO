from repository.auth_exceptions import RefreshSessionNotFoundRepo, NotFoundUserForAuthRepo
from api.errors import NotFound

class RefreshSessionNotFound(NotFound):
    def __init__(self, details=None):
        super().__init__(resource="session", details=details)

class NotFoundUserForAuth(NotFound):
    def __init__(self, details=None):
        super().__init__(resource="user", details=details)


def auth_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundUserForAuthRepo:
            raise NotFoundUserForAuth(details={"user_id": e.user_id}) from e
        except RefreshSessionNotFoundRepo as e :
            raise RefreshSessionNotFound() from e
    return wrapper