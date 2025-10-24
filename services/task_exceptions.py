from repository.exceptions import ForeignKeyError, NotFound


class TaskNotFound(Exception):
    pass

class NotFoundUserForTask(Exception):
    pass

def task_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFound:
            raise TaskNotFound
        except ForeignKeyError:
            raise NotFoundUserForTask
    return wrapper


