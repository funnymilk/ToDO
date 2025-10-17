from repository.exceptions import NotFound


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

def task_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFound:
            raise TaskNotFound
    return wrapper

def user_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFound:
            raise UserNotFound
    return wrapper