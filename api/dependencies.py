
#from repositories.users import UsersRepository
#from services.users import UsersService

from repository.task_Repository import TasksRepository
from services.task_service import TasksService



def tasks_service():
    return TasksService(TasksRepository)


#def users_service():
 #   return UsersService(UsersRepository)