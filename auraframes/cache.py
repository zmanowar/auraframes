import json
import os

CACHE_DIR = 'cache/'

# TODO: Silly caching, should probably rework.

def save_to_cache(file_name, data):
    path = os.path.join(CACHE_DIR, file_name + '.json')
    with open(path, 'w') as f:
        json.dump(data, f)


def cache(file_name, use_arg=False):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if use_arg:
                path = os.path.join(CACHE_DIR, file_name + "-" + args[1] + '.json')
            else:
                path = os.path.join(CACHE_DIR, file_name + '.json')
            if os.path.isfile(path):
                with open(path, 'r') as f:
                    ret = json.load(f)
            else:
                with open(path, 'w') as f:
                    ret = function(*args, **kwargs)
                    json.dump(ret, f)
            return ret

        return wrapper

    return decorator


def async_cache(file_name):
    def decorator(function):
        async def wrapper(*args, **kwargs):
            path = os.path.join(CACHE_DIR, file_name + '.json')
            if os.path.isfile(path):
                with open(path, 'r') as f:
                    ret = json.load(f)
            else:
                with open(path, 'w') as f:
                    ret = await function(*args, **kwargs)
                    json.dump(ret, f)
            return ret

        return wrapper

    return decorator
