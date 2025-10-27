from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from psycopg2.errors import UniqueViolation

class UserNotFoundRepo(Exception):    
    pass

class NotUniqEmailRepo(Exception):    
    pass

def user_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            result = func(*args, **kwargs)
            if not result:
                raise UserNotFoundRepo
            return result
        except IntegrityError as e:
            self.db.rollback()
            orig = e.orig
            msg = str(orig).lower()
            if "unique" in msg:
                raise NotUniqEmailRepo from e
            if isinstance(orig, UniqueViolation):
                raise NotUniqEmailRepo from e            
        except SQLAlchemyError:
            raise UserNotFoundRepo
    return wrapper