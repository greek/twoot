from index import startup

def toStartup(func):
    def decorator(*args, **kwargs):
        func(*args, **kwargs)
    
        startup()
    
    return decorator
