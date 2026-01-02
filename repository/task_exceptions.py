from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from psycopg2.errors import ForeignKeyViolation

class TaskNotFoundRepo(Exception):    
    pass

class NotFoundUserForTaskRepo(Exception):    
    pass

def task_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            result = func(*args, **kwargs)
            # Only treat explicit 'None' as not found. Empty lists/tuples are valid results.
            if result is None:
                raise TaskNotFoundRepo
            return result
        except IntegrityError as e:
            self.db.rollback()
            orig = e.orig
            msg = str(orig).lower()
            if "foreign key" in msg:
                raise NotFoundUserForTaskRepo from e
            if isinstance(orig, ForeignKeyViolation):
                raise NotFoundUserForTaskRepo from e
        except SQLAlchemyError:
            raise TaskNotFoundRepo
    return wrapper
