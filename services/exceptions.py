from repository.exceptions import NotFound
from sqlalchemy.exc import SQLAlchemyError

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

class TaskNotFound(Exception):
    pass

class TransactionError(Exception):
    pass

def task_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFound:
            raise TaskNotFound
        except SQLAlchemyError:
            raise TransactionError
    return wrapper

def user_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFound:
            raise UserNotFound
        except SQLAlchemyError:
            raise TransactionError
    return wrapper