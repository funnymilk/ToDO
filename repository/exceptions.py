class NotFound(Exception):    
    pass

def exceptions_trap(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise NotFound        
        return result
    return wrapper
