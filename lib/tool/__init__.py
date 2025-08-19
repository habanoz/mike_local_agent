import os
import importlib
import inspect

def load_functions():
    functions = {}
    package_dir = os.path.dirname(__file__)
    for filename in os.listdir(package_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"{__name__}.{filename[:-3]}"
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isfunction):
                # Only include functions defined in this module
                if obj.__module__ == module.__name__ and not name.startswith('_'):
                    functions[name] = obj
    return functions