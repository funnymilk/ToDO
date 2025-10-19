from sqlalchemy.exc import SQLAlchemyError

class NotFound(Exception):    
    pass

def exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:                     
                raise NotFound(f"{func.__name__}: object not found")
            return result
        except SQLAlchemyError as e:
            raise NotFound(f"Database error: {e}")
    return wrapper

def trans_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except NotFound:
            raise SQLAlchemyError        
        return result
    return wrapper