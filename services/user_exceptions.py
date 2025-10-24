from repository.user_exceptions import UserNotFoundRepo, NotUniqEmailRepo

class UserNotFound(Exception):
    pass
    
class EmailExists(Exception):
    pass

class IncorrectPassword(Exception):
    pass

class InputIncorrectPassword(Exception):
    pass

class IncorrectName(Exception):
    pass

def user_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotUniqEmailRepo:
            raise EmailExists
        except UserNotFoundRepo:
            raise UserNotFound
    return wrapper