from repository.task_Repository import TasksRepository
from repository.user_Repository import UsersRepository
from services.task_service import TasksService
from services.user_service import UsersService

def tasks_service():
    return TasksService(TasksRepository)

def users_service():
    return UsersService(UsersRepository)
