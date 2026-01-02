from repository.task_exceptions import NotFoundUserForTaskRepo, TaskNotFoundRepo
from api.errors import NotFound

class TaskNotFound(NotFound):
    def __init__(self, details=None):
        super().__init__(resource="task", details=details)

class NotFoundUserForTask(NotFound):
    def __init__(self, details=None):
        super().__init__(resource="user", details=details)


def task_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TaskNotFoundRepo:
            raise TaskNotFound()
        except NotFoundUserForTaskRepo:
            raise NotFoundUserForTask()
    return wrapper


