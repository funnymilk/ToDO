from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from psycopg2.errors import ForeignKeyViolation

class RefreshSessionNotFoundRepo(Exception):
    pass

class NotFoundUserForAuthRepo(Exception):
    pass

def auth_exceptions_trap(func):
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            result = func(*args, **kwargs)
            return result
        except IntegrityError as e:
            self.db.rollback()
            orig = e.orig
            msg = str(orig).lower()
            if "foreign key" in msg:
                raise NotFoundUserForAuthRepo from e
            if isinstance(orig, ForeignKeyViolation):
                raise NotFoundUserForAuthRepo from e
        except SQLAlchemyError as e:
            raise RefreshSessionNotFoundRepo from e
    return wrapper
