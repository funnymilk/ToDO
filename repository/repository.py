from abc import ABC, abstractmethod

class AbstractRepositoryTask(ABC):
    @abstractmethod
    def add_one():
        raise NotImplementedError
    
    @abstractmethod
    def get_one():
        raise NotImplementedError
    
    @abstractmethod
    def get_all():
        raise NotImplementedError
    
    @abstractmethod
    def get_isdone():
        raise NotImplementedError
    
    @abstractmethod
    def get_user_tasks():
        raise NotImplementedError
    
    @abstractmethod
    def up_task():
        raise NotImplementedError
    
    @abstractmethod
    def del_task():
        raise NotImplementedError
    
    
class AbstractRepositoryUser(ABC):
    @abstractmethod
    def get_user():
        raise NotImplementedError
    
    @abstractmethod
    def create_user():
        raise NotImplementedError
    
    @abstractmethod
    def login_check():
        raise NotImplementedError