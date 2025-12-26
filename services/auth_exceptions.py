from repository.auth_exceptions import RefreshSessionNotFoundRepo, NotFoundUserForAuthRepo

class RefreshSessionNotFound(Exception):
    pass

class NotFoundUserForAuth(Exception):
    pass


def auth_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundUserForAuthRepo:
            raise NotFoundUserForAuth
        except RefreshSessionNotFoundRepo as e :
            raise RefreshSessionNotFound from e
    return wrapper