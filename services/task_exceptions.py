from repository.task_exceptions import TaskNotFoundRepo


class TaskNotFound(Exception):
    pass

class NotFoundUserForTask(Exception):
    pass

def task_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TaskNotFoundRepo:
            raise TaskNotFound
        except NotFoundUserForTask:
            raise NotFoundUserForTask
    return wrapper


