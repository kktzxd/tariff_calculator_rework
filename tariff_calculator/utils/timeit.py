from functools import wraps
import time

def timeit(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = method(self, *args, **kwargs)
        end_time = time.time()
        print(f"{method.__name__} выполнен за {end_time - start_time:.4f} сек")
        return result
    return wrapper