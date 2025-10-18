from sqlalchemy.exc import SQLAlchemyError

class NotFound(Exception):    
    pass

def exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except NotFound:
            raise NotFound       
    return wrapper

def trans_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except SQLAlchemyError:
            raise SQLAlchemyError        
        return result
    return wrapper