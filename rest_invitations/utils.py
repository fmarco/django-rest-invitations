from importlib import import_module


def import_callable(path):
    if hasattr(path, '__call__'):
        return path
    else:
        module, attr_name = path.rsplit('.', 1)
        return getattr(import_module(module), attr_name)
