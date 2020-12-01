from index import startup

def to_startup(func):
    def decorator(*args, **kwargs):
        func(*args, **kwargs)
    
        startup()
    
    return decorator
