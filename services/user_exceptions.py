from repository.exceptions import NotFound, NotUniqEmail

class UserNotFound(Exception):
    pass
    
class EmailExists(Exception):
    pass

class IncorrectName(Exception):
    pass

class IncorrectPassword(Exception):
    pass

class InputIncorrectPassword(Exception):
    pass

class TransactionError(Exception):
    pass

def user_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotUniqEmail:
            raise EmailExists
        except NotFound:
            raise UserNotFound
    return wrapper