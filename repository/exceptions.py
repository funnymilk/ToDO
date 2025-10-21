from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation

class NotFound(Exception):    
    pass

class NotUniqEmail(Exception):    
    pass

class ForeignKeyError(Exception):    
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
        except IntegrityError as e:
            self.db.rollback()
            orig = e.orig
            msg = str(orig).lower()

            if "unique" in msg:
                raise NotUniqEmail from e
            elif "foreign key" in msg:
                raise ForeignKeyError from e
            elif isinstance(orig, UniqueViolation):
                raise NotUniqEmail from e
            elif isinstance(orig, ForeignKeyViolation):
                raise ForeignKeyError from e
            
        except SQLAlchemyError:
            raise NotFound
    return wrapper