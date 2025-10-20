from sqlalchemy.exc import SQLAlchemyError, IntegrityError

class NotFound(Exception):    
    pass

class NotUniqEmail(Exception):    
    pass

def exceptions_trap(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:                     
                raise NotFound
            return result
        except SQLAlchemyError:
            raise NotFound
    return wrapper

def trans_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            result = func(*args, **kwargs)
            return result
        except IntegrityError:
            self.db.rollback()
            raise NotUniqEmail
    return wrapper