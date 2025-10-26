from repository.task_exceptions import NotFoundUserForTaskRepo, TaskNotFoundRepo


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
        except NotFoundUserForTaskRepo:
            raise NotFoundUserForTask
    return wrapper


